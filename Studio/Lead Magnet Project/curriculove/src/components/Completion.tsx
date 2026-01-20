"use client";

import { useEffect, useState } from "react";

interface CompletionProps {
  savesCount: number;
  philosophyName: string;
  onViewSaves: () => void;
  onStartOver: () => void;
  onBrowseAll?: () => void;
}

export default function Completion({
  savesCount,
  philosophyName,
  onViewSaves,
  onStartOver,
  onBrowseAll,
}: CompletionProps) {
  const [showConfetti, setShowConfetti] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setShowConfetti(false), 3000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="mobile-container flex flex-col min-h-[100dvh] relative overflow-hidden">
      {/* Confetti */}
      {showConfetti && (
        <div className="absolute inset-0 pointer-events-none">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-3 h-3 rounded-full"
              style={{
                left: `${Math.random() * 100}%`,
                top: `-20px`,
                backgroundColor: i % 3 === 0
                  ? "var(--primary)"
                  : i % 3 === 1
                  ? "#FFD700"
                  : "#FF6B6B",
                animation: `confetti-fall ${2 + Math.random() * 2}s ease-out forwards`,
                animationDelay: `${Math.random() * 0.5}s`,
              }}
            />
          ))}
        </div>
      )}

      {/* Content */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 pb-20">
        {/* Success icon */}
        <div className="w-24 h-24 rounded-full bg-[var(--primary)] flex items-center justify-center mb-6 animate-slide-up">
          <span className="material-symbols-outlined text-[var(--background-dark)] text-5xl">
            celebration
          </span>
        </div>

        {/* Title */}
        <h1 className="text-2xl font-bold text-[var(--foreground)] text-center mb-2 animate-slide-up">
          Discovery Complete!
        </h1>

        <p className="text-[var(--foreground-secondary)] text-center mb-8 animate-slide-up">
          You've explored your top 3 {philosophyName} matches
        </p>

        {/* Stats card */}
        <div className="card-elevated p-6 w-full mb-8 animate-slide-up">
          <div className="flex justify-around text-center">
            <div>
              <div className="text-3xl font-bold text-[var(--primary)]">
                {savesCount}
              </div>
              <div className="text-sm text-[var(--foreground-muted)]">
                Saved
              </div>
            </div>
            <div className="w-px bg-[var(--border)]" />
            <div>
              <div className="text-3xl font-bold text-[var(--foreground)]">
                3
              </div>
              <div className="text-sm text-[var(--foreground-muted)]">
                Reviewed
              </div>
            </div>
          </div>
        </div>

        {/* Primary CTA */}
        <button
          onClick={onViewSaves}
          className="w-full py-4 bg-[var(--primary)] text-[var(--background-dark)] rounded-2xl font-semibold flex items-center justify-center gap-2 mb-4 active:scale-[0.98] transition-transform animate-slide-up"
        >
          <span className="material-symbols-outlined">favorite</span>
          View Your {savesCount} Saves
        </button>

        {/* Secondary CTA */}
        <button
          onClick={onBrowseAll || onViewSaves}
          className="w-full py-4 border-2 border-[var(--border)] text-[var(--foreground)] rounded-2xl font-semibold flex items-center justify-center gap-2 active:scale-[0.98] transition-transform animate-slide-up"
        >
          <span className="material-symbols-outlined">explore</span>
          Browse All Curricula
        </button>

        {/* Tip */}
        <div className="mt-8 text-center animate-slide-up">
          <p className="text-sm text-[var(--foreground-muted)]">
            <span className="material-symbols-outlined text-base align-middle mr-1">
              tips_and_updates
            </span>
            Pro tip: Visit each website to explore samples and pricing
          </p>
        </div>
      </div>
    </div>
  );
}
