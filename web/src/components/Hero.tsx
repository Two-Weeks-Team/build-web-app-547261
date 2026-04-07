"use client";

export default function Hero({ onRefresh }: { onRefresh: () => void }) {
  return (
    <header className="paper rounded-lg border border-border p-4 md:p-5">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Idea Distillery Studio</p>
          <h1 className="text-2xl md:text-4xl font-bold">Build Web App — one-pass MVP brief composer</h1>
          <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
            Keep rough context and structured output in the same frame. Spark → Extraction → Viability → Brief → Save.
          </p>
        </div>
        <button onClick={onRefresh} className="rounded-md border border-border bg-muted px-4 py-2 text-sm hover:bg-card transition-colors">
          Refresh Studio Data
        </button>
      </div>
    </header>
  );
}
