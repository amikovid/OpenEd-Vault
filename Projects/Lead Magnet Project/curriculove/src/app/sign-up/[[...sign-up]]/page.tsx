import { SignUp } from "@clerk/nextjs";

export default function SignUpPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[100dvh] bg-[var(--surface)] p-6">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-bold text-[var(--foreground)] mb-2">
          Join Curriculove
        </h1>
        <p className="text-[var(--foreground-secondary)] text-sm">
          Create an account to save favorites and share reviews
        </p>
      </div>
      <SignUp
        appearance={{
          elements: {
            rootBox: "w-full max-w-md",
            card: "bg-[var(--background)] border border-[var(--border)] shadow-xl",
            headerTitle: "text-[var(--foreground)]",
            headerSubtitle: "text-[var(--foreground-secondary)]",
            formButtonPrimary: "bg-[var(--primary)] hover:bg-[var(--primary)]/90",
          },
        }}
      />
    </div>
  );
}
