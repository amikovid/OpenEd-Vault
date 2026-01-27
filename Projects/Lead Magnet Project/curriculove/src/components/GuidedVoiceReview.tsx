"use client";

import { useState, useRef, useEffect } from "react";

// Web Speech API types
interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
  resultIndex: number;
}

interface SpeechRecognitionResultList {
  length: number;
  item(index: number): SpeechRecognitionResult;
  [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognitionResult {
  isFinal: boolean;
  length: number;
  item(index: number): SpeechRecognitionAlternative;
  [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionAlternative {
  transcript: string;
  confidence: number;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}

interface ISpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: SpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
}

declare global {
  interface Window {
    SpeechRecognition: new () => ISpeechRecognition;
    webkitSpeechRecognition: new () => ISpeechRecognition;
  }
}

interface GuidedVoiceReviewProps {
  curriculumName: string;
  curriculumSlug: string;
  onSubmit: (review: PolishedReview) => void;
  onCancel: () => void;
}

interface PolishedReview {
  curriculumSlug: string;
  rawTranscript: string;
  polishedReview: string;
  rating: number;
  highlights: string[];
  concerns: string[];
  bestFor: string[];
}

interface Question {
  id: string;
  prompt: string;
  icon: string;
  placeholder: string;
}

const REVIEW_QUESTIONS: Question[] = [
  {
    id: "highlights",
    prompt: "What did you like most about this curriculum?",
    icon: "thumb_up",
    placeholder: "The hands-on activities, the clear instructions, the engaging content...",
  },
  {
    id: "concerns",
    prompt: "Any challenges or things you'd improve?",
    icon: "lightbulb",
    placeholder: "Time commitment, prep work, cost, difficulty level...",
  },
  {
    id: "bestFor",
    prompt: "Who would this curriculum be best for?",
    icon: "group",
    placeholder: "Active learners, visual learners, families with multiple ages...",
  },
];

type RecordingState = "idle" | "recording" | "processing" | "editing" | "submitting";
type InputMode = "text" | "voice";

export default function GuidedVoiceReview({
  curriculumName,
  curriculumSlug,
  onSubmit,
  onCancel,
}: GuidedVoiceReviewProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [currentTranscript, setCurrentTranscript] = useState("");
  const [state, setState] = useState<RecordingState>("idle");
  const [polishedReview, setPolishedReview] = useState<PolishedReview | null>(null);
  const [editedReview, setEditedReview] = useState("");
  const [rating, setRating] = useState(4);
  const [error, setError] = useState<string | null>(null);
  const [isSupported, setIsSupported] = useState(true);
  const [inputMode, setInputMode] = useState<InputMode>("text");
  const [currentTextInput, setCurrentTextInput] = useState("");

  const recognitionRef = useRef<ISpeechRecognition | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        setIsSupported(false);
      }
    }
  }, []);

  const currentQuestion = REVIEW_QUESTIONS[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === REVIEW_QUESTIONS.length - 1;
  const allQuestionsAnswered = currentQuestionIndex >= REVIEW_QUESTIONS.length;

  const startRecording = () => {
    setError(null);
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    let finalTranscript = "";

    recognition.onresult = (event) => {
      let interimTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) {
          finalTranscript += result[0].transcript + " ";
        } else {
          interimTranscript += result[0].transcript;
        }
      }

      setCurrentTranscript(finalTranscript + interimTranscript);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      if (event.error === "not-allowed") {
        setError("Microphone access denied. Please allow microphone access and try again.");
      } else {
        setError(`Speech recognition error: ${event.error}`);
      }
      setState("idle");
    };

    recognition.onend = () => {
      if (state === "recording") {
        recognition.start();
      }
    };

    recognitionRef.current = recognition;
    recognition.start();
    setState("recording");
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }

    if (!currentTranscript.trim()) {
      setError("No speech detected. Please try again or type your answer.");
      setState("idle");
      setInputMode("text");
      return;
    }

    // Save answer for current question
    setAnswers((prev) => ({
      ...prev,
      [currentQuestion.id]: currentTranscript.trim(),
    }));

    setCurrentTranscript("");
    setState("idle");
    setInputMode("text"); // Reset to text mode for next question

    // Move to next question or finish
    if (isLastQuestion) {
      // All questions answered, process the review
      processAllAnswers({
        ...answers,
        [currentQuestion.id]: currentTranscript.trim(),
      });
    } else {
      setCurrentQuestionIndex((prev) => prev + 1);
    }
  };

  const processAllAnswers = async (allAnswers: Record<string, string>) => {
    setState("processing");

    // Combine all answers into a raw transcript
    const rawTranscript = `
Highlights: ${allAnswers.highlights || ""}
Concerns: ${allAnswers.concerns || ""}
Best for: ${allAnswers.bestFor || ""}
    `.trim();

    try {
      const res = await fetch("/api/polish-review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          rawTranscript,
          curriculumName,
          curriculumSlug,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to polish review");
      }

      const data = await res.json();
      setPolishedReview(data);
      setEditedReview(data.polishedReview);
      setRating(data.rating || 4);
      setState("editing");
    } catch (err) {
      console.error("Error polishing review:", err);
      setError("Failed to process your review. Please try again.");
      setState("idle");
      setCurrentQuestionIndex(0);
    }
  };

  const handleSubmit = () => {
    if (!polishedReview) return;

    setState("submitting");

    onSubmit({
      ...polishedReview,
      polishedReview: editedReview,
      rating,
    });
  };

  const skipQuestion = () => {
    setCurrentTranscript("");
    setCurrentTextInput("");
    if (isLastQuestion) {
      processAllAnswers(answers);
    } else {
      setCurrentQuestionIndex((prev) => prev + 1);
    }
  };

  const goBack = () => {
    if (currentQuestionIndex > 0) {
      const prevQuestionId = REVIEW_QUESTIONS[currentQuestionIndex - 1].id;
      setCurrentQuestionIndex((prev) => prev - 1);
      setCurrentTextInput(answers[prevQuestionId] || "");
      setCurrentTranscript(answers[prevQuestionId] || "");
      setInputMode("text");
    }
  };

  // Fallback text input
  if (!isSupported) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-end justify-center z-50">
        <div className="bg-[var(--surface)] w-full max-w-lg rounded-t-3xl p-6 pb-10 animate-slide-up max-h-[90vh] overflow-y-auto">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold text-[var(--foreground)]">
              Review {curriculumName}
            </h3>
            <button onClick={onCancel} className="text-[var(--foreground-muted)]">
              <span className="material-symbols-outlined">close</span>
            </button>
          </div>

          <p className="text-[var(--foreground-secondary)] text-sm mb-4">
            Voice input not supported. Please type your answers:
          </p>

          {REVIEW_QUESTIONS.map((q) => (
            <div key={q.id} className="mb-4">
              <label className="text-sm font-medium text-[var(--foreground)] mb-2 block">
                {q.prompt}
              </label>
              <textarea
                value={answers[q.id] || ""}
                onChange={(e) => setAnswers((prev) => ({ ...prev, [q.id]: e.target.value }))}
                placeholder={q.placeholder}
                className="w-full h-20 p-3 border border-[var(--border)] rounded-xl bg-[var(--background)] text-[var(--foreground)] resize-none text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
              />
            </div>
          ))}

          <div className="flex items-center gap-2 my-4">
            <span className="text-[var(--foreground-secondary)] text-sm">Rating:</span>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setRating(star)}
                  className={`text-2xl ${star <= rating ? "text-[var(--primary)]" : "text-[var(--border)]"}`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={() => {
              const hasContent = Object.values(answers).some((a) => a.trim());
              if (hasContent) {
                processAllAnswers(answers);
              }
            }}
            disabled={!Object.values(answers).some((a) => a.trim())}
            className="w-full py-4 bg-[var(--primary)] text-[var(--background-dark)] rounded-full font-bold disabled:opacity-50"
          >
            Generate Review
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-end justify-center z-50">
      <div className="bg-[var(--surface)] w-full max-w-lg rounded-t-3xl p-6 pb-10 animate-slide-up">
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-[var(--foreground)]">
            Review {curriculumName}
          </h3>
          <button onClick={onCancel} className="text-[var(--foreground-muted)]">
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        {/* Progress indicator */}
        {state !== "editing" && state !== "processing" && state !== "submitting" && (
          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-xs text-[var(--foreground-muted)]">
                Question {Math.min(currentQuestionIndex + 1, REVIEW_QUESTIONS.length)} of {REVIEW_QUESTIONS.length}
              </span>
              {currentQuestionIndex > 0 && (
                <button onClick={goBack} className="text-xs text-[var(--primary)] flex items-center gap-1">
                  <span className="material-symbols-outlined text-sm">arrow_back</span>
                  Back
                </button>
              )}
            </div>
            <div className="h-1.5 w-full bg-[var(--border)] rounded-full overflow-hidden">
              <div
                className="h-full bg-[var(--primary)] rounded-full transition-all duration-300"
                style={{ width: `${((currentQuestionIndex + 1) / REVIEW_QUESTIONS.length) * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Question Flow - Text Input (Default) */}
        {state === "idle" && !allQuestionsAnswered && currentQuestion && inputMode === "text" && (
          <div className="py-4">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-[var(--primary)]/10 flex items-center justify-center">
                <span className="material-symbols-outlined text-xl text-[var(--primary)]">{currentQuestion.icon}</span>
              </div>
              <h4 className="text-base font-semibold text-[var(--foreground)] flex-1">
                {currentQuestion.prompt}
              </h4>
            </div>

            <textarea
              value={currentTextInput}
              onChange={(e) => setCurrentTextInput(e.target.value)}
              placeholder={currentQuestion.placeholder}
              className="w-full h-24 p-4 border border-[var(--border)] rounded-xl bg-[var(--background)] text-[var(--foreground)] resize-none text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)] mb-4"
            />

            <div className="flex items-center gap-3">
              <button
                onClick={() => {
                  if (currentTextInput.trim()) {
                    setAnswers((prev) => ({
                      ...prev,
                      [currentQuestion.id]: currentTextInput.trim(),
                    }));
                    setCurrentTextInput("");
                    if (isLastQuestion) {
                      processAllAnswers({
                        ...answers,
                        [currentQuestion.id]: currentTextInput.trim(),
                      });
                    } else {
                      setCurrentQuestionIndex((prev) => prev + 1);
                    }
                  }
                }}
                disabled={!currentTextInput.trim()}
                className="flex-1 py-3 bg-[var(--primary)] text-[var(--background-dark)] rounded-full font-bold disabled:opacity-50"
              >
                {isLastQuestion ? "Generate Review" : "Next Question"}
              </button>

              {/* Voice option - only if supported */}
              {isSupported && (
                <button
                  onClick={() => {
                    setInputMode("voice");
                    startRecording();
                  }}
                  className="w-12 h-12 rounded-full bg-[var(--surface)] border border-[var(--border)] flex items-center justify-center text-[var(--foreground-muted)] hover:text-[var(--primary)] hover:border-[var(--primary)] transition-colors"
                  title="Use voice instead"
                >
                  <span className="material-symbols-outlined text-xl">mic</span>
                </button>
              )}
            </div>

            <button onClick={skipQuestion} className="w-full text-center text-[var(--foreground-muted)] text-xs underline mt-3">
              Skip this question
            </button>
          </div>
        )}

        {/* Question Flow - Voice Input */}
        {state === "idle" && !allQuestionsAnswered && currentQuestion && inputMode === "voice" && (
          <div className="text-center py-6">
            <div className="w-16 h-16 rounded-full bg-[var(--primary)]/10 flex items-center justify-center mx-auto mb-4">
              <span className="material-symbols-outlined text-3xl text-[var(--primary)]">{currentQuestion.icon}</span>
            </div>
            <h4 className="text-lg font-semibold text-[var(--foreground)] mb-2">
              {currentQuestion.prompt}
            </h4>
            <p className="text-[var(--foreground-muted)] text-sm mb-6">
              {currentQuestion.placeholder}
            </p>

            <button
              onClick={startRecording}
              className="w-20 h-20 rounded-full bg-[var(--primary)] text-[var(--background-dark)] flex items-center justify-center mx-auto hover:scale-105 transition-transform mb-4"
            >
              <span className="material-symbols-outlined text-4xl">mic</span>
            </button>

            <div className="flex flex-col items-center gap-3 mt-2">
              <button
                onClick={() => setInputMode("text")}
                className="text-[var(--primary)] text-sm font-medium flex items-center gap-1"
              >
                <span className="material-symbols-outlined text-sm">keyboard</span>
                Switch to typing
              </button>
              <button onClick={skipQuestion} className="text-[var(--foreground-muted)] text-xs underline">
                Skip this question
              </button>
            </div>
          </div>
        )}

        {/* Recording State */}
        {state === "recording" && (
          <div className="text-center py-4">
            <div className="w-20 h-20 rounded-full bg-red-500 text-white flex items-center justify-center mx-auto mb-4 animate-pulse">
              <span className="material-symbols-outlined text-4xl">mic</span>
            </div>
            <p className="text-[var(--foreground)] font-medium mb-1">Recording...</p>
            <p className="text-[var(--foreground-muted)] text-xs mb-3">Tap the stop button when you're done</p>

            <div className="bg-[var(--background)] rounded-lg p-4 mb-4 min-h-[80px] max-h-[150px] overflow-y-auto text-left">
              <p className="text-[var(--foreground-secondary)] text-sm">
                {currentTranscript || "Start speaking..."}
              </p>
            </div>

            <button
              onClick={stopRecording}
              className="w-full py-4 bg-red-500 text-white rounded-full font-bold flex items-center justify-center gap-2 hover:bg-red-600 transition-colors"
            >
              <span className="material-symbols-outlined">stop_circle</span>
              Stop Recording
            </button>

            <button
              onClick={() => {
                if (recognitionRef.current) {
                  recognitionRef.current.stop();
                  recognitionRef.current = null;
                }
                setState("idle");
                setInputMode("text");
                setCurrentTranscript("");
              }}
              className="text-[var(--foreground-muted)] text-xs underline mt-3"
            >
              Cancel and type instead
            </button>
          </div>
        )}

        {/* Processing State */}
        {state === "processing" && (
          <div className="text-center py-12">
            <div className="flex gap-1 justify-center mb-4">
              <span className="w-3 h-3 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-3 h-3 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-3 h-3 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
            <p className="text-[var(--foreground-secondary)]">Creating your review...</p>
          </div>
        )}

        {/* Editing State */}
        {state === "editing" && polishedReview && (
          <div>
            <p className="text-[var(--foreground-secondary)] text-sm mb-3">
              Here's your review. Feel free to edit:
            </p>

            <textarea
              value={editedReview}
              onChange={(e) => setEditedReview(e.target.value)}
              className="w-full h-32 p-4 border border-[var(--border)] rounded-xl bg-[var(--background)] text-[var(--foreground)] resize-none focus:outline-none focus:ring-2 focus:ring-[var(--primary)] mb-4"
            />

            {/* Rating */}
            <div className="flex items-center gap-2 mb-4">
              <span className="text-[var(--foreground-secondary)] text-sm">Rating:</span>
              <div className="flex gap-1">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    onClick={() => setRating(star)}
                    className={`text-2xl ${star <= rating ? "text-[var(--primary)]" : "text-[var(--border)]"}`}
                  >
                    ★
                  </button>
                ))}
              </div>
            </div>

            {/* Highlights & Concerns */}
            {(polishedReview.highlights.length > 0 || polishedReview.concerns.length > 0) && (
              <div className="flex flex-col gap-2 mb-4 text-xs">
                {polishedReview.highlights.length > 0 && (
                  <div className="flex items-start gap-2">
                    <span className="material-symbols-outlined text-[var(--success)] text-sm">thumb_up</span>
                    <span className="text-[var(--foreground-muted)]">
                      {polishedReview.highlights.join(", ")}
                    </span>
                  </div>
                )}
                {polishedReview.concerns.length > 0 && (
                  <div className="flex items-start gap-2">
                    <span className="material-symbols-outlined text-amber-500 text-sm">lightbulb</span>
                    <span className="text-[var(--foreground-muted)]">
                      {polishedReview.concerns.join(", ")}
                    </span>
                  </div>
                )}
                {polishedReview.bestFor.length > 0 && (
                  <div className="flex items-start gap-2">
                    <span className="material-symbols-outlined text-[var(--primary)] text-sm">group</span>
                    <span className="text-[var(--foreground-muted)]">
                      Best for: {polishedReview.bestFor.join(", ")}
                    </span>
                  </div>
                )}
              </div>
            )}

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setState("idle");
                  setCurrentQuestionIndex(0);
                  setAnswers({});
                  setPolishedReview(null);
                  setCurrentTextInput("");
                  setCurrentTranscript("");
                  setInputMode("text");
                }}
                className="flex-1 py-3 border border-[var(--border)] rounded-full font-medium text-[var(--foreground-secondary)]"
              >
                Start Over
              </button>
              <button
                onClick={handleSubmit}
                className="flex-1 py-3 bg-[var(--primary)] text-[var(--background-dark)] rounded-full font-bold"
              >
                Submit Review
              </button>
            </div>
          </div>
        )}

        {/* Submitting State */}
        {state === "submitting" && (
          <div className="text-center py-12">
            <div className="flex gap-1 justify-center mb-4">
              <span className="w-3 h-3 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-3 h-3 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-3 h-3 bg-[var(--primary)] rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
            <p className="text-[var(--foreground-secondary)]">Submitting your review...</p>
          </div>
        )}
      </div>
    </div>
  );
}
