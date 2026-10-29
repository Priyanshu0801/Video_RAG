"use client";

type ResultCardProps = {
  frame: string;
  start: number;
  end: number;
  text?: string;
  type: "text" | "visual";
  backendUrl: string;
  seekToTime: (seconds: number) => void;
};

export default function ResultCard({
  frame,
  start,
  end,
  text,
  type,
  backendUrl,
  seekToTime,
}: ResultCardProps) {
  return (
    <div className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-950 shadow-lg transition hover:border-blue-500 hover:shadow-blue-500/10">
      {/* Frame Thumbnail */}
      <img
        src={`${backendUrl}/frames/${frame}`}
        alt={frame}
        className="h-48 w-full object-cover"
      />

      {/* Content */}
      <div className="p-4">
        <button
          onClick={() => seekToTime(start)}
          className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
            type === "text"
              ? "bg-blue-600 hover:bg-blue-500"
              : "bg-cyan-600 hover:bg-cyan-500"
          }`}
        >
          ▶ {start.toFixed(1)}s – {end.toFixed(1)}s
        </button>

        {text && (
          <p className="mt-4 text-zinc-200 leading-relaxed">
            {text}
          </p>
        )}

        <div className="mt-3 flex items-center justify-between">
          <span className="text-xs text-zinc-500">{frame}</span>

          <span
            className={`rounded-full px-2 py-1 text-xs ${
              type === "text"
                ? "bg-blue-500/20 text-blue-400"
                : "bg-cyan-500/20 text-cyan-400"
            }`}
          >
            {type === "text" ? "Transcript" : "Visual"}
          </span>
        </div>
      </div>
    </div>
  );
}