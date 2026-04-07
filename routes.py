import json
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ai_service import generate_brief, generate_insights
from models import ArtifactSnapshot, PlanningArtifact, SessionLocal


router = APIRouter()


class PlanRequest(BaseModel):
    query: str
    preferences: Optional[str] = ""


class InsightsRequest(BaseModel):
    selection: str
    context: Optional[str] = ""


class SaveArtifactRequest(BaseModel):
    title: str
    raw_input: str
    preferences: Optional[str] = ""
    summary: str
    items: List[dict]
    score: int
    note: Optional[str] = None
    is_fallback: Optional[bool] = False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/plan")
@router.post("/plan")
async def plan(payload: PlanRequest):
    return await generate_brief(payload.query, payload.preferences or "")


@router.post("/insights")
@router.post("/insights")
async def insights(payload: InsightsRequest):
    return await generate_insights(payload.selection, payload.context or "")


@router.get("/artifacts")
@router.get("/artifacts")
def list_artifacts(db: Session = Depends(get_db)):
    rows = db.query(PlanningArtifact).order_by(PlanningArtifact.updated_at.desc()).limit(30).all()
    data = []
    for r in rows:
        data.append(
            {
                "id": r.id,
                "title": r.title,
                "summary": r.summary,
                "score": r.score,
                "is_fallback": bool(r.is_fallback),
                "note": r.note,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            }
        )
    return {"artifacts": data}


@router.post("/artifacts/save")
@router.post("/artifacts/save")
def save_artifact(payload: SaveArtifactRequest, db: Session = Depends(get_db)):
    artifact = PlanningArtifact(
        title=payload.title,
        raw_input=payload.raw_input,
        preferences_json=json.dumps({"preferences": payload.preferences or ""}),
        summary=payload.summary,
        items_json=json.dumps(payload.items),
        score=max(0, min(100, payload.score)),
        note=payload.note,
        is_fallback=bool(payload.is_fallback),
    )
    db.add(artifact)
    db.commit()
    db.refresh(artifact)

    snap = ArtifactSnapshot(
        artifact_id=artifact.id,
        version=1,
        summary=artifact.summary,
        items_json=artifact.items_json,
        score=artifact.score,
        note=artifact.note,
    )
    db.add(snap)
    db.commit()

    return {"id": artifact.id, "message": "Artifact saved to shelf."}
