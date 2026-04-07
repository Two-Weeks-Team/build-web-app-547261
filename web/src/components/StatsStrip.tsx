"use client";

import type { DemoPayload } from "@/lib/api";

export default function StatsStrip({ demo }: { demo: DemoPayload | null }) {
  return <section className="mt-4 grid grid-cols-2 gap-2 md:grid-cols-4">{["Spark", "Extraction", "Viability", "Brief"].map((s) => <div key={s} className="rounded-md border border-border bg-card p-2 text-xs">{s}: {demo ? "done" : "pending"}</div>)}</section>;
}
