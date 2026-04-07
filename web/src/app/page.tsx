"use client";

import { useEffect, useState } from "react";
import Hero from "@/components/Hero";
import WorkspacePanel from "@/components/WorkspacePanel";
import InsightPanel from "@/components/InsightPanel";
import CollectionPanel from "@/components/CollectionPanel";
import StatePanel from "@/components/StatePanel";
import StatsStrip from "@/components/StatsStrip";
import ReferenceShelf from "@/components/ReferenceShelf";
import FeaturePanel from "@/components/FeaturePanel";
import { fetchDemo, type DemoPayload } from "@/lib/api";

export default function Page() {
  const [demo, setDemo] = useState<DemoPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchDemo();
      setDemo(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load studio context.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-[1400px] p-4 md:p-6">
        <Hero onRefresh={load} />
        <StatsStrip demo={demo} />
        <StatePanel loading={loading} error={error} onRetry={load} />

        <div className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-[1.15fr_1fr_0.85fr]">
          <WorkspacePanel demo={demo} onGenerated={setDemo} />
          <InsightPanel demo={demo} />
          <div className="space-y-4">
            <FeaturePanel demo={demo} />
            <CollectionPanel demo={demo} onOpened={setDemo} />
          </div>
        </div>

        <ReferenceShelf demo={demo} />
      </div>
    </main>
  );
}
