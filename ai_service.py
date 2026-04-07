import json
import os
import re
from typing import Any, Dict, List

import httpx


INFERENCE_URL = "https://inference.do-ai.run/v1/chat/completions"
DEFAULT_MODEL = os.getenv("DO_INFERENCE_MODEL", "anthropic-claude-4.6-sonnet")


def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


def _coerce_unstructured_payload(raw_text: str) -> dict[str, object]:
    compact = raw_text.strip()
    normalized = compact.replace("\n", ",")
    tags = [part.strip(" -•\t") for part in normalized.split(",") if part.strip(" -•\t")]
    if not tags:
        tags = ["guided plan", "saved output", "shareable insight"]
    headline = tags[0].title()
    items = []
    for index, tag in enumerate(tags[:3], start=1):
        items.append({
            "title": f"Stage {index}: {tag.title()}",
            "detail": f"Use {tag} to move the request toward a demo-ready outcome.",
            "score": min(96, 80 + index * 4),
        })
    highlights = [tag.title() for tag in tags[:3]]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact or f"{headline} fallback is ready for review.",
        "tags": tags[:6],
        "items": items,
        "score": 88,
        "insights": [f"Lead with {headline} on the first screen.", "Keep one clear action visible throughout the flow."],
        "next_actions": ["Review the generated plan.", "Save the strongest output for the demo finale."],
        "highlights": highlights,
    }

def _normalize_inference_payload(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return _coerce_unstructured_payload(str(payload))
    normalized = dict(payload)
    summary = str(normalized.get("summary") or normalized.get("note") or "AI-generated plan ready")
    raw_items = normalized.get("items")
    items: list[dict[str, object]] = []
    if isinstance(raw_items, list):
        for index, entry in enumerate(raw_items[:3], start=1):
            if isinstance(entry, dict):
                title = str(entry.get("title") or f"Stage {index}")
                detail = str(entry.get("detail") or entry.get("description") or title)
                score = float(entry.get("score") or min(96, 80 + index * 4))
            else:
                label = str(entry).strip() or f"Stage {index}"
                title = f"Stage {index}: {label.title()}"
                detail = f"Use {label} to move the request toward a demo-ready outcome."
                score = float(min(96, 80 + index * 4))
            items.append({"title": title, "detail": detail, "score": score})
    if not items:
        items = _coerce_unstructured_payload(summary).get("items", [])
    raw_insights = normalized.get("insights")
    if isinstance(raw_insights, list):
        insights = [str(entry) for entry in raw_insights if str(entry).strip()]
    elif isinstance(raw_insights, str) and raw_insights.strip():
        insights = [raw_insights.strip()]
    else:
        insights = []
    next_actions = normalized.get("next_actions")
    if isinstance(next_actions, list):
        next_actions = [str(entry) for entry in next_actions if str(entry).strip()]
    else:
        next_actions = []
    highlights = normalized.get("highlights")
    if isinstance(highlights, list):
        highlights = [str(entry) for entry in highlights if str(entry).strip()]
    else:
        highlights = []
    if not insights and not next_actions and not highlights:
        fallback = _coerce_unstructured_payload(summary)
        insights = fallback.get("insights", [])
        next_actions = fallback.get("next_actions", [])
        highlights = fallback.get("highlights", [])
    return {
        **normalized,
        "summary": summary,
        "items": items,
        "score": float(normalized.get("score") or 88),
        "insights": insights,
        "next_actions": next_actions,
        "highlights": highlights,
    }


async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    token = os.getenv("GRADIENT_MODEL_ACCESS_KEY") or os.getenv("DIGITALOCEAN_INFERENCE_KEY")
    if not token:
        return {
            "ok": False,
            "note": "AI temporarily unavailable: missing inference credentials.",
            "data": None,
        }

    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "temperature": 0.4,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(INFERENCE_URL, headers=headers, json=payload)
            response.raise_for_status()
            raw = response.json()

        content = raw.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        extracted = _extract_json(content)
        parsed = json.loads(extracted)
        return {"ok": True, "note": None, "data": parsed}
    except Exception:
        return {
            "ok": False,
            "note": "AI temporarily unavailable; using fallback planning logic.",
            "data": None,
        }


async def generate_brief(query: str, preferences: str) -> Dict[str, Any]:
    schema_hint = {
        "summary": "string",
        "items": [
            {"section": "Problem", "content": "string"},
            {"section": "Target Users", "content": "string"},
            {"section": "Core Loop", "content": "string"},
            {"section": "MVP Scope", "content": "string"},
            {"section": "User Flow Outline", "content": "string"},
            {"section": "Risks", "content": "string"},
            {"section": "Success Criteria", "content": "string"},
            {"section": "Viability Rationale", "content": "string"}
        ],
        "score": 0
    }

    messages = [
        {"role": "system", "content": "You are a product-planning copilot. Return JSON only."},
        {
            "role": "user",
            "content": (
                "Turn the rough idea into an execution-ready MVP brief. "
                "Include concise, practical content. Score must be 0-100. "
                f"Output schema: {json.dumps(schema_hint)}\n\n"
                f"Rough idea:\n{query}\n\n"
                f"Preferences:\n{preferences}"
            ),
        },
    ]

    result = await _call_inference(messages, max_tokens=512)
    if result.get("ok") and isinstance(result.get("data"), dict):
        data = result["data"]
        summary = str(data.get("summary", "Execution-ready MVP brief generated."))
        items = data.get("items", [])
        score = int(data.get("score", 72))
        score = max(0, min(100, score))
        return {"summary": summary, "items": items, "score": score, "note": result.get("note")}

    return {
        "summary": "Fallback draft: clear MVP direction generated from incomplete extraction.",
        "items": [
            {"section": "Problem", "content": "Users struggle to turn rough ideas into actionable product plans quickly."},
            {"section": "Target Users", "content": "Solo founders, PMs, and hackathon teams starting with incomplete context."},
            {"section": "Core Loop", "content": "Paste rough notes → generate structured brief → review viability rationale → save artifact."},
            {"section": "MVP Scope", "content": "Intake canvas, process ribbon, brief cards, viability badges, and artifact shelf."},
            {"section": "User Flow Outline", "content": "Input rough idea, generate one-pass brief, inspect rationale, save and version outputs."},
            {"section": "Risks", "content": "Overly broad scope and ambiguous audience; mitigate with constraint prompts."},
            {"section": "Success Criteria", "content": "User gets usable first-pass brief in one run and saves at least one artifact."},
            {"section": "Viability Rationale", "content": "Strong need and clear workflow; confidence reduced due to incomplete extraction."}
        ],
        "score": 72,
        "note": "AI temporarily unavailable; served polished fallback draft.",
    }


async def generate_insights(selection: str, context: str) -> Dict[str, Any]:
    messages = [
        {"role": "system", "content": "You analyze product planning artifacts. Return JSON only."},
        {
            "role": "user",
            "content": (
                "Return JSON with keys: insights (list of strings), next_actions (list of strings), highlights (list of strings). "
                "Focus on execution-readiness and scope quality.\n\n"
                f"Selection:\n{selection}\n\nContext:\n{context}"
            ),
        },
    ]

    result = await _call_inference(messages, max_tokens=512)
    if result.get("ok") and isinstance(result.get("data"), dict):
        data = result["data"]
        return {
            "insights": data.get("insights", []),
            "next_actions": data.get("next_actions", []),
            "highlights": data.get("highlights", []),
            "note": result.get("note"),
        }

    return {
        "insights": [
            "The brief is strongest when target users and core loop are tightly scoped.",
            "Execution confidence increases when dependencies and timeline assumptions are explicit."
        ],
        "next_actions": [
            "Narrow MVP scope to one user segment and one primary workflow.",
            "Define first-release success criteria with measurable adoption signals."
        ],
        "highlights": [
            "One-pass source-to-brief transformation is clear and demo-ready.",
            "Fallback planning direction remains credible for incomplete input."
        ],
        "note": "AI temporarily unavailable; returned deterministic planning insights.",
    }
