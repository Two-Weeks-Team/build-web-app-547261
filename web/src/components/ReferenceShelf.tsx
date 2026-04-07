"use client";

import type { DemoPayload } from "@/lib/api";

export default function ReferenceShelf({ demo }: { demo: DemoPayload | null }) {
  return (
    <section className="mt-4 rounded-lg border border-border bg-card p-4">
      <h3 className="text-lg font-semibold">Seeded planning playground</h3>
      <p className="text-sm text-muted-foreground mt-1">CampusPulse, LocalLoop, CreatorCircle, IdeaSpark MVP Brief, Fallback Planning Draft.</p>
      <p className="mt-2 text-sm">Fallback notice: {demo?.fallback_notice ?? "None"}</p>
    </section>
  );
}
