import { PhilosophyTag } from "@/data/philosophies";
import { PhilosophyScores } from "@/lib/quiz-agent/scoring";

export type QuizPhase = "opener" | "guided" | "refinement" | "complete";

export interface QuizSession {
  sessionId: string;
  philosophyScores: PhilosophyScores;
  questionHistory: { question: string; selectedOption: string; optionIndex: number; freeText?: string }[];
  // Full history for agent context
  agentHistory: { question: string; options: string[]; answer: string }[];
  // Track which questions from the bank have been asked
  askedQuestionIds: string[];
  // Track opener choice for guided Q2
  openerChoice: number | null;
  // Track current question being answered (for score delta application)
  currentQuestionId: string | null;
  // Current phase
  phase: QuizPhase;
  createdAt: number;
}

// Declare the global type
declare global {
  // eslint-disable-next-line no-var
  var _quizSessions: Map<string, QuizSession> | undefined;
}

// Use globalThis to persist across module reloads in development
const globalSessions = globalThis._quizSessions ?? new Map<string, QuizSession>();
globalThis._quizSessions = globalSessions;

export function getSession(sessionId: string): QuizSession | undefined {
  return globalSessions.get(sessionId);
}

export function setSession(sessionId: string, session: QuizSession): void {
  globalSessions.set(sessionId, session);
}

export function deleteSession(sessionId: string): boolean {
  return globalSessions.delete(sessionId);
}

// For debugging
export function getSessionCount(): number {
  return globalSessions.size;
}
