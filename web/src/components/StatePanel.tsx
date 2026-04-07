"use client";

export default function StatePanel({ loading, error, onRetry }: { loading: boolean; error: string | null; onRetry: () => void }) {
  if (loading) return <div className="mt-3 rounded-md border border-border bg-muted p-2 text-sm">Loading studio surfaces…</div>;
  if (error) return <div className="mt-3 rounded-md border border-border bg-card p-2 text-sm text-destructive">{error} <button onClick={onRetry} className="underline">Retry</button></div>;
  return <div className="mt-3 rounded-md border border-border bg-card p-2 text-sm text-success">Studio ready. Brief and artifact shelf are synced.</div>;
}
