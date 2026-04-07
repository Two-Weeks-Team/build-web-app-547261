"use client";

import { useState } from "react";
import { fetchInsights } from "@/lib/api";
import type { DemoPayload } from "@/lib/api";

export default function InsightPanel({ demo }: { demo: DemoPayload | null }) {
  const [insights, setInsights] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    setLoading(true);
    const res = await fetchInsights("MVP Scope", demo?.summary ?? "");
    setInsights(res.insights);
    setLoading(false);
  };

  return (
    <section className="paper rounded-lg border border-border p-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Structured MVP Brief</h2>
        <button onClick={run} className="rounded-md border border-border bg-muted px-3 py-1 text-xs">{loading ? "Analyzing..." : "Refresh rationale"}</button>
      </div>
      <div className="mt-3 space-y-2 text-sm">
        {demo?.brief ? Object.entries(demo.brief).map(([k, v]) => <div key={k} className="rounded-md border border-border bg-card p-2"><strong>{k}:</strong> {v}</div>) : <p className="text-muted-foreground">No brief yet.</p>}
      </div>
      <ul className="mt-3 list-disc pl-5 text-sm text-muted-foreground">
        {insights.map((i) => <li key={i}>{i}</li>)}
      </ul>
    </section>
  );
}
