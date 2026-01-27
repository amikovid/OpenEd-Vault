"use client";

import { useState, useEffect } from "react";
import Quiz from "@/components/Quiz";
import Results from "@/components/Results";
import EmailGate from "@/components/EmailGate";
import Recommendations from "@/components/Recommendations";
import BrowseRecommendations from "@/components/BrowseRecommendations";
import BottomNav from "@/components/BottomNav";
import SavesList from "@/components/SavesList";
import Completion from "@/components/Completion";
import type { PhilosophyScores, PhilosophyTag } from "@/lib/quiz-agent/scoring";

type Phase = "quiz" | "results" | "email" | "recommendations" | "completion" | "browse";
type Tab = "discover" | "saves" | "profile";

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

interface SavedCurriculum {
  slug: string;
  name: string;
  matchScore: number;
  reason: string;
  curriculum: {
    name: string;
    slug: string;
    description: string;
    pricingSummary: string;
    priceTier: string;
    website: string;
    gradeRange: string;
    philosophyTags: string[];
    openedInsight: string;
    logoUrl: string | null;
    imageUrl: string | null;
    isOpenEdVendor: boolean;
    prepTimeScore?: number;
    teacherInvolvementLevel?: string;
  } | null;
}

export default function Home() {
  const [phase, setPhase] = useState<Phase>("quiz");
  const [activeTab, setActiveTab] = useState<Tab>("discover");
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);
  const [favorites, setFavorites] = useState<string[]>([]);
  const [savedItems, setSavedItems] = useState<SavedCurriculum[]>([]);

  // Track recommendations data for saving full curriculum info
  const [recommendationsData, setRecommendationsData] = useState<SavedCurriculum[]>([]);

  // Store captured user email for associating with reviews
  const [userEmail, setUserEmail] = useState<string | null>(null);

  const handleQuizComplete = (result: QuizResult) => {
    setQuizResult(result);
    // Go to email gate first (before showing results)
    setPhase("email");
  };

  const handleEmailSubmit = (email: string, state?: string) => {
    console.log("Email captured:", email, "State:", state, "Philosophy:", quizResult?.primary.tag);
    // Store email for associating with reviews later
    setUserEmail(email);
    // After email, show results
    setPhase("results");
  };

  const handleEmailSkip = () => {
    // Skip email, go directly to results
    setPhase("results");
  };

  const handleResultsContinue = () => {
    // After results, go to recommendations
    setPhase("recommendations");
  };

  const handleAddFavorite = (slug: string) => {
    if (!favorites.includes(slug)) {
      setFavorites((prev) => [...prev, slug]);

      // Find the full item data from recommendations
      const item = recommendationsData.find((r) => r.slug === slug);
      if (item) {
        setSavedItems((prev) => [...prev, item]);
      }
    }
  };

  const handleRemoveFavorite = (slug: string) => {
    setFavorites((prev) => prev.filter((f) => f !== slug));
    setSavedItems((prev) => prev.filter((item) => item.slug !== slug));
  };

  const handleRestart = () => {
    setPhase("quiz");
    setActiveTab("discover");
    setQuizResult(null);
    setFavorites([]);
    setSavedItems([]);
    setRecommendationsData([]);
  };

  const handleRecommendationsFinish = () => {
    setPhase("completion");
  };

  const handleViewSaves = () => {
    setPhase("browse");
    setActiveTab("saves");
  };

  const handleBrowseAll = () => {
    setPhase("browse");
    setActiveTab("discover");
  };

  const handleTabChange = (tab: Tab) => {
    setActiveTab(tab);
    // Stay in browse phase when switching tabs - don't restart recommendations
  };

  // Show bottom nav only in browse mode or after completion
  const showBottomNav = phase === "browse" || phase === "completion";

  return (
    <main className="min-h-[100dvh] bg-[var(--background)]">
      {/* Quiz Phase */}
      {phase === "quiz" && <Quiz onComplete={handleQuizComplete} />}

      {/* Results Phase */}
      {phase === "results" && quizResult && (
        <Results result={quizResult} onContinue={handleResultsContinue} />
      )}

      {/* Email Gate Phase */}
      {phase === "email" && quizResult && (
        <EmailGate
          primaryPhilosophy={quizResult.primary.tag}
          primaryPhilosophyName={quizResult.primary.name}
          secondaryPhilosophies={quizResult.secondary.map((s) => s.tag)}
          confidence={quizResult.confidence}
          onSubmit={handleEmailSubmit}
          onSkip={handleEmailSkip}
        />
      )}

      {/* Recommendations Phase */}
      {phase === "recommendations" && quizResult && (
        <RecommendationsWithDataCapture
          quizResult={quizResult}
          onAddFavorite={handleAddFavorite}
          favorites={favorites}
          onFinish={handleRecommendationsFinish}
          onDataLoad={setRecommendationsData}
          userEmail={userEmail}
        />
      )}

      {/* Completion Phase */}
      {phase === "completion" && quizResult && (
        <Completion
          savesCount={favorites.length}
          philosophyName={quizResult.primary.name}
          onViewSaves={handleViewSaves}
          onStartOver={handleRestart}
          onBrowseAll={handleBrowseAll}
        />
      )}

      {/* Browse Phase with Tabs */}
      {phase === "browse" && (
        <>
          {activeTab === "discover" && (
            <BrowseRecommendations
              onAddFavorite={handleAddFavorite}
              favorites={favorites}
              userEmail={userEmail}
            />
          )}

          {activeTab === "saves" && (
            <SavesList
              items={savedItems}
              onRemove={handleRemoveFavorite}
              onBack={() => {
                setActiveTab("discover");
                setPhase("recommendations");
              }}
            />
          )}

          {activeTab === "profile" && (
            <ProfileView
              quizResult={quizResult}
              onRestart={handleRestart}
            />
          )}
        </>
      )}

      {/* Bottom Navigation */}
      {showBottomNav && (
        <BottomNav
          activeTab={activeTab}
          onTabChange={handleTabChange}
          savesCount={favorites.length}
        />
      )}
    </main>
  );
}

// Wrapper component to capture recommendations data
function RecommendationsWithDataCapture({
  quizResult,
  onAddFavorite,
  favorites,
  onFinish,
  onDataLoad,
  userEmail,
}: {
  quizResult: QuizResult;
  onAddFavorite: (slug: string) => void;
  favorites: string[];
  onFinish: () => void;
  onDataLoad: (data: SavedCurriculum[]) => void;
  userEmail: string | null;
}) {
  const [recommendations, setRecommendations] = useState<SavedCurriculum[] | null>(null);

  // Fetch recommendations data once and pass to child
  useEffect(() => {
    if (!recommendations) {
      fetch("/api/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          primaryPhilosophy: quizResult.primary.tag,
          secondaryPhilosophies: quizResult.secondary.map((s) => s.tag),
          confidence: quizResult.confidence,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.recommendations) {
            setRecommendations(data.recommendations);
            onDataLoad(data.recommendations);
          }
        })
        .catch(console.error);
    }
  }, [quizResult, recommendations, onDataLoad]);

  return (
    <Recommendations
      quizResult={quizResult}
      onAddFavorite={onAddFavorite}
      favorites={favorites}
      onFinish={onFinish}
      initialRecommendations={recommendations || undefined}
      userEmail={userEmail}
    />
  );
}

// Simple Profile View
function ProfileView({
  quizResult,
  onRestart,
}: {
  quizResult: QuizResult | null;
  onRestart: () => void;
}) {
  return (
    <div className="mobile-container flex flex-col min-h-[100dvh] pb-20">
      <div className="p-6">
        <h1 className="text-xl font-bold text-[var(--foreground)] mb-1">
          Profile
        </h1>
        <p className="text-sm text-[var(--foreground-muted)]">
          Your homeschool profile
        </p>
      </div>

      <div className="flex-1 px-6">
        {quizResult && (
          <div className="card-elevated p-6 mb-6">
            <div className="text-center">
              <span className="chip-primary mb-3 inline-block">
                Your Style
              </span>
              <h2 className="text-2xl font-bold text-[var(--foreground)] mb-2">
                {quizResult.primary.name}
              </h2>
              <p className="text-[var(--foreground-secondary)] text-sm">
                {quizResult.primary.description}
              </p>
            </div>
          </div>
        )}

        <div className="card p-5 mb-6">
          <h3 className="text-sm font-semibold text-[var(--foreground-muted)] uppercase tracking-wide mb-4">
            Actions
          </h3>
          <button
            onClick={onRestart}
            className="w-full py-3 border-2 border-[var(--border)] text-[var(--foreground)] rounded-xl font-semibold flex items-center justify-center gap-2"
          >
            <span className="material-symbols-outlined">refresh</span>
            Retake Quiz
          </button>
        </div>

        <div className="card p-5">
          <h3 className="text-sm font-semibold text-[var(--foreground-muted)] uppercase tracking-wide mb-4">
            Coming Soon
          </h3>
          <div className="space-y-3 text-sm text-[var(--foreground-secondary)]">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-[var(--foreground-muted)]">
                mail
              </span>
              <span>Save your matches via email</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-[var(--foreground-muted)]">
                share
              </span>
              <span>Share your homeschool style</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-[var(--foreground-muted)]">
                compare
              </span>
              <span>Compare curricula side-by-side</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
