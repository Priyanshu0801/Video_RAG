"use client";

type StatusCardProps = {
  status: string;
};

const steps = [
  { label: "Uploading", emoji: "📤" },
  { label: "Transcribing", emoji: "🎙" },
  { label: "Extracting Frames", emoji: "🎞" },
  { label: "OCR", emoji: "📝" },
  { label: "Building Text Index", emoji: "📚" },
  { label: "Building Visual Index", emoji: "👁" },
  { label: "Completed", emoji: "✅" },
];

export default function StatusCard({ status }: StatusCardProps) {
  const completed =
    status.includes("Processing Complete") || status.startsWith("✅");

  let activeStep = 0;

  if (status.includes("Uploading")) activeStep = 0;
  else if (status.includes("Transcribing")) activeStep = 1;
  else if (status.includes("OCR")) activeStep = 3;
  else if (status.includes("Index")) activeStep = 5;
  else if (completed) activeStep = 6;

  return (
    <div className="rounded-3xl border border-zinc-800 bg-zinc-900/60 p-6 shadow-xl backdrop-blur-xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">⚡ AI Processing Pipeline</h3>

        <span
          className={`rounded-full px-3 py-1 text-xs font-medium ${
            completed
              ? "bg-green-500/20 text-green-400"
              : "bg-blue-500/20 text-blue-400"
          }`}
        >
          {completed ? "Completed" : "Running"}
        </span>
      </div>

      {/* Current Status */}
      <div className="mt-5 rounded-xl border border-zinc-800 bg-zinc-950 p-4">
        <p className="text-sm text-zinc-400">Current Status</p>
        <p className="mt-1 font-medium">{status}</p>
      </div>

      {/* Timeline */}
      <div className="mt-6 space-y-3">
        {steps.map((step, index) => {
          const done = index < activeStep;
          const active = index === activeStep && !completed;
          const finalDone = completed && index === 6;

          return (
            <div
              key={step.label}
              className={`flex items-center gap-4 rounded-xl border p-3 transition-all ${
                done || finalDone
                  ? "border-green-500/30 bg-green-500/10"
                  : active
                  ? "border-blue-500/40 bg-blue-500/10"
                  : "border-zinc-800 bg-zinc-950"
              }`}
            >
              <div
                className={`flex h-10 w-10 items-center justify-center rounded-full text-lg ${
                  done || finalDone
                    ? "bg-green-500/20"
                    : active
                    ? "bg-blue-500/20 animate-pulse"
                    : "bg-zinc-800"
                }`}
              >
                {done || finalDone ? "✔" : step.emoji}
              </div>

              <div className="flex-1">
                <p className="font-medium">{step.label}</p>

                <p className="text-xs text-zinc-500">
                  {done || finalDone
                    ? "Completed"
                    : active
                    ? "In Progress..."
                    : "Pending"}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}