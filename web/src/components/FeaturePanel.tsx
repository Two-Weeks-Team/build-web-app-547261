"use client";

import type { DemoPayload } from "@/lib/api";

export default function FeaturePanel({ demo }: { demo: DemoPayload | null }) {
  return (
    <section className="paper rounded-lg border border-border p-4">
      <h3 className="text-lg font-semibold">Viability snapshot with rationale</h3>
      <p className="mt-1 text-2xl font-bold text-warning">Score {demo?.score ?? "--"}</p>
      <ul className="mt-2 list-disc pl-5 text-sm text-muted-foreground">
        {(demo?.rationale ?? []).map((r) => <li key={r}>{r}</li>)}
      </ul>
    </section>
  );
}
