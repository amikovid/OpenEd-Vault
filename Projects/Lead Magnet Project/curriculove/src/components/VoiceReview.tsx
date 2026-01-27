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

interface VoiceReviewProps {
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

type RecordingState = "idle" | "recording" | "processing" | "editing" | "submitting";

export default function VoiceReview({
  curriculumName,
  curriculumSlug,
  onSubmit,
  onCancel,
}: VoiceReviewProps) {
  const [state, setState] = useState<RecordingState>("idle");
  const [transcript, setTranscript] = useState("");
  const [polishedReview, setPolishedReview] = useState<PolishedReview | null>(null);
  const [editedReview, setEditedReview] = useState("");
  const [rating, setRating] = useState(4);
  const [error, setError] = useState<string | null>(null);

  const recognitionRef = useRef<ISpeechRecognition | null>(null);
  const isRecordingRef = useRef(false);
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    // Check for Web Speech API support
    if (typeof window !== "undefined") {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        setIsSupported(false);
        return;
      }

      // Arc browser has issues with Web Speech API - default to text input
      const isArc = navigator.userAgent.includes("Arc");
      if (isArc) {
        setIsSupported(false);
      }
    }
  }, []);

  useEffect(() => {
    return () => {
      isRecordingRef.current = false;
      if (recognitionRef.current) {
        recognitionRef.current.stop();
        recognitionRef.current = null;
      }
    };
  }, []);

  const startRecording = () => {
    setError(null);
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    let finalTranscript = "";
    setTranscript("");

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

      setTranscript(finalTranscript + interimTranscript);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      isRecordingRef.current = false;
      if (event.error === "not-allowed") {
        setError("Microphone access denied. Please allow microphone access and try again.");
        setState("idle");
      } else if (event.error === "network") {
        // Network error - auto-fallback to text input
        setError("Voice input unavailable. Please type your review instead.");
        setIsSupported(false);
      } else {
        setError(`Speech recognition error: ${event.error}`);
        setState("idle");
      }
    };

    recognition.onend = () => {
      if (isRecordingRef.current) {
        // Auto-restart if still in recording mode (browser may stop after silence)
        recognition.start();
      }
    };

    recognitionRef.current = recognition;
    isRecordingRef.current = true;
    recognition.start();
    setState("recording");
  };

  const stopRecording = async () => {
    isRecordingRef.current = false;
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }

    if (!transcript.trim()) {
      setError("No speech detected. Please try again.");
      setState("idle");
      return;
    }

    setState("processing");

    try {
      const res = await fetch("/api/polish-review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          rawTranscript: transcript,
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

  const handleCancel = () => {
    isRecordingRef.current = false;
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }
    setState("idle");
    onCancel();
  };

  // Fallback text input for unsupported browsers
  if (!isSupported) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-end justify-center z-50">
        <div className="bg-[var(--surface)] w-full max-w-lg rounded-t-3xl p-6 pb-10 animate-slide-up">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold text-[var(--foreground)]">
              Review {curriculumName}
            </h3>
            <button onClick={handleCancel} className="text-[var(--foreground-muted)]" aria-label="Close review">
              <span className="material-symbols-outlined">close</span>
            </button>
          </div>

          <p className="text-[var(--foreground-secondary)] text-sm mb-4">
            Voice input not supported in this browser. Please type your review:
          </p>

          <textarea
            value={editedReview}
            onChange={(e) => setEditedReview(e.target.value)}
            placeholder="Share your experience with this curriculum..."
            className="w-full h-32 p-4 border border-[var(--border)] rounded-xl bg-[var(--background)] text-[var(--foreground)] resize-none focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
            aria-label="Your review"
          />

          <div className="flex items-center gap-2 my-4">
            <span className="text-[var(--foreground-secondary)] text-sm">Rating:</span>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setRating(star)}
                  className={`text-2xl ${star <= rating ? "text-[var(--primary)]" : "text-[var(--border)]"}`}
                  aria-label={`Rate ${star} out of 5 stars`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={() => {
              if (editedReview.trim()) {
                onSubmit({
                  curriculumSlug,
                  rawTranscript: editedReview,
                  polishedReview: editedReview,
                  rating,
                  highlights: [],
                  concerns: [],
                  bestFor: [],
                });
              }
            }}
            disabled={!editedReview.trim()}
            className="w-full py-4 bg-[var(--primary)] text-[var(--background-dark)] rounded-full font-bold disabled:opacity-50"
          >
            Submit Review
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-end justify-center z-50">
      <div className="bg-[var(--surface)] w-full max-w-lg rounded-t-3xl p-6 pb-10 animate-slide-up">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-[var(--foreground)]">
            Review {curriculumName}
          </h3>
          <button onClick={handleCancel} className="text-[var(--foreground-muted)]">
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Idle State - Start Recording */}
        {state === "idle" && (
          <div className="text-center py-8">
            <p className="text-[var(--foreground-secondary)] mb-6">
              Tap the microphone and tell us about your experience with {curriculumName}
            </p>
            <button
              onClick={startRecording}
              className="w-24 h-24 rounded-full bg-[var(--primary)] text-[var(--background-dark)] flex items-center justify-center mx-auto hover:scale-105 transition-transform"
              aria-label="Start voice recording"
            >
              <span className="material-symbols-outlined text-5xl">mic</span>
            </button>
            <p className="text-[var(--foreground-muted)] text-xs mt-4">
              Or type your review below
            </p>
            <button
              onClick={() => {
                setIsSupported(false);
              }}
              className="text-[var(--primary)] text-sm mt-2 underline"
            >
              Switch to text input
            </button>
          </div>
        )}

        {/* Recording State */}
        {state === "recording" && (
          <div className="text-center py-4">
            <div className="w-24 h-24 rounded-full bg-red-500 text-white flex items-center justify-center mx-auto mb-4 animate-pulse">
              <span className="material-symbols-outlined text-5xl">mic</span>
            </div>
            <p className="text-[var(--foreground)] font-medium mb-2">Listening...</p>

            <div className="bg-[var(--background)] rounded-lg p-4 mb-6 min-h-[100px] max-h-[200px] overflow-y-auto text-left">
              <p className="text-[var(--foreground-secondary)] text-sm">
                {transcript || "Start speaking..."}
              </p>
            </div>

            <button
              onClick={stopRecording}
              className="px-8 py-3 bg-[var(--primary)] text-[var(--background-dark)] rounded-full font-bold"
            >
              Done Speaking
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
            <p className="text-[var(--foreground-secondary)]">Polishing your review...</p>
          </div>
        )}

        {/* Editing State */}
        {state === "editing" && polishedReview && (
          <div>
            <p className="text-[var(--foreground-secondary)] text-sm mb-3">
              We've cleaned up your review. Feel free to edit:
            </p>

            <textarea
              value={editedReview}
              onChange={(e) => setEditedReview(e.target.value)}
              className="w-full h-32 p-4 border border-[var(--border)] rounded-xl bg-[var(--background)] text-[var(--foreground)] resize-none focus:outline-none focus:ring-2 focus:ring-[var(--primary)] mb-4"
              aria-label="Edit your review"
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
              <div className="flex gap-4 mb-4 text-xs">
                {polishedReview.highlights.length > 0 && (
                  <div>
                    <span className="text-[var(--success)] font-medium">Highlights: </span>
                    <span className="text-[var(--foreground-muted)]">
                      {polishedReview.highlights.join(", ")}
                    </span>
                  </div>
                )}
                {polishedReview.concerns.length > 0 && (
                  <div>
                    <span className="text-[var(--warning)] font-medium">Concerns: </span>
                    <span className="text-[var(--foreground-muted)]">
                      {polishedReview.concerns.join(", ")}
                    </span>
                  </div>
                )}
              </div>
            )}

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setState("idle");
                  setTranscript("");
                  setPolishedReview(null);
                }}
                className="flex-1 py-3 border border-[var(--border)] rounded-full font-medium text-[var(--foreground-secondary)]"
              >
                Re-record
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
