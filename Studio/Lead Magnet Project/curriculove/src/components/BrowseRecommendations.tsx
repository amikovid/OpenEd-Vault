"use client";

import { useState, useEffect } from "react";
import VoiceReview from "./VoiceReview";
import UserButton from "./UserButton";
import curricula from "@/data/curricula-convex.json";
import { Curriculum, PHILOSOPHY_SHORT, getInsightData } from "@/lib/types";

interface PolishedReview {
  curriculumSlug: string;
  rawTranscript: string;
  polishedReview: string;
  rating: number;
  highlights: string[];
  concerns: string[];
  bestFor: string[];
}

interface BrowseRecommendationsProps {
  onAddFavorite: (slug: string) => void;
  favorites: string[];
}

function truncateToSentence(text: string, maxLength = 120): string {
  if (!text) return "";
  const firstSentence = text.match(/^[^.!?]+[.!?]/);
  if (firstSentence && firstSentence[0].length <= maxLength) {
    return firstSentence[0];
  }
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + "...";
}

function getPlaceholderImage(name: string): string {
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

export default function BrowseRecommendations({
  onAddFavorite,
  favorites,
}: BrowseRecommendationsProps) {
  const [allCurricula] = useState<Curriculum[]>(curricula as Curriculum[]);

  // Search and filter state
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedPhilosophy, setSelectedPhilosophy] = useState<string>("all");
  const [selectedPriceTier, setSelectedPriceTier] = useState<string>("all");
  const [selectedGradeRange, setSelectedGradeRange] = useState<string>("all");
  const [openEdOnly, setOpenEdOnly] = useState(false);
  const [sortBy, setSortBy] = useState<string>("name");
  const [viewMode, setViewMode] = useState<"swipe" | "list">("list");
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  // Grade range options
  const gradeRanges = [
    { value: "all", label: "All Grades" },
    { value: "prek", label: "PreK" },
    { value: "k-5", label: "K-5th" },
    { value: "6-8", label: "6th-8th" },
    { value: "9-12", label: "9th-12th" },
  ];

  // Check if curriculum matches grade range filter
  const matchesGrade = (gradeRange: string, filter: string): boolean => {
    if (filter === "all") return true;
    const gr = gradeRange.toLowerCase();
    if (filter === "prek") return gr.includes("prek") || gr.includes("pre-k");
    if (filter === "k-5") return gr.includes("k") || gr.includes("1") || gr.includes("2") || gr.includes("3") || gr.includes("4") || gr.includes("5");
    if (filter === "6-8") return gr.includes("6") || gr.includes("7") || gr.includes("8") || gr.includes("middle");
    if (filter === "9-12") return gr.includes("9") || gr.includes("10") || gr.includes("11") || gr.includes("12") || gr.includes("high");
    return true;
  };

  // Filter curricula based on search and filters
  const filteredCurricula = allCurricula
    .filter(curriculum => {
      const matchesSearch = searchQuery === "" ||
        curriculum.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        curriculum.description.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesPhilosophy = selectedPhilosophy === "all" ||
        curriculum.philosophyTags.includes(selectedPhilosophy);

      const matchesPriceTier = selectedPriceTier === "all" ||
        curriculum.priceTier === selectedPriceTier;

      const matchesGradeRange = matchesGrade(curriculum.gradeRange || "", selectedGradeRange);

      const matchesOpenEd = !openEdOnly || curriculum.isOpenEdVendor;

      return matchesSearch && matchesPhilosophy && matchesPriceTier && matchesGradeRange && matchesOpenEd;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case "name":
          return a.name.localeCompare(b.name);
        case "name-desc":
          return b.name.localeCompare(a.name);
        case "price-low":
          const priceOrder = { "$": 1, "$$": 2, "$$$": 3, "$$$$": 4, "": 5 };
          return (priceOrder[a.priceTier as keyof typeof priceOrder] || 5) - (priceOrder[b.priceTier as keyof typeof priceOrder] || 5);
        case "price-high":
          const priceOrderDesc = { "$": 1, "$$": 2, "$$$": 3, "$$$$": 4, "": 5 };
          return (priceOrderDesc[b.priceTier as keyof typeof priceOrderDesc] || 5) - (priceOrderDesc[a.priceTier as keyof typeof priceOrderDesc] || 5);
        case "vendor":
          return (b.isOpenEdVendor ? 1 : 0) - (a.isOpenEdVendor ? 1 : 0);
        default:
          return 0;
      }
    });

  const [currentIndex, setCurrentIndex] = useState(0);
  const [swipeDirection, setSwipeDirection] = useState<"left" | "right" | null>(null);

  // Review modal state
  const [showReviewPrompt, setShowReviewPrompt] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [reviewCurriculum, setReviewCurriculum] = useState<Curriculum | null>(null);

  // Convex mutations (disabled until configured)
  // const submitReview = useMutation(api.reviews.submitReview);
  // const addFavorite = useMutation(api.users.addFavorite);

  const handleSwipe = async (direction: "left" | "right") => {
    const current = filteredCurricula[currentIndex];

    setSwipeDirection(direction);

    if (direction === "right" && current) {
      onAddFavorite(current.slug);

      // Save to Convex if logged in (disabled until Convex configured)
      // Favorites are stored locally for now
      console.log("Favorite added locally:", current.slug);

      setReviewCurriculum(current);
      setShowReviewPrompt(true);
      setTimeout(() => setSwipeDirection(null), 250);
      return;
    }

    setTimeout(() => {
      setSwipeDirection(null);
      advanceToNext();
    }, 250);
  };

  const handleReviewPromptResponse = (hasTriedIt: boolean) => {
    setShowReviewPrompt(false);
    if (hasTriedIt && reviewCurriculum) {
      setShowReviewModal(true);
    } else {
      advanceToNext();
    }
  };

  const handleReviewSubmit = async (review: PolishedReview) => {
    setShowReviewModal(false);

    // Convex storage disabled - reviews stored locally for now
    console.log("Review collected (Convex disabled):", review.curriculumSlug);

    setReviewCurriculum(null);
    advanceToNext();
  };

  const advanceToNext = () => {
    if (currentIndex < filteredCurricula.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      // Loop back to start
      setCurrentIndex(0);
    }
  };

  // Reset current index when filters change
  useEffect(() => {
    setCurrentIndex(0);
  }, [searchQuery, selectedPhilosophy, selectedPriceTier, selectedGradeRange, openEdOnly, sortBy]);

  const current = filteredCurricula[currentIndex];

  if (!current) {
    return (
      <div className="mobile-container flex flex-col items-center justify-center min-h-[100dvh] p-6 bg-[var(--surface)]">
        <p className="text-[var(--foreground)]">No curricula found</p>
      </div>
    );
  }

  const heroImage = current.imageUrl || current.logoUrl || getPlaceholderImage(current.name);

  return (
    <div className="mobile-container flex flex-col min-h-[100dvh] bg-[var(--background)]">
      {/* Header */}
      <header className="flex items-center p-4 pb-2 justify-between sticky top-0 bg-[var(--background)]/80 backdrop-blur-md z-10">
        <a href="/" className="w-12">
          <span className="material-symbols-outlined text-2xl text-[var(--foreground)]">arrow_back</span>
        </a>
        <h2 className="text-lg font-bold text-[var(--foreground)]">Browse All</h2>
        <div className="w-12 flex items-center justify-end gap-2">
          <span className="text-[var(--primary)] font-bold text-sm">{favorites.length}</span>
          <UserButton />
        </div>
      </header>

      {/* Search and Filters */}
      <div className="px-4 py-3 space-y-3 bg-[var(--background)]">
        {/* Search Bar */}
        <div className="relative">
          <input
            type="text"
            placeholder="Search curricula..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-3 pl-10 bg-[var(--surface)] border border-[var(--border)] rounded-xl text-[var(--foreground)] placeholder-[var(--foreground-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
          />
          <span className="material-symbols-outlined absolute left-3 top-3.5 text-[var(--foreground-muted)]">search</span>
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-3 top-3.5 text-[var(--foreground-muted)] hover:text-[var(--foreground)]"
            >
              <span className="material-symbols-outlined text-xl">close</span>
            </button>
          )}
        </div>

        {/* Filter Row 1: Philosophy + Grade */}
        <div className="flex gap-2">
          <select
            value={selectedPhilosophy}
            onChange={(e) => setSelectedPhilosophy(e.target.value)}
            className="flex-1 px-3 py-2 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-[var(--foreground)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
          >
            <option value="all">All Philosophies</option>
            {Object.entries(PHILOSOPHY_SHORT).map(([tag, name]) => (
              <option key={tag} value={tag}>{name}</option>
            ))}
          </select>

          <select
            value={selectedGradeRange}
            onChange={(e) => setSelectedGradeRange(e.target.value)}
            className="flex-1 px-3 py-2 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-[var(--foreground)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
          >
            {gradeRanges.map(({ value, label }) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </div>

        {/* Filter Row 2: Price + Sort */}
        <div className="flex gap-2">
          <select
            value={selectedPriceTier}
            onChange={(e) => setSelectedPriceTier(e.target.value)}
            className="flex-1 px-3 py-2 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-[var(--foreground)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
          >
            <option value="all">All Prices</option>
            <option value="$">$ Budget</option>
            <option value="$$">$$ Mid-range</option>
            <option value="$$$">$$$ Premium</option>
            <option value="$$$$">$$$$ Luxury</option>
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="flex-1 px-3 py-2 bg-[var(--surface)] border border-[var(--border)] rounded-lg text-[var(--foreground)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
          >
            <option value="name">Sort: A-Z</option>
            <option value="name-desc">Sort: Z-A</option>
            <option value="price-low">Price: Low-High</option>
            <option value="price-high">Price: High-Low</option>
            <option value="vendor">OpenEd Partners First</option>
          </select>
        </div>

        {/* Toggle Row: OpenEd Only + View Mode */}
        <div className="flex items-center justify-between">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={openEdOnly}
              onChange={(e) => setOpenEdOnly(e.target.checked)}
              className="w-4 h-4 accent-[var(--primary)]"
            />
            <span className="text-sm text-[var(--foreground-secondary)]">
              OpenEd Partners Only ({allCurricula.filter(c => c.isOpenEdVendor).length})
            </span>
          </label>

          <div className="flex gap-1 bg-[var(--surface)] border border-[var(--border)] rounded-lg p-1">
            <button
              onClick={() => setViewMode("list")}
              className={`p-1.5 rounded transition-colors ${viewMode === "list" ? "bg-[var(--primary)] text-white" : "text-[var(--foreground-muted)]"}`}
              title="List view"
            >
              <span className="material-symbols-outlined text-lg">list</span>
            </button>
            <button
              onClick={() => setViewMode("swipe")}
              className={`p-1.5 rounded transition-colors ${viewMode === "swipe" ? "bg-[var(--primary)] text-white" : "text-[var(--foreground-muted)]"}`}
              title="Swipe view"
            >
              <span className="material-symbols-outlined text-lg">swipe</span>
            </button>
          </div>
        </div>

        {/* Results Count */}
        <p className="text-[var(--foreground-secondary)] text-xs">
          {filteredCurricula.length} of {allCurricula.length} curricula
          {searchQuery && ` matching "${searchQuery}"`}
        </p>
      </div>

      {viewMode === "swipe" && (
        <>
          {/* Progress */}
          <div className="px-6 py-2">
            <div className="flex justify-between items-center">
              <p className="text-[var(--foreground)] text-sm font-medium">Explore Curricula</p>
              <p className="text-[var(--primary)] text-xs font-semibold">
                {currentIndex + 1} of {filteredCurricula.length}
              </p>
            </div>
            <div className="h-1.5 w-full bg-[var(--border)] rounded-full overflow-hidden mt-2">
              <div
                className="h-full bg-[var(--primary)] rounded-full transition-all duration-500"
                style={{ width: `${((currentIndex + 1) / filteredCurricula.length) * 100}%` }}
              />
            </div>
          </div>

      {/* Card */}
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
          {/* Hero Image */}
          <div
            className="relative w-full aspect-[4/5] bg-center bg-no-repeat bg-cover"
            style={{ backgroundImage: `url("${heroImage}")` }}
          >
            {current.isOpenEdVendor && (
              <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm text-[var(--background-dark)] text-xs font-semibold px-2 py-1 rounded-full flex items-center gap-1">
                <span className="material-symbols-outlined text-sm">verified</span>
                OpenEd Partner
              </div>
            )}

            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />

            <div className="absolute bottom-4 left-4 right-4 text-white">
              <h1 className="text-3xl font-bold leading-tight">{current.name}</h1>
              {current.description && (
                <p className="text-white/90 text-sm font-medium italic mt-1">
                  {truncateToSentence(current.description, 80)}
                </p>
              )}
            </div>
          </div>

          {/* Details */}
          <div className="p-5 flex flex-col gap-4">
            <div className="flex gap-2 flex-wrap">
              {current.priceTier && (
                <div className="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-[var(--primary)]/20 px-3 border border-[var(--primary)]/20">
                  <span className="material-symbols-outlined text-sm text-[var(--foreground)]">payments</span>
                  <p className="text-[var(--foreground)] text-xs font-bold">{current.priceTier}</p>
                </div>
              )}
              {current.gradeRange && (
                <div className="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-[var(--background)] px-3 border border-[var(--border)]">
                  <span className="material-symbols-outlined text-sm text-[var(--foreground-muted)]">school</span>
                  <p className="text-[var(--foreground-secondary)] text-xs font-bold">{current.gradeRange}</p>
                </div>
              )}
              {current.philosophyTags.slice(0, 2).map((tag) => (
                <div key={tag} className="flex h-7 shrink-0 items-center justify-center gap-x-1 rounded-full bg-[var(--background)] px-3 border border-[var(--border)]">
                  <span className="material-symbols-outlined text-sm text-[var(--foreground-muted)]">psychology</span>
                  <p className="text-[var(--foreground-secondary)] text-xs font-bold">{PHILOSOPHY_SHORT[tag] || tag}</p>
                </div>
              ))}
            </div>

            {current.openedInsight && (() => {
              const insight = getInsightData(current.openedInsight);
              if (!insight.synthesis && !insight.quote) return null;
              return (
                <div className="flex flex-col items-start gap-3 rounded-lg border border-[var(--border)] bg-[var(--background)] p-4">
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
                      href={`https://opened.co/tool/${current.slug}`}
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

      {/* Action Buttons */}
      <footer className="p-8 pb-12">
        <div className="flex items-center justify-center gap-8">
          <button
            onClick={() => handleSwipe("left")}
            className="w-16 h-16 rounded-full bg-[var(--surface)] shadow-xl flex items-center justify-center border-4 border-red-50 text-red-500 hover:scale-110 active:scale-95 transition-all"
            aria-label="Pass"
          >
            <span className="material-symbols-outlined text-3xl font-bold">close</span>
          </button>

          <button
            onClick={() => handleSwipe("right")}
            className="w-20 h-20 rounded-full bg-[var(--primary)] shadow-xl flex items-center justify-center text-[var(--background-dark)] hover:scale-110 active:scale-95 transition-all"
            aria-label="Save"
          >
            <span className="material-symbols-outlined text-4xl" style={{ fontVariationSettings: "'FILL' 1" }}>favorite</span>
          </button>

          <button
            onClick={() => window.open(current.website, "_blank")}
            className="w-16 h-16 rounded-full bg-[var(--surface)] shadow-xl flex items-center justify-center border-4 border-blue-50 text-blue-500 hover:scale-110 active:scale-95 transition-all"
            aria-label="More Info"
          >
            <span className="material-symbols-outlined text-3xl font-bold">info</span>
          </button>
        </div>
      </footer>
        </>
      )}

      {/* List View */}
      {viewMode === "list" && (
        <div className="px-4 pb-20 space-y-3 overflow-y-auto">
          {filteredCurricula.map((curriculum) => {
            const isExpanded = expandedCard === curriculum.slug;
            const isFavorite = favorites.includes(curriculum.slug);

            return (
              <div
                key={curriculum.slug}
                className="bg-[var(--surface)] rounded-xl border border-[var(--border)] overflow-hidden"
              >
                {/* Collapsed View */}
                <div
                  onClick={() => setExpandedCard(isExpanded ? null : curriculum.slug)}
                  className="p-4 cursor-pointer hover:bg-[var(--background)] transition-colors"
                >
                  <div className="flex items-start gap-3">
                    <div className="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 bg-[var(--background)]">
                      <img
                        src={curriculum.logoUrl || getPlaceholderImage(curriculum.name)}
                        alt={curriculum.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-[var(--foreground)] mb-1">{curriculum.name}</h3>
                      <p className="text-xs text-[var(--foreground-secondary)] mb-2 line-clamp-2">
                        {curriculum.description}
                      </p>
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-xs font-bold text-[var(--primary)]">{curriculum.priceTier}</span>
                        <span className="text-xs text-[var(--foreground-muted)]">•</span>
                        <span className="text-xs text-[var(--foreground-muted)]">{curriculum.gradeRange}</span>
                        {curriculum.philosophyTags.slice(0, 2).map((tag) => (
                          <span key={tag} className="text-xs px-2 py-0.5 bg-[var(--background)] border border-[var(--border)] rounded-full">
                            {PHILOSOPHY_SHORT[tag] || tag}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="flex flex-col gap-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          if (isFavorite) {
                            // Remove from favorites (you might want to add this handler)
                          } else {
                            onAddFavorite(curriculum.slug);
                          }
                        }}
                        className={`p-2 rounded-full transition-colors ${
                          isFavorite
                            ? "bg-[var(--primary)] text-white"
                            : "bg-[var(--background)] border border-[var(--border)] text-[var(--foreground-muted)]"
                        }`}
                      >
                        <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: isFavorite ? "'FILL' 1" : "'FILL' 0" }}>
                          favorite
                        </span>
                      </button>
                      <span className="material-symbols-outlined text-[var(--foreground-muted)]">
                        {isExpanded ? "expand_less" : "expand_more"}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Expanded View */}
                {isExpanded && (
                  <div className="px-4 pb-4 space-y-3 border-t border-[var(--border)] pt-4">
                    <p className="text-sm text-[var(--foreground-secondary)] leading-relaxed">
                      {curriculum.description}
                    </p>

                    {curriculum.openedInsight && (() => {
                      const insight = getInsightData(curriculum.openedInsight);
                      if (!insight.synthesis && !insight.quote) return null;
                      return (
                        <div className="rounded-lg border border-[var(--border)] bg-[var(--background)] p-3">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="material-symbols-outlined text-[var(--primary)] text-lg">verified</span>
                            <p className="text-[var(--foreground)] text-sm font-bold">OpenEd Insight</p>
                          </div>
                          {insight.quote && (
                            <p className="text-[var(--foreground)] text-sm italic mb-2">
                              &ldquo;{insight.quote}&rdquo;
                              {insight.attribution && (
                                <span className="text-[var(--foreground-muted)] not-italic"> - {insight.attribution}</span>
                              )}
                            </p>
                          )}
                          {insight.synthesis && (
                            <p className="text-[var(--foreground-muted)] text-xs leading-normal">
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

                    <div className="flex gap-2">
                      <a
                        href={curriculum.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex-1 py-2 px-4 bg-[var(--primary)] text-white rounded-full text-sm font-bold text-center hover:opacity-90 transition-opacity"
                      >
                        Visit Website
                      </a>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Review Prompt Modal */}
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
