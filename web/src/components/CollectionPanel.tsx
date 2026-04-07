"use client";

import { useState } from "react";
import { saveArtifact, fetchDemo } from "@/lib/api";
import type { DemoPayload } from "@/lib/api";

export default function CollectionPanel({ demo, onOpened }: { demo: DemoPayload | null; onOpened: (v: DemoPayload) => void }) {
  const [saving, setSaving] = useState(false);

  const onSave = async () => {
    if (!demo?.brief) return;
    setSaving(true);
    await saveArtifact("New Saved Planning Draft", demo.brief, demo.score);
    const refreshed = await fetchDemo();
    onOpened(refreshed);
    setSaving(false);
  };

  return (
    <section className="paper rounded-lg border border-border p-4">
      <h3 className="text-lg font-semibold">Persistent artifact shelf</h3>
      <div className="mt-2 space-y-2">
        {demo?.artifacts?.map((a) => <div key={a.id} className="rounded-md border border-border bg-card p-2 text-sm">{a.name} · {a.type} · {a.score}</div>)}
      </div>
      <button onClick={onSave} disabled={saving} className="mt-3 rounded-md bg-accent px-3 py-2 text-accent-foreground text-sm disabled:opacity-60">
        {saving ? "Saving..." : "Save current brief"}
      </button>
    </section>
  );
}
