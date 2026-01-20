"use client";

import { useState, useEffect } from "react";
import { useMutation } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { PhilosophyScores, PhilosophyTag } from "@/lib/quiz-agent/scoring";
import { Curriculum, Recommendation, PHILOSOPHY_SHORT, getInsightData } from "@/lib/types";
import VoiceReview from "./VoiceReview";

interface PolishedReview {
  curriculumSlug: string;
  rawTranscript: string;
  polishedReview: string;
  rating: number;
  highlights: string[];
  concerns: string[];
  bestFor: string[];
}

interface QuizResult {
  primary: {
    tag: PhilosophyTag;
    name: string;
    description: string;
    score: number;
  };
  secondary: { tag: PhilosophyTag; name: string; score: number }[];
  confidence: number;
  scores: PhilosophyScores;
}

interface RecommendationsProps {
  quizResult: QuizResult;
  onAddFavorite: (slug: string) => void;
  favorites: string[];
  onFinish: () => void;
  initialRecommendations?: Recommendation[]; // Optional pre-fetched recommendations
}

// Truncate text to first sentence (max 120 chars)
function truncateToSentence(text: string, maxLength = 120): string {
  if (!text) return "";
  const firstSentence = text.match(/^[^.!?]+[.!?]/);
  if (firstSentence && firstSentence[0].length <= maxLength) {
    return firstSentence[0];
  }
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + "...";
}

// Generate a placeholder image based on curriculum name
function getPlaceholderImage(name: string): string {
  // Using a gradient placeholder with curriculum initial
  return `data:image/svg+xml,${encodeURIComponent(`
    <svg width="400" height="500" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#1a3d2e;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#102219;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#grad)"/>
      <text x="50%" y="45%" font-family="Plus Jakarta Sans, sans-serif" font-size="120" font-weight="bold" fill="#13ec80" text-anchor="middle" dominant-baseline="middle">${name.charAt(0)}</text>
    </svg>
  `)}`;
}

export default function Recommendations({
  quizResult,
  onAddFavorite,
  favorites,
  onFinish,
  initialRecommendations,
}: RecommendationsProps) {
  const [recommendations, setRecommendations] = useState<Recommendation[]>(initialRecommendations || []);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(!initialRecommendations);
  const [error, setError] = useState<string | null>(null);
  const [swipeDirection, setSwipeDirection] = useState<"left" | "right" | null>(null);

  // Review modal state
  const [showReviewPrompt, setShowReviewPrompt] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [reviewCurriculum, setReviewCurriculum] = useState<Recommendation | null>(null);
  const [reviews, setReviews] = useState<PolishedReview[]>([]);

  // Loading message state
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);
  const LOADING_MESSAGES = [
    "Consulting the wisdom of Charlotte Mason...",
    "Checking if it sparks joy (and learning)...",
    "Cross-referencing with veteran homeschool moms...",
    "Calculating optimal couch-to-curriculum ratio...",
    "Searching for that Goldilocks fit...",
    "Making sure it won't collect dust on the shelf...",
    "Factoring in your coffee consumption needs...",
    "Avoiding anything that requires glitter...",
    "Finding curricula that won't make you cry...",
    "Balancing rigor with sanity...",
  ];

  useEffect(() => {
    if (isLoading) {
      const interval = setInterval(() => {
        setLoadingMessageIndex((prev) => (prev + 1) % LOADING_MESSAGES.length);
      }, 2500);
      return () => clearInterval(interval);
    }
  }, [isLoading]);

  // Convex mutation for submitting reviews
  const submitReview = useMutation(api.reviews.submitReview);

  useEffect(() => {
    // Only fetch if we don't have initial recommendations
    if (!initialRecommendations) {
      fetchRecommendations();
    }
  }, [quizResult, initialRecommendations]);

  const fetchRecommendations = async () => {
    try {
      setIsLoading(true);
      const res = await fetch("/api/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          primaryPhilosophy: quizResult.primary.tag,
          secondaryPhilosophies: quizResult.secondary.map((s) => s.tag),
          confidence: quizResult.confidence,
        }),
      });
      const data = await res.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setRecommendations(data.recommendations);
      setIsLoading(false);
    } catch (err) {
      setError(String(err));
      setIsLoading(false);
    }
  };

  const handleSwipe = (direction: "left" | "right") => {
    const current = recommendations[currentIndex];

    setSwipeDirection(direction);

    if (direction === "right" && current) {
      onAddFavorite(current.slug);
      // Show "Have you tried this?" prompt
      setReviewCurriculum(current);
      setShowReviewPrompt(true);
      // Don't auto-advance, wait for user response
      setTimeout(() => setSwipeDirection(null), 250);
      return;
    }

    setTimeout(() => {
      setSwipeDirection(null);
      if (currentIndex < recommendations.length - 1) {
        setCurrentIndex((prev) => prev + 1);
      } else {
        onFinish();
      }
    }, 250);
  };

  const handleReviewPromptResponse = (hasTriedIt: boolean) => {
    setShowReviewPrompt(false);
    if (hasTriedIt && reviewCurriculum) {
      setShowReviewModal(true);
    } else {
      // Advance to next card
      advanceToNext();
    }
  };

  const handleReviewSubmit = async (review: PolishedReview) => {
    setReviews((prev) => [...prev, review]);
    setShowReviewModal(false);

    // Save to Convex
    try {
      await submitReview({
        curriculumSlug: review.curriculumSlug,
        curriculumName: reviewCurriculum?.name || review.curriculumSlug,
        rawTranscript: review.rawTranscript,
        polishedReview: review.polishedReview,
        rating: review.rating,
        highlights: review.highlights,
        concerns: review.concerns,
        bestFor: review.bestFor,
        // userId, userEmail, userName will be added when Clerk auth is wired up
      });
      console.log("Review saved to Convex:", review.curriculumSlug);
    } catch (err) {
      // Gracefully handle if Convex isn't configured
      console.log("Review collected (Convex not configured):", review.curriculumSlug, err);
    }

    setReviewCurriculum(null);
    advanceToNext();
  };

  const advanceToNext = () => {
    if (currentIndex < recommendations.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      onFinish();
    }
  };

  // Loading state
  if (isLoading) {
    const maxScore = Math.max(...Object.values(quizResult.scores), 1);
    const primaryPercent = Math.round((quizResult.primary.score / maxScore) * 100);

    return (
      <div className="mobile-container flex flex-col min-h-[100dvh] bg-[var(--surface)]">
        {/* Header */}
        <header className="flex items-center p-4 pb-2 justify-between sticky top-0 bg-[var(--surface)]/80 backdrop-blur-md z-10">
          <div className="w-12" />
          <h2 className="text-lg font-bold text-[var(--foreground)]">Curriculove</h2>
          <div className="w-12" />
        </header>

        <div className="flex-1 flex flex-col items-center justify-center px-6 pb-20">
          <div className="card-elevated p-8 text-center w-full mb-4">
            <span className="chip-primary mb-4 inline-block">Your top match</span>
            <h2 className="text-2xl font-bold text-[var(--foreground)] mb-1">
              {quizResult.primary.name}
            </h2>
            <p className="text-[var(--primary)] font-medium mb-4">
              {primaryPercent}% match
            </p>
            <p className="text-[var(--foreground-secondary)] text-sm mb-6">
              {quizResult.primary.description}
            </p>
            <button
              disabled
              className="w-full py-4 bg-[var(--primary)]/50 text-[var(--background-dark)] rounded-full font-bold flex items-center justify-center gap-2 cursor-wait"
            >
              <span className="material-symbols-outlined animate-spin">progress_activity</span>
              See Your Matches
            </button>
          </div>

          <div className="flex items-center gap-3 text-[var(--foreground-muted)]">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-2 h-2 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-2 h-2 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
            <span className="text-sm transition-opacity duration-300">{LOADING_MESSAGES[loadingMessageIndex]}</span>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="mobile-container flex flex-col items-center justify-center min-h-[100dvh] p-6 bg-[var(--surface)]">
        <div className="card-elevated p-8 text-center w-full">
          <span className="material-symbols-outlined text-[var(--error)] text-5xl mb-4">
            error
          </span>
          <p className="text-[var(--error)] mb-6">{error}</p>
          <button
            onClick={fetchRecommendations}
            className="px-6 py-3 bg-[var(--primary)] text-[var(--background-dark)] font-semibold rounded-full"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const current = recommendations[currentIndex];

  // No more recommendations
  if (!current) {
    return (
      <div className="mobile-container flex flex-col items-center justify-center min-h-[100dvh] p-6 bg-[var(--surface)]">
        <div className="card-elevated p-8 text-center w-full">
          <span className="material-symbols-outlined text-[var(--primary)] text-6xl mb-4">
            check_circle
          </span>
          <h2 className="text-2xl font-bold text-[var(--foreground)] mb-2">
            All Done!
          </h2>
          <p className="text-[var(--foreground-secondary)] mb-6">
            You've reviewed all {recommendations.length} curricula
          </p>
          <button
            onClick={onFinish}
            className="w-full py-4 bg-[var(--primary)] text-[var(--background-dark)] rounded-full font-bold flex items-center justify-center gap-2"
          >
            <span className="material-symbols-outlined">favorite</span>
            See Your {favorites.length} Favorites
          </button>
        </div>
      </div>
    );
  }

  const curriculum = current.curriculum;
  const heroImage = curriculum?.imageUrl || curriculum?.logoUrl || getPlaceholderImage(current.name);

  return (
    <div className="mobile-container flex flex-col min-h-[100dvh] bg-[var(--background)]">
      {/* Header */}
      <header className="flex items-center p-4 pb-2 justify-between sticky top-0 bg-[var(--background)]/80 backdrop-blur-md z-10">
        <div className="w-12">
          <span className="material-symbols-outlined text-2xl text-[var(--foreground)]">menu</span>
        </div>
        <h2 className="text-lg font-bold text-[var(--foreground)]">Curriculove</h2>
        <div className="w-12" />
      </header>

      {/* Progress Indicator */}
      <div className="px-6 py-2">
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-center">
            <p className="text-[var(--foreground)] text-sm font-medium">Daily Discovery</p>
            <p className="text-[var(--primary)] text-xs font-semibold">
              {currentIndex + 1} of {recommendations.length} matches
            </p>
          </div>
          <div className="h-1.5 w-full bg-[var(--border)] rounded-full overflow-hidden">
            <div
              className="h-full bg-[var(--primary)] rounded-full transition-all duration-500"
              style={{ width: `${((currentIndex + 1) / recommendations.length) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Discovery Card */}
      <main className="flex-1 flex flex-col items-center justify-center p-4 relative overflow-hidden">
        <div
          className={`w-full max-w-md bg-[var(--surface)] rounded-xl shadow-xl overflow-hidden flex flex-col border border-[var(--border-light)] transition-all duration-250 ${
            swipeDirection === "left"
              ? "animate-slide-out-left"
              : swipeDirection === "right"
              ? "animate-slide-out-right"
              : "animate-slide-up"
          }`}
        >
          {/* Hero Image Section - 4:5 aspect ratio */}
          <div
            className="relative w-full aspect-[4/5] bg-center bg-no-repeat bg-cover"
            style={{ backgroundImage: `url("${heroImage}")` }}
          >
            {/* Match Badge */}
            <div className="absolute top-4 right-4 bg-[var(--primary)] text-[var(--background-dark)] px-3 py-1.5 rounded-full font-bold text-sm shadow-lg flex items-center gap-1">
              <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>bolt</span>
              {current.matchScore}% Match
            </div>

            {/* OpenEd Partner badge */}
            {curriculum?.isOpenEdVendor && (
              <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm text-[var(--background-dark)] text-xs font-semibold px-2 py-1 rounded-full flex items-center gap-1">
                <span className="material-symbols-outlined text-sm">verified</span>
                OpenEd Partner
              </div>
            )}

            {/* Gradient Overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />

            {/* Title and Tagline on Image */}
            <div className="absolute bottom-4 left-4 right-4 text-white">
              <h1 className="text-3xl font-bold leading-tight">{current.name}</h1>
              {curriculum?.description && (
                <p className="text-white/90 text-sm font-medium italic mt-1">
                  {truncateToSentence(curriculum.description, 80)}
                </p>
              )}
            </div>
          </div>

          {/* Content Details */}
          <div className="p-5 flex flex-col gap-4">
            {/* Chips */}
            <div className="flex gap-2 flex-wrap">
              {curriculum?.priceTier && (
                <div className="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-[var(--primary)]/20 px-3 border border-[var(--primary)]/20">
                  <span className="material-symbols-outlined text-sm text-[var(--foreground)]">payments</span>
                  <p className="text-[var(--foreground)] text-xs font-bold">{curriculum.priceTier}</p>
                </div>
              )}
              {curriculum?.gradeRange && (
                <div className="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-[var(--background)] px-3 border border-[var(--border)]">
                  <span className="material-symbols-outlined text-sm text-[var(--foreground-muted)]">school</span>
                  <p className="text-[var(--foreground-secondary)] text-xs font-bold">{curriculum.gradeRange}</p>
                </div>
              )}
              {curriculum?.philosophyTags.slice(0, 2).map((tag) => (
                <div key={tag} className="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-[var(--background)] px-3 border border-[var(--border)]">
                  <span className="material-symbols-outlined text-sm text-[var(--foreground-muted)]">psychology</span>
                  <p className="text-[var(--foreground-secondary)] text-xs font-bold">{PHILOSOPHY_SHORT[tag] || tag}</p>
                </div>
              ))}
            </div>

            {/* Why it matches Section */}
            <div className="flex flex-col gap-1.5">
              <h3 className="text-[var(--primary)] text-xs font-bold uppercase tracking-wider">Why it matches you</h3>
              <p className="text-[var(--foreground-secondary)] text-sm leading-relaxed">
                {current.reason}
              </p>
            </div>

            {/* OpenEd Insight */}
            {curriculum?.openedInsight && (() => {
              const insight = getInsightData(curriculum.openedInsight);
              if (!insight.synthesis && !insight.quote) return null;
              return (
                <div className="flex flex-col items-start justify-between gap-3 rounded-lg border border-[var(--border)] bg-[var(--background)] p-4">
                  <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-2">
                      <span className="material-symbols-outlined text-[var(--primary)] text-xl">verified</span>
                      <p className="text-[var(--foreground)] text-sm font-bold">OpenEd Insight</p>
                    </div>
                    {insight.quote && (
                      <p className="text-[var(--foreground)] text-sm italic leading-relaxed">
                        &ldquo;{insight.quote}&rdquo;
                        {insight.attribution && (
                          <span className="text-[var(--foreground-muted)] not-italic"> - {insight.attribution}</span>
                        )}
                      </p>
                    )}
                    {insight.synthesis && (
                      <p className="text-[var(--foreground-muted)] text-xs leading-normal">
                        {truncateToSentence(insight.synthesis)}
                      </p>
                    )}
                  </div>
                  {insight.hasFullReview && (
                    <a
                      href={`https://opened.co/tool/${curriculum.slug}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs font-bold tracking-wide flex items-center gap-1 text-[var(--primary)] hover:underline"
                    >
                      Read Full Review
                      <span className="material-symbols-outlined text-sm">arrow_forward</span>
                    </a>
                  )}
                </div>
              );
            })()}
          </div>
        </div>
      </main>

      {/* Floating Action Buttons */}
      <footer className="p-8 pb-12">
        <div className="flex items-center justify-center gap-8">
          {/* Pass Button */}
          <button
            onClick={() => handleSwipe("left")}
            className="w-16 h-16 rounded-full bg-[var(--surface)] shadow-xl flex items-center justify-center border-4 border-red-50 text-red-500 hover:scale-110 active:scale-95 transition-all"
            aria-label="Pass"
          >
            <span className="material-symbols-outlined text-3xl font-bold">close</span>
          </button>

          {/* Save Button */}
          <button
            onClick={() => handleSwipe("right")}
            className="w-20 h-20 rounded-full bg-[var(--primary)] shadow-xl flex items-center justify-center text-[var(--background-dark)] hover:scale-110 active:scale-95 transition-all"
            aria-label="Save"
          >
            <span className="material-symbols-outlined text-4xl" style={{ fontVariationSettings: "'FILL' 1" }}>favorite</span>
          </button>

          {/* Info Button */}
          <button
            onClick={() => window.open(curriculum?.website, "_blank")}
            className="w-16 h-16 rounded-full bg-[var(--surface)] shadow-xl flex items-center justify-center border-4 border-blue-50 text-blue-500 hover:scale-110 active:scale-95 transition-all"
            aria-label="More Info"
          >
            <span className="material-symbols-outlined text-3xl font-bold">info</span>
          </button>
        </div>
      </footer>

      {/* "Have you tried this?" Prompt Modal */}
      {showReviewPrompt && reviewCurriculum && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-[var(--surface)] rounded-2xl p-6 w-full max-w-sm animate-slide-up">
            <div className="text-center mb-6">
              <span className="material-symbols-outlined text-[var(--primary)] text-5xl mb-3 block">
                rate_review
              </span>
              <h3 className="text-xl font-bold text-[var(--foreground)] mb-2">
                Have you tried {reviewCurriculum.name}?
              </h3>
              <p className="text-[var(--foreground-secondary)] text-sm">
                Your review helps other homeschool families find the right fit.
              </p>
            </div>

            <div className="flex flex-col gap-3">
              <button
                onClick={() => handleReviewPromptResponse(true)}
                className="w-full py-4 bg-[var(--primary)] text-[var(--background-dark)] rounded-full font-bold flex items-center justify-center gap-2"
              >
                <span className="material-symbols-outlined">mic</span>
                Yes, leave a review
              </button>
              <button
                onClick={() => handleReviewPromptResponse(false)}
                className="w-full py-3 border border-[var(--border)] rounded-full font-medium text-[var(--foreground-secondary)]"
              >
                Not yet
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Voice Review Modal */}
      {showReviewModal && reviewCurriculum && (
        <VoiceReview
          curriculumName={reviewCurriculum.name}
          curriculumSlug={reviewCurriculum.slug}
          onSubmit={handleReviewSubmit}
          onCancel={() => {
            setShowReviewModal(false);
            setReviewCurriculum(null);
            advanceToNext();
          }}
        />
      )}
    </div>
  );
}
