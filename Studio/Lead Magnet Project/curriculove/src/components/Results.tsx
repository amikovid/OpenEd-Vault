"use client";

import {
  PhilosophyTag,
  PhilosophyScores,
  PHILOSOPHY_NAMES,
  getSortedPhilosophies,
} from "@/lib/quiz-agent/scoring";

interface ResultsProps {
  result: {
    primary: {
      tag: PhilosophyTag;
      name: string;
      description: string;
      score: number;
    };
    secondary: {
      tag: PhilosophyTag;
      name: string;
      score: number;
    }[];
    confidence: number;
    scores: PhilosophyScores;
  };
  onContinue: () => void;
}

export default function Results({ result, onContinue }: ResultsProps) {
  const sorted = getSortedPhilosophies(result.scores);
  const maxScore = Math.max(...Object.values(result.scores), 1);
  const topFive = sorted.slice(0, 5).filter((p) => p.score > 0);
  const primaryPercent = Math.round((result.primary.score / maxScore) * 100);

  return (
    <div className="mobile-container flex flex-col min-h-[100dvh]">
      {/* Header */}
      <div className="p-6 pb-0">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-xl font-bold text-[var(--foreground)]">
              Curriculove
            </h1>
            <p className="text-sm text-[var(--foreground-muted)]">
              Your Homeschool Profile
            </p>
          </div>
          <div className="match-badge">
            <span className="material-symbols-outlined text-base">verified</span>
            {result.confidence}% match
          </div>
        </div>
      </div>

      <div className="flex-1 px-6 pb-6 overflow-auto">
        {/* Primary Result Card */}
        <div className="card-elevated p-6 mb-6 animate-slide-up">
          <div className="text-center mb-6">
            <span className="chip-primary mb-3 inline-block">
              <span className="material-symbols-outlined text-sm mr-1">star</span>
              Primary Match
            </span>
            <h2 className="text-2xl font-bold text-[var(--foreground)] mb-2">
              {result.primary.name}
            </h2>
            <p className="text-[var(--foreground-secondary)] text-sm leading-relaxed">
              {result.primary.description}
            </p>
          </div>

          {/* Primary score bar */}
          <div className="bg-[var(--surface-secondary)] rounded-xl p-4">
            <div className="flex justify-between text-sm mb-2">
              <span className="font-semibold text-[var(--foreground)]">
                {result.primary.tag}
              </span>
              <span className="font-bold text-[var(--primary)]">
                {primaryPercent}%
              </span>
            </div>
            <div className="h-3 bg-[var(--border-light)] rounded-full overflow-hidden">
              <div
                className="h-full bg-[var(--primary)] rounded-full transition-all duration-700"
                style={{ width: `${primaryPercent}%` }}
              />
            </div>
          </div>
        </div>

        {/* Secondary Matches */}
        {result.secondary.length > 0 && (
          <div className="card p-5 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <span className="material-symbols-outlined text-[var(--foreground-muted)] text-xl">
                leaderboard
              </span>
              <h3 className="text-sm font-semibold text-[var(--foreground-muted)] uppercase tracking-wide">
                Also strong matches
              </h3>
            </div>
            <div className="space-y-4">
              {result.secondary.map((match) => {
                const percent = Math.round((match.score / maxScore) * 100);
                return (
                  <div key={match.tag}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="font-medium text-[var(--foreground)]">
                        {match.name}
                      </span>
                      <span className="text-[var(--foreground-secondary)]">
                        {percent}%
                      </span>
                    </div>
                    <div className="h-2 bg-[var(--surface-secondary)] rounded-full overflow-hidden">
                      <div
                        className="h-full bg-[var(--foreground-muted)] rounded-full transition-all duration-500"
                        style={{ width: `${percent}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Full Breakdown */}
        <div className="card p-5 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <span className="material-symbols-outlined text-[var(--foreground-muted)] text-xl">
              analytics
            </span>
            <h3 className="text-sm font-semibold text-[var(--foreground-muted)] uppercase tracking-wide">
              Full Profile
            </h3>
          </div>
          <div className="space-y-3">
            {topFive.map((philosophy, index) => {
              const percentage = Math.round((philosophy.score / maxScore) * 100);
              const isPrimary = index === 0;

              return (
                <div key={philosophy.tag} className="flex items-center gap-3">
                  <span className="w-8 text-xs font-mono text-[var(--foreground-muted)]">
                    {philosophy.tag}
                  </span>
                  <div className="flex-1 h-2 bg-[var(--surface-secondary)] rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        isPrimary ? "bg-[var(--primary)]" : "bg-[var(--foreground-muted)]"
                      }`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <span className="w-10 text-xs text-right text-[var(--foreground-secondary)] font-medium">
                    {percentage}%
                  </span>
                </div>
              );
            })}
          </div>

          {/* Tag legend */}
          <div className="mt-4 pt-4 border-t border-[var(--border)]">
            <div className="flex flex-wrap gap-2">
              {topFive.slice(0, 3).map((p) => (
                <span key={p.tag} className="chip text-xs">
                  {p.tag} = {PHILOSOPHY_NAMES[p.tag]}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* CTA */}
        <button
          onClick={onContinue}
          className="w-full py-4 bg-[var(--primary)] hover:bg-[var(--primary-hover)] text-[var(--background-dark)] rounded-2xl font-semibold transition-all duration-200 flex items-center justify-center gap-2 active:scale-[0.98]"
        >
          <span>See Matching Curricula</span>
          <span className="material-symbols-outlined text-xl">arrow_forward</span>
        </button>

        <p className="text-center text-xs text-[var(--foreground-muted)] mt-4 pb-4">
          Based on your answers, we'll show curricula that fit your style
        </p>
      </div>
    </div>
  );
}
