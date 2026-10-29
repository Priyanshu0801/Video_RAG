"use client";

import { useRef, useState } from "react";

type UploadCardProps = {
  file: File | null;
  setFile: (file: File | null) => void;
  uploadVideo: () => void;
  uploading: boolean;
  status: string;
  uploadedFile: string;
};

export default function UploadCard({
  file,
  setFile,
  uploadVideo,
  uploading,
  status,
  uploadedFile,
}: UploadCardProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState(false);

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const dropped = e.dataTransfer.files?.[0];
    if (dropped && dropped.type.startsWith("video/")) {
      setFile(dropped);
    }
  }

  function handleDragOver(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragActive(true);
  }

  function handleDragLeave(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragActive(false);
  }

  return (
    <div className="rounded-3xl border border-zinc-800 bg-zinc-900/60 p-8 shadow-2xl backdrop-blur-xl">
      {/* Drop Zone */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`flex cursor-pointer flex-col items-center rounded-2xl border-2 border-dashed px-8 py-16 transition-all ${
          dragActive
            ? "scale-[1.02] border-blue-500 bg-blue-500/10"
            : "border-zinc-700 hover:border-blue-500 hover:bg-zinc-900/80"
        }`}
        onClick={() => inputRef.current?.click()}
      >
        <div className="text-6xl">{dragActive ? "📂" : "📹"}</div>

        <h2 className="mt-5 text-3xl font-bold">
          {dragActive ? "Drop Video Here" : "Upload Your Video"}
        </h2>

        <p className="mt-3 text-center text-zinc-400">
          Drag & Drop or click to browse
        </p>

        <p className="mt-1 text-sm text-zinc-500">
          MP4 • MOV • AVI
        </p>

        <input
          ref={inputRef}
          type="file"
          accept="video/*"
          className="hidden"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        {/* Selected File */}
        {file && (
          <div className="mt-6 w-full max-w-md rounded-xl border border-zinc-700 bg-zinc-950 p-4">
            <div className="flex items-center gap-3">
              <div className="text-2xl">🎬</div>

              <div className="min-w-0 flex-1">
                <p className="truncate font-medium">{file.name}</p>

                <p className="text-xs text-zinc-500">
                  {(file.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Upload Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            uploadVideo();
          }}
          disabled={!file || uploading}
          className="mt-8 rounded-xl bg-blue-600 px-8 py-3 text-lg font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-zinc-700"
        >
          {uploading ? "Processing..." : "Upload Video"}
        </button>

        {/* Status */}
        <div className="mt-8 w-full max-w-xl rounded-xl border border-zinc-800 bg-zinc-900/70 px-5 py-4 text-center">
          <p className="text-sm text-zinc-300">{status}</p>

          {uploadedFile && (
            <p className="mt-2 text-xs text-zinc-500">
              File: {uploadedFile}
            </p>
          )}
        </div>
      </div>

      {/* AI Features */}
      <div className="mt-10 grid gap-4 md:grid-cols-3">
        <FeatureCard
          icon="🎙"
          title="Whisper"
          desc="Speech Transcription"
        />

        <FeatureCard
          icon="📝"
          title="OCR"
          desc="Text Detection"
        />

        <FeatureCard
          icon="👁"
          title="CLIP"
          desc="Visual Understanding"
        />
      </div>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  desc,
}: {
  icon: string;
  title: string;
  desc: string;
}) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5 text-center transition hover:border-blue-500 hover:bg-zinc-800">
      <div className="text-3xl">{icon}</div>

      <p className="mt-3 font-semibold">{title}</p>

      <p className="mt-1 text-sm text-zinc-400">{desc}</p>
    </div>
  );
}