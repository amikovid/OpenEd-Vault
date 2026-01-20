"use client";

import { useUser, SignInButton, UserButton as ClerkUserButton } from "@clerk/nextjs";

export default function UserButton() {
  const { isSignedIn, isLoaded } = useUser();

  if (!isLoaded) {
    return null;
  }

  if (!isSignedIn) {
    return (
      <SignInButton mode="modal">
        <button
          className="text-[var(--foreground-muted)] hover:text-[var(--foreground)] transition-colors"
          title="Sign in to save across devices"
        >
          <span className="material-symbols-outlined text-xl">
            account_circle
          </span>
        </button>
      </SignInButton>
    );
  }

  return (
    <ClerkUserButton
      afterSignOutUrl="/"
      appearance={{
        elements: {
          avatarBox: "w-7 h-7",
        },
      }}
    />
  );
}
