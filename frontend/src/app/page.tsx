"use client";

import { useRef, useState } from "react";

import UploadCard from "@/components/UploadCard";
import VideoPlayer from "@/components/VideoPlayer";
import ChatPanel from "@/components/ChatPanel";
import StatusCard from "@/components/StatusCard";

const BACKEND_URL = "http://127.0.0.1:8000";

type TextResult = {
  start: number;
  end: number;
  frame: string;
  text: string;
};

type VisualResult = {
  start: number;
  end: number;
  frame: string;
};

type SearchResults = {
  text_results: TextResult[];
  visual_results: VisualResult[];
};

export default function Home() {
  const videoRef = useRef<HTMLVideoElement>(null);

  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("Choose a video to upload.");
  const [uploading, setUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState("");

  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);

  const [results, setResults] = useState<SearchResults | null>(null);

  // Jump video to timestamp
  function seekToTime(seconds: number) {
    if (!videoRef.current) return;

    videoRef.current.currentTime = seconds;
    videoRef.current.play();

    videoRef.current.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
  }

  // ---------------- Upload + Live Progress ----------------
  async function uploadVideo() {
    if (!file) return;

    setUploading(true);
    setResults(null);
    setStatus("📤 Uploading video...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Upload
      const uploadRes = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const uploadData = await uploadRes.json();

      if (!uploadRes.ok) {
        throw new Error(uploadData.detail || "Upload failed.");
      }

      setUploadedFile(uploadData.filename);

      // Start Processing
      const processRes = await fetch(
        `${BACKEND_URL}/process?filename=${encodeURIComponent(
          uploadData.filename
        )}`,
        {
          method: "POST",
        }
      );

      const processData = await processRes.json();

      if (!processRes.ok) {
        throw new Error(processData.detail || "Processing failed.");
      }

      // Live Progress (SSE)
      const taskId = processData.task_id;

      const source = new EventSource(
        `${BACKEND_URL}/progress/${taskId}`
      );

      source.onmessage = (event) => {
        const data = JSON.parse(event.data);

        setStatus(`${data.percent}% • ${data.stage}`);

        if (data.done) {
          source.close();
          setUploading(false);
          setStatus("✅ Processing Complete");
        }
      };

      source.onerror = () => {
        source.close();
        setUploading(false);
        setStatus("❌ Lost connection to progress stream.");
      };
    } catch (err: any) {
      setUploading(false);
      setStatus(`❌ ${err.message}`);
    }
  }

  // ---------------- Ask Question ----------------
  async function askQuestion(): Promise<SearchResults | null> {
    if (!question.trim()) return null;

    setAsking(true);

    try {
      const res = await fetch(
        `${BACKEND_URL}/query?question=${encodeURIComponent(question)}`
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Query failed.");
      }

      setResults(data.results);

      return data.results;
    } catch (err: any) {
      alert(err.message);
      return null;
    } finally {
      setAsking(false);
    }
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-zinc-950 text-white">

      {/* Background Glow */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,#2563eb33,transparent_55%)]" />

      <div className="relative mx-auto max-w-7xl px-6 py-10">

        {/* Header */}
        <header className="flex items-center justify-between">
          <h1 className="text-2xl font-bold tracking-tight">
            🎥 Multimodal Video RAG
          </h1>

          <span className="rounded-full border border-zinc-700 bg-zinc-900/70 px-4 py-1 text-sm text-zinc-300">
            Whisper • OCR • CLIP
          </span>
        </header>

        {/* Hero */}
        <section className="mt-16 text-center">
          <h2 className="text-5xl font-extrabold leading-tight md:text-6xl">
            Ask Anything About
            <span className="block bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
              Your Videos
            </span>
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-lg text-zinc-400">
            Upload a video, let AI analyze speech, text and visuals,
            then retrieve answers with timestamps and frame references.
          </p>
        </section>

        {/* Upload */}
        <section className="mx-auto mt-14 max-w-5xl">
          <UploadCard
            file={file}
            setFile={setFile}
            uploadVideo={uploadVideo}
            uploading={uploading}
            status={status}
            uploadedFile={uploadedFile}
          />
        </section>

        {/* Live Status */}
        {uploading && (
          <section className="mx-auto mt-8 max-w-5xl">
            <StatusCard status={status} />
          </section>
        )}

        {/* Workspace */}
        {uploadedFile && (
          <section className="mx-auto mt-10 grid max-w-7xl gap-8 lg:grid-cols-[1.1fr_1fr]">

            {/* Left */}
            <VideoPlayer
              videoRef={videoRef}
              videoUrl={`${BACKEND_URL}/videos/${encodeURIComponent(uploadedFile)}`}
            />

            {/* Right */}
            <ChatPanel
              question={question}
              setQuestion={setQuestion}
              asking={asking}
              askQuestion={askQuestion}
              seekToTime={seekToTime}
              backendUrl={BACKEND_URL}
            />
          </section>
        )}
      </div>
    </main>
  );
}