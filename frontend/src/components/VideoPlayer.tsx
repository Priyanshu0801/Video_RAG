"use client";

import { RefObject } from "react";

type VideoPlayerProps = {
  videoRef: RefObject<HTMLVideoElement | null>;
  videoUrl: string;
};

export default function VideoPlayer({
  videoRef,
  videoUrl,
}: VideoPlayerProps) {
  return (
    <div className="sticky top-6 overflow-hidden rounded-3xl border border-zinc-800 bg-zinc-900/60 shadow-2xl backdrop-blur-xl">
      {/* Header */}
      <div className="border-b border-zinc-800 px-5 py-4">
        <h2 className="text-xl font-semibold">🎬 Video Player</h2>
        <p className="text-sm text-zinc-400">
          Click any timestamp from the chat to jump instantly.
        </p>
      </div>

      {/* Video */}
      <div className="p-4">
        <video
          ref={videoRef}
          controls
          className="aspect-video w-full rounded-2xl bg-black"
          src={videoUrl}
        />

        {/* Controls Info */}
        <div className="mt-4 rounded-xl border border-zinc-800 bg-zinc-950 p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-zinc-400">Status</span>
            <span className="rounded-full bg-green-500/20 px-3 py-1 text-xs font-medium text-green-400">
              Ready
            </span>
          </div>

          <div className="mt-4 grid grid-cols-3 gap-3 text-center">
            <div className="rounded-lg bg-zinc-900 p-3">
              <div className="text-lg">🎙</div>
              <p className="mt-1 text-xs text-zinc-400">Whisper</p>
            </div>

            <div className="rounded-lg bg-zinc-900 p-3">
              <div className="text-lg">📝</div>
              <p className="mt-1 text-xs text-zinc-400">OCR</p>
            </div>

            <div className="rounded-lg bg-zinc-900 p-3">
              <div className="text-lg">👁</div>
              <p className="mt-1 text-xs text-zinc-400">CLIP</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}