import { NextRequest, NextResponse } from "next/server";
import { v4 as uuidv4 } from "uuid";
import { setSession, QuizSession } from "@/lib/sessionStore";
import { initializeScores } from "@/lib/quiz-agent/scoring";
import { OPENER_QUESTION } from "@/lib/quiz-agent/prompt";

export async function POST(request: NextRequest) {
  try {
    const sessionId = uuidv4();

    // Create session with initialized scores
    const session: QuizSession = {
      sessionId,
      philosophyScores: initializeScores(),
      questionHistory: [],
      agentHistory: [],
      askedQuestionIds: [],
      openerChoice: null,
      currentQuestionId: "opener",
      phase: "opener",
      createdAt: Date.now(),
    };
    setSession(sessionId, session);

    // Return the fixed opener question
    return NextResponse.json({
      sessionId,
      question: OPENER_QUESTION.question,
      options: OPENER_QUESTION.options,
      questionNumber: 1,
      phase: "opener",
    });
  } catch (error) {
    console.error("Error starting quiz:", error);
    return NextResponse.json(
      { error: "Failed to start quiz", details: String(error) },
      { status: 500 }
    );
  }
}
