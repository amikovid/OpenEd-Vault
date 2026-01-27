"use client";

import { useState } from "react";
import { Curriculum, Recommendation, PHILOSOPHY_SHORT, getInsightData } from "@/lib/types";

interface SavedItem {
  slug: string;
  name: string;
  matchScore: number;
  reason: string;
  curriculum: Curriculum | null;
}

interface SavesListProps {
  items: SavedItem[];
  onRemove: (slug: string) => void;
  onBack?: () => void;
}

type FilterType = "all" | "high" | "medium" | "low";
type SortType = "match" | "name" | "price";

export default function SavesList({ items, onRemove, onBack }: SavesListProps) {
  const [filter, setFilter] = useState<FilterType>("all");
  const [sortBy, setSortBy] = useState<SortType>("match");
  const [expandedSlug, setExpandedSlug] = useState<string | null>(null);

  // Filter items
  let filteredItems = [...items];
  if (filter === "high") {
    filteredItems = filteredItems.filter((item) => item.matchScore >= 90);
  } else if (filter === "medium") {
    filteredItems = filteredItems.filter(
      (item) => item.matchScore >= 70 && item.matchScore < 90
    );
  } else if (filter === "low") {
    filteredItems = filteredItems.filter((item) => item.matchScore < 70);
  }

  // Sort items
  filteredItems.sort((a, b) => {
    if (sortBy === "match") return b.matchScore - a.matchScore;
    if (sortBy === "name") return a.name.localeCompare(b.name);
    if (sortBy === "price") {
      const priceOrder: Record<string, number> = {
        Free: 0,
        "$": 1,
        "$$": 2,
        "$$$": 3,
        "$$$$": 4,
      };
      const aPrice = priceOrder[a.curriculum?.priceTier || ""] ?? 5;
      const bPrice = priceOrder[b.curriculum?.priceTier || ""] ?? 5;
      return aPrice - bPrice;
    }
    return 0;
  });

  if (items.length === 0) {
    return (
      <div className="mobile-container flex flex-col min-h-[100dvh]">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-xl font-bold text-[var(--foreground)]">
                My Saves
              </h1>
              <p className="text-sm text-[var(--foreground-muted)]">
                Your saved curricula
              </p>
            </div>
          </div>
        </div>

        <div className="flex-1 flex flex-col items-center justify-center px-6 pb-20">
          <div className="card p-8 text-center w-full">
            <span className="material-symbols-outlined text-[var(--foreground-muted)] text-6xl mb-4">
              favorite_border
            </span>
            <h2 className="text-xl font-bold text-[var(--foreground)] mb-2">
              No saves yet
            </h2>
            <p className="text-[var(--foreground-secondary)] mb-6">
              Swipe right on curricula you like to save them here
            </p>
            {onBack && (
              <button
                onClick={onBack}
                className="px-6 py-3 bg-[var(--primary)] text-[var(--background-dark)] font-semibold rounded-full"
              >
                Start Discovering
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mobile-container flex flex-col min-h-[100dvh] pb-20">
      {/* Header */}
      <div className="p-6 pb-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-xl font-bold text-[var(--foreground)]">
              My Saves
            </h1>
            <p className="text-sm text-[var(--foreground-muted)]">
              {items.length} saved curricula
            </p>
          </div>
          <span className="chip-primary">
            <span className="material-symbols-outlined text-sm mr-1">favorite</span>
            {items.length}
          </span>
        </div>

        {/* Filter & Sort */}
        <div className="flex gap-2 overflow-x-auto pb-2">
          <button
            onClick={() => setFilter("all")}
            className={`chip whitespace-nowrap ${filter === "all" ? "chip-primary" : ""}`}
          >
            All
          </button>
          <button
            onClick={() => setFilter("high")}
            className={`chip whitespace-nowrap ${filter === "high" ? "chip-primary" : ""}`}
          >
            90%+ Match
          </button>
          <button
            onClick={() => setFilter("medium")}
            className={`chip whitespace-nowrap ${filter === "medium" ? "chip-primary" : ""}`}
          >
            70-89%
          </button>
          <button
            onClick={() => setSortBy(sortBy === "match" ? "name" : sortBy === "name" ? "price" : "match")}
            className="chip whitespace-nowrap"
          >
            <span className="material-symbols-outlined text-sm mr-1">sort</span>
            {sortBy === "match" ? "Match" : sortBy === "name" ? "A-Z" : "Price"}
          </button>
        </div>
      </div>

      {/* List */}
      <div className="flex-1 px-6 space-y-4">
        {filteredItems.map((item) => {
          const curriculum = item.curriculum;
          const isExpanded = expandedSlug === item.slug;

          return (
            <div key={item.slug} className="card overflow-hidden">
              {/* Main row */}
              <div
                className="p-4 flex items-center gap-4 cursor-pointer"
                onClick={() => setExpandedSlug(isExpanded ? null : item.slug)}
              >
                {/* Logo/Initial */}
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-[var(--background-dark)] to-[#1a3d2e] flex items-center justify-center flex-shrink-0">
                  {curriculum?.logoUrl ? (
                    <img
                      src={curriculum.logoUrl}
                      alt={item.name}
                      className="w-10 h-10 object-contain"
                    />
                  ) : (
                    <span className="text-white/50 text-xl font-bold">
                      {item.name.charAt(0)}
                    </span>
                  )}
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-[var(--foreground)] truncate">
                      {item.name}
                    </h3>
                    {curriculum?.isOpenEdVendor && (
                      <span className="material-symbols-outlined text-[var(--primary)] text-base flex-shrink-0">
                        verified
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="match-badge text-[10px]">
                      {item.matchScore}%
                    </span>
                    {curriculum?.priceTier && (
                      <span className="text-xs text-[var(--foreground-muted)]">
                        {curriculum.priceTier}
                      </span>
                    )}
                    {curriculum?.gradeRange && (
                      <span className="text-xs text-[var(--foreground-muted)]">
                        {curriculum.gradeRange}
                      </span>
                    )}
                  </div>
                </div>

                {/* Expand icon */}
                <span
                  className={`material-symbols-outlined text-[var(--foreground-muted)] transition-transform ${
                    isExpanded ? "rotate-180" : ""
                  }`}
                >
                  expand_more
                </span>
              </div>

              {/* Expanded content */}
              {isExpanded && (
                <div className="px-4 pb-4 border-t border-[var(--border)]">
                  <div className="pt-4">
                    {/* Philosophy chips */}
                    <div className="flex flex-wrap gap-2 mb-3">
                      {curriculum?.philosophyTags.slice(0, 3).map((tag) => (
                        <span key={tag} className="chip text-xs">
                          {PHILOSOPHY_SHORT[tag] || tag}
                        </span>
                      ))}
                    </div>

                    {/* Reason */}
                    <p className="text-sm text-[var(--foreground-secondary)] mb-4">
                      {item.reason}
                    </p>

                    {/* OpenEd Insight */}
                    {curriculum?.openedInsight && (() => {
                      const insight = getInsightData(curriculum.openedInsight);
                      if (!insight.synthesis && !insight.quote) return null;
                      return (
                        <div className="bg-[var(--primary-light)] rounded-lg p-3 mb-4">
                          <div className="flex items-center gap-1 mb-1">
                            <span className="material-symbols-outlined text-[var(--primary)] text-base">
                              lightbulb
                            </span>
                            <span className="text-xs font-semibold text-[var(--primary)]">
                              OpenEd Insight
                            </span>
                          </div>
                          {insight.quote && (
                            <p className="text-xs text-[var(--foreground)] leading-relaxed italic mb-1">
                              &ldquo;{insight.quote}&rdquo;
                              {insight.attribution && (
                                <span className="not-italic text-[var(--foreground-muted)]"> - {insight.attribution}</span>
                              )}
                            </p>
                          )}
                          {insight.synthesis && (
                            <p className="text-xs text-[var(--foreground)] leading-relaxed">
                              {insight.synthesis}
                            </p>
                          )}
                          {insight.hasFullReview && (
                            <a
                              href={`https://opened.co/tool/${curriculum.slug}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs font-semibold text-[var(--primary)] hover:underline mt-2 inline-flex items-center gap-1"
                            >
                              Read Full Review
                              <span className="material-symbols-outlined text-sm">arrow_forward</span>
                            </a>
                          )}
                        </div>
                      );
                    })()}

                    {/* Actions */}
                    <div className="flex gap-2">
                      {curriculum?.website && (
                        <a
                          href={curriculum.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex-1 py-2 bg-[var(--primary)] text-[var(--background-dark)] rounded-xl font-semibold text-sm flex items-center justify-center gap-1"
                        >
                          <span className="material-symbols-outlined text-base">
                            open_in_new
                          </span>
                          Visit Website
                        </a>
                      )}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onRemove(item.slug);
                        }}
                        className="px-4 py-2 border border-[var(--border)] rounded-xl text-[var(--foreground-muted)] text-sm flex items-center gap-1 hover:border-[var(--error)] hover:text-[var(--error)] transition-colors"
                      >
                        <span className="material-symbols-outlined text-base">
                          delete
                        </span>
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
