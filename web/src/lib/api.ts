"use client";

export type DemoPayload = {
  summary: string;
  score: number;
  items: Array<{ id: string; title: string; status: string }>;
  brief?: Record<string, string>;
  artifacts?: Array<{ id: string; name: string; type: string; score: number }>;
  rationale?: string[];
  fallback_notice?: string;
};

const jsonHeaders = { "Content-Type": "application/json" };

async function parse<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return (await res.json()) as T;
}

export async function fetchDemo(): Promise<DemoPayload> {
  const res = await fetch("/api/demo", { cache: "no-store" });
  return parse<DemoPayload>(res);
}

export async function generatePlan(query: string, preferences: string): Promise<DemoPayload> {
  const res = await fetch("/api/plan", {
    method: "POST",
    headers: jsonHeaders,
    body: JSON.stringify({ query, preferences })
  });
  return parse<DemoPayload>(res);
}

export async function fetchInsights(selection: string, context: string): Promise<{ insights: string[]; next_actions: string[]; highlights: string[] }> {
  const res = await fetch("/api/insights", {
    method: "POST",
    headers: jsonHeaders,
    body: JSON.stringify({ selection, context })
  });
  return parse(res);
}

export async function saveArtifact(name: string, content: Record<string, string>, score: number): Promise<{ ok: boolean }> {
  const res = await fetch("/api/artifacts", {
    method: "POST",
    headers: jsonHeaders,
    body: JSON.stringify({ name, content, score })
  });
  return parse(res);
}
