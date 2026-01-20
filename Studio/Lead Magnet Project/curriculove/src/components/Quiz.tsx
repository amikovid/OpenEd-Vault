"use client";

import { useState, useEffect } from "react";
import type { PhilosophyScores, PhilosophyTag } from "@/lib/quiz-agent/scoring";
import UserButton from "./UserButton";

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

interface QuizProps {
  onComplete: (result: QuizResult) => void;
}

interface QuizState {
  sessionId: string | null;
  question: string;
  options: string[];
  questionNumber: number;
  isLoading: boolean;
  error: string | null;
}

export default function Quiz({ onComplete }: QuizProps) {
  const [state, setState] = useState<QuizState>({
    sessionId: null,
    question: "",
    options: [],
    questionNumber: 0,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    startQuiz();
  }, []);

  const startQuiz = async () => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));
      const res = await fetch("/api/quiz/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const data = await res.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setState({
        sessionId: data.sessionId,
        question: data.question,
        options: data.options,
        questionNumber: data.questionNumber,
        isLoading: false,
        error: null,
      });
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: String(err),
      }));
    }
  };

  const submitAnswer = async (optionIndex: number) => {
    if (!state.sessionId) return;

    try {
      setState((prev) => ({ ...prev, isLoading: true }));

      const res = await fetch("/api/quiz/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sessionId: state.sessionId,
          selectedOptionIndex: optionIndex,
          currentQuestion: {
            question: state.question,
            options: state.options,
          },
        }),
      });
      const data = await res.json();

      if (data.error) {
        throw new Error(data.error);
      }

      if (data.isComplete) {
        onComplete(data.result);
      } else {
        setState((prev) => ({
          ...prev,
          question: data.question,
          options: data.options,
          questionNumber: data.questionNumber,
          isLoading: false,
        }));
      }
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: String(err),
      }));
    }
  };

  if (state.error) {
    return (
      <div className="mobile-container flex flex-col items-center justify-center p-6">
        <div className="card p-8 text-center w-full">
          <span className="material-symbols-outlined text-[var(--error)] text-5xl mb-4">
            error
          </span>
          <p className="text-[var(--error)] mb-6">{state.error}</p>
          <button
            onClick={startQuiz}
            className="px-6 py-3 bg-[var(--primary)] text-[var(--background-dark)] font-semibold rounded-full hover:bg-[var(--primary-hover)] transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="mobile-container flex flex-col min-h-[100dvh]">
      {/* Header */}
      <div className="p-6 pb-0">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-xl font-bold text-[var(--foreground)]">
              Curriculove
            </h1>
            <p className="text-sm text-[var(--foreground-muted)]">
              Find your homeschool style
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="chip">
              <span className="material-symbols-outlined text-base mr-1">quiz</span>
              Q{state.questionNumber}
            </span>
            <UserButton />
          </div>
        </div>

        {/* Progress bar */}
        <div className="mb-8">
          <div className="flex justify-between text-xs text-[var(--foreground-muted)] mb-2">
            <span>Progress</span>
            <span>{Math.min(state.questionNumber * 12, 100)}%</span>
          </div>
          <div className="h-2 bg-[var(--surface-secondary)] rounded-full overflow-hidden">
            <div
              className="h-full bg-[var(--primary)] transition-all duration-500 ease-out rounded-full"
              style={{ width: `${Math.min(state.questionNumber * 12, 100)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Question card */}
      <div className="flex-1 px-6 pb-6">
        <div className="card-elevated p-6 mb-6 animate-slide-up">
          <h2 className="text-lg font-semibold leading-relaxed text-[var(--foreground)]">
            {state.question || "Loading your first question..."}
          </h2>
        </div>

        {/* Options */}
        <div className="space-y-3">
          {state.options.map((option, index) => (
            <button
              key={index}
              onClick={() => submitAnswer(index)}
              disabled={state.isLoading}
              className={`w-full p-4 text-left rounded-2xl border-2 transition-all duration-200 ${
                state.isLoading
                  ? "border-[var(--border-light)] bg-[var(--surface-secondary)] text-[var(--foreground-muted)] cursor-not-allowed opacity-60"
                  : "border-[var(--border)] bg-[var(--surface)] text-[var(--foreground)] hover:border-[var(--primary)] hover:bg-[var(--primary-light)] active:scale-[0.98]"
              }`}
            >
              <div className="flex items-center gap-3">
                <span
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    state.isLoading
                      ? "bg-[var(--border-light)] text-[var(--foreground-muted)]"
                      : "bg-[var(--surface-secondary)] text-[var(--foreground-secondary)]"
                  }`}
                >
                  {String.fromCharCode(65 + index)}
                </span>
                <span className="flex-1 font-medium">{option}</span>
              </div>
            </button>
          ))}
        </div>

        {/* Loading indicator */}
        {state.isLoading && (
          <div className="flex items-center justify-center gap-2 mt-6 text-[var(--foreground-muted)]">
            <div className="flex gap-1">
              <span
                className="w-2 h-2 bg-[var(--primary)] rounded-full animate-bounce"
                style={{ animationDelay: "0ms" }}
              />
              <span
                className="w-2 h-2 bg-[var(--primary)] rounded-full animate-bounce"
                style={{ animationDelay: "150ms" }}
              />
              <span
                className="w-2 h-2 bg-[var(--primary)] rounded-full animate-bounce"
                style={{ animationDelay: "300ms" }}
              />
            </div>
            <span className="text-sm">Analyzing...</span>
          </div>
        )}
      </div>
    </div>
  );
}
