"use client";

import { useState } from "react";

// US States - OpenEd operates in AR, IN, IA, KS, MN, MT, NV, OR, UT
const US_STATES = [
  { value: "", label: "Select state (optional)" },
  { value: "AL", label: "Alabama" },
  { value: "AK", label: "Alaska" },
  { value: "AZ", label: "Arizona" },
  { value: "AR", label: "Arkansas" },
  { value: "CA", label: "California" },
  { value: "CO", label: "Colorado" },
  { value: "CT", label: "Connecticut" },
  { value: "DE", label: "Delaware" },
  { value: "FL", label: "Florida" },
  { value: "GA", label: "Georgia" },
  { value: "HI", label: "Hawaii" },
  { value: "ID", label: "Idaho" },
  { value: "IL", label: "Illinois" },
  { value: "IN", label: "Indiana" },
  { value: "IA", label: "Iowa" },
  { value: "KS", label: "Kansas" },
  { value: "KY", label: "Kentucky" },
  { value: "LA", label: "Louisiana" },
  { value: "ME", label: "Maine" },
  { value: "MD", label: "Maryland" },
  { value: "MA", label: "Massachusetts" },
  { value: "MI", label: "Michigan" },
  { value: "MN", label: "Minnesota" },
  { value: "MS", label: "Mississippi" },
  { value: "MO", label: "Missouri" },
  { value: "MT", label: "Montana" },
  { value: "NE", label: "Nebraska" },
  { value: "NV", label: "Nevada" },
  { value: "NH", label: "New Hampshire" },
  { value: "NJ", label: "New Jersey" },
  { value: "NM", label: "New Mexico" },
  { value: "NY", label: "New York" },
  { value: "NC", label: "North Carolina" },
  { value: "ND", label: "North Dakota" },
  { value: "OH", label: "Ohio" },
  { value: "OK", label: "Oklahoma" },
  { value: "OR", label: "Oregon" },
  { value: "PA", label: "Pennsylvania" },
  { value: "RI", label: "Rhode Island" },
  { value: "SC", label: "South Carolina" },
  { value: "SD", label: "South Dakota" },
  { value: "TN", label: "Tennessee" },
  { value: "TX", label: "Texas" },
  { value: "UT", label: "Utah" },
  { value: "VT", label: "Vermont" },
  { value: "VA", label: "Virginia" },
  { value: "WA", label: "Washington" },
  { value: "WV", label: "West Virginia" },
  { value: "WI", label: "Wisconsin" },
  { value: "WY", label: "Wyoming" },
];

interface EmailGateProps {
  primaryPhilosophy: string;
  primaryPhilosophyName: string;
  secondaryPhilosophies?: string[];
  confidence?: number;
  onSubmit: (email: string, state?: string) => void;
  onSkip?: () => void;
}

export default function EmailGate({
  primaryPhilosophy,
  primaryPhilosophyName,
  secondaryPhilosophies,
  confidence,
  onSubmit,
  onSkip,
}: EmailGateProps) {
  const [email, setEmail] = useState("");
  const [state, setState] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email || !email.includes("@")) {
      setError("Please enter a valid email");
      return;
    }

    setIsSubmitting(true);

    try {
      // Send to HubSpot
      const response = await fetch("/api/hubspot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          state: state || undefined,
          primaryPhilosophy,
          primaryPhilosophyName,
          secondaryPhilosophies,
          confidence,
        }),
      });

      const data = await response.json();

      if (!data.success) {
        console.error("HubSpot error:", data.error);
        // Don't show error to user - still proceed
      }

      setIsSubmitting(false);
      onSubmit(email, state || undefined);
    } catch (err) {
      console.error("Submit error:", err);
      setIsSubmitting(false);
      // Still proceed even on error
      onSubmit(email, state || undefined);
    }
  };

  return (
    <div className="mobile-container flex flex-col min-h-[100dvh] bg-[var(--surface)]">
      {/* Header */}
      <div className="p-6 pb-0">
        <div className="flex items-center justify-center">
          <h1 className="text-xl font-bold text-[var(--foreground)]">
            Curriculove
          </h1>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 pb-6">
        {/* Success checkmark */}
        <div className="w-20 h-20 rounded-full bg-[var(--primary)] flex items-center justify-center mb-6 shadow-lg shadow-[var(--primary)]/30">
          <span className="material-symbols-outlined text-[var(--background-dark)] text-4xl">
            check_circle
          </span>
        </div>

        {/* Title */}
        <h2 className="text-2xl font-extrabold text-[var(--foreground)] text-center mb-2">
          Quiz Complete!
        </h2>

        <p className="text-[var(--foreground-secondary)] text-center mb-8 max-w-xs leading-relaxed">
          We've identified your homeschool style. Enter your email to see your results and top curriculum matches.
        </p>

        {/* Form */}
        <form onSubmit={handleSubmit} className="w-full max-w-sm">
          <div className="relative mb-4">
            <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-[var(--foreground-muted)]">
              mail
            </span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="w-full h-14 rounded-2xl bg-[var(--background)] border-2 border-[var(--border)] pl-12 pr-4 text-base text-[var(--foreground)] placeholder:text-[var(--foreground-muted)] focus:border-[var(--primary)] focus:outline-none transition-colors"
              disabled={isSubmitting}
              autoFocus
              aria-label="Email address"
            />
          </div>

          <div className="relative mb-4">
            <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-[var(--foreground-muted)]">
              location_on
            </span>
            <select
              value={state}
              onChange={(e) => setState(e.target.value)}
              className="w-full h-14 rounded-2xl bg-[var(--background)] border-2 border-[var(--border)] pl-12 pr-4 text-base text-[var(--foreground)] focus:border-[var(--primary)] focus:outline-none transition-colors appearance-none cursor-pointer"
              disabled={isSubmitting}
              aria-label="Select your state"
            >
              {US_STATES.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
            <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-[var(--foreground-muted)] pointer-events-none">
              expand_more
            </span>
          </div>

          {error && (
            <p className="text-[var(--error)] text-sm text-center mb-4">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full h-14 bg-[var(--primary)] text-[var(--background-dark)] rounded-full font-bold text-base flex items-center justify-center gap-2 disabled:opacity-50 active:scale-[0.98] transition-all shadow-lg shadow-[var(--primary)]/20"
          >
            {isSubmitting ? (
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-[var(--background-dark)] rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-[var(--background-dark)] rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-[var(--background-dark)] rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            ) : (
              <>
                <span>See My Results</span>
                <span className="material-symbols-outlined">arrow_forward</span>
              </>
            )}
          </button>
        </form>

        {/* Skip link */}
        {onSkip && (
          <button
            onClick={onSkip}
            className="mt-6 text-sm text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors underline underline-offset-2"
          >
            Skip for now
          </button>
        )}

        {/* Trust signals */}
        <div className="mt-10 flex items-center gap-6 text-xs text-[var(--foreground-muted)]">
          <div className="flex items-center gap-1.5">
            <span className="material-symbols-outlined text-sm text-[var(--primary)]">lock</span>
            <span>No spam, ever</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="material-symbols-outlined text-sm text-[var(--primary)]">verified</span>
            <span>100% free</span>
          </div>
        </div>
      </div>
    </div>
  );
}
