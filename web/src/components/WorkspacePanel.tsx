"use client";

import { useState } from "react";
import { generatePlan } from "@/lib/api";
import type { DemoPayload } from "@/lib/api";

export default function WorkspacePanel({ demo, onGenerated }: { demo: DemoPayload | null; onGenerated: (v: DemoPayload) => void }) {
  const [query, setQuery] = useState("CampusPulse: students post real-time campus updates, clubs, alerts, and friend sightings. Need trust, moderation, and fast launch in one semester with a tiny team.");
  const [preferences, setPreferences] = useState("Audience: university students; Platform: mobile first; Timeline: 12 weeks; Monetization: sponsored campus spots later.");
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setRunning(true);
    setError(null);
    try {
      const next = await generatePlan(query, preferences);
      onGenerated(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Generation failed");
    } finally {
      setRunning(false);
    }
  };

  return (
    <section className="paper rounded-lg border border-border p-4">
      <h2 className="text-xl font-semibold">Rough context intake canvas</h2>
      <form onSubmit={submit} className="mt-3 space-y-3">
        <textarea value={query} onChange={(e) => setQuery(e.target.value)} className="h-40 w-full rounded-md border border-border bg-background p-3 text-sm" />
        <textarea value={preferences} onChange={(e) => setPreferences(e.target.value)} className="h-24 w-full rounded-md border border-border bg-background p-3 text-sm" />
        <button disabled={running} className="rounded-md bg-primary px-4 py-2 text-primary-foreground disabled:opacity-60">
          {running ? "Generating Brief..." : "Generate Brief"}
        </button>
      </form>
      {error && <p className="mt-2 text-sm text-destructive">{error}</p>}
      <p className="mt-3 text-xs text-muted-foreground">Current score: {demo?.score ?? "—"}</p>
    </section>
  );
}
