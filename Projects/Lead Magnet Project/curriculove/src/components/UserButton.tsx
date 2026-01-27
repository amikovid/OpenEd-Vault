"use client";

// Simplified UserButton that doesn't depend on Clerk
// Auth features will be re-enabled when Clerk keys are configured in production
export default function UserButton() {
  return (
    <button
      className="text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors"
      title="Account (coming soon)"
    >
      <span className="material-symbols-outlined text-xl">
        account_circle
      </span>
    </button>
  );
}
