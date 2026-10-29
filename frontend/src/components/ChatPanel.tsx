"use client";

import { useEffect, useRef, useState } from "react";
import ResultCard from "./ResultCard";

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

type Message = {
  id: number;
  role: "user" | "assistant";
  text: string;
  results?: SearchResults;
};

type ChatPanelProps = {
  question: string;
  setQuestion: (value: string) => void;
  asking: boolean;
  askQuestion: () => Promise<SearchResults | null>;
  seekToTime: (seconds: number) => void;
  backendUrl: string;
};

export default function ChatPanel({
  question,
  setQuestion,
  asking,
  askQuestion,
  seekToTime,
  backendUrl,
}: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleAsk() {
    if (!question.trim()) return;

    const userMessage: Message = {
      id: Date.now(),
      role: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    const askedQuestion = question;
    setQuestion("");

    const results = await askQuestion();

    const assistantMessage: Message = {
      id: Date.now() + 1,
      role: "assistant",
      text:
        results &&
        (results.text_results.length > 0 || results.visual_results.length > 0)
          ? `Found ${
              results.text_results.length + results.visual_results.length
            } relevant matches for "${askedQuestion}".`
          : `No matching results found for "${askedQuestion}".`,
      results: results ?? undefined,
    };

    setMessages((prev) => [...prev, assistantMessage]);
  }

  return (
    <div className="flex h-[82vh] flex-col overflow-hidden rounded-3xl border border-zinc-800 bg-zinc-900/60 shadow-2xl backdrop-blur-xl">
      {/* Header */}
      <div className="border-b border-zinc-800 px-5 py-4">
        <h2 className="text-xl font-semibold">💬 Video Chat</h2>
        <p className="text-sm text-zinc-400">
          Ask questions about speech, text and visuals.
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 space-y-5 overflow-y-auto p-5">
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center">
            <div className="text-center">
              <div className="text-5xl">🎬</div>

              <h3 className="mt-4 text-xl font-semibold">
                Start chatting with your video
              </h3>

              <p className="mt-2 text-zinc-400">
                Try: "dark night", "still together", "who is not alone?"
              </p>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id}>
            {/* User Bubble */}
            {msg.role === "user" && (
              <div className="flex justify-end">
                <div className="max-w-[80%] rounded-2xl bg-blue-600 px-4 py-3">
                  {msg.text}
                </div>
              </div>
            )}

            {/* Assistant Bubble */}
            {msg.role === "assistant" && (
              <div className="space-y-4">
                <div className="max-w-[90%] rounded-2xl border border-zinc-700 bg-zinc-800 px-4 py-3">
                  {msg.text}
                </div>

                {/* Text Results */}
                {msg.results?.text_results.map((item, i) => (
                  <ResultCard
                    key={`text-${i}`}
                    frame={item.frame}
                    start={item.start}
                    end={item.end}
                    text={item.text}
                    type="text"
                    backendUrl={backendUrl}
                    seekToTime={seekToTime}
                  />
                ))}

                {/* Visual Results */}
                {msg.results?.visual_results.length ? (
                  <div>
                    <h4 className="mb-2 text-sm font-semibold text-zinc-300">
                      Visual Matches
                    </h4>

                    <div className="grid gap-4 sm:grid-cols-2">
                      {msg.results.visual_results.map((item, i) => (
                        <ResultCard
                          key={`visual-${i}`}
                          frame={item.frame}
                          start={item.start}
                          end={item.end}
                          type="visual"
                          backendUrl={backendUrl}
                          seekToTime={seekToTime}
                        />
                      ))}
                    </div>
                  </div>
                ) : null}
              </div>
            )}
          </div>
        ))}

        {asking && (
          <div className="flex items-center gap-3">
            <div className="h-3 w-3 animate-pulse rounded-full bg-blue-400" />
            <div className="h-3 w-3 animate-pulse rounded-full bg-blue-400 [animation-delay:150ms]" />
            <div className="h-3 w-3 animate-pulse rounded-full bg-blue-400 [animation-delay:300ms]" />
            <span className="text-sm text-zinc-400">
              AI is searching...
            </span>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t border-zinc-800 p-4">
        <div className="flex gap-3">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Ask something about your video..."
            className="flex-1 rounded-xl border border-zinc-700 bg-zinc-950 px-4 py-3 outline-none focus:border-blue-500"
          />

          <button
            onClick={handleAsk}
            disabled={asking}
            className="rounded-xl bg-blue-600 px-6 py-3 font-semibold transition hover:bg-blue-500 disabled:bg-zinc-700"
          >
            {asking ? "..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}