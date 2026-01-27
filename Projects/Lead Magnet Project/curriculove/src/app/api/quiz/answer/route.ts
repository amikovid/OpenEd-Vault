import { NextRequest, NextResponse } from "next/server";
import { getSession, setSession } from "@/lib/sessionStore";
import {
  OPENER_SCORE_DELTAS,
  GUIDED_Q2_SCORE_DELTAS,
  applyScoreDeltas,
  calculateConfidence,
  selectNextQuestion,
  deriveResult,
  PHILOSOPHY_NAMES,
  PHILOSOPHY_DESCRIPTIONS,
  scoreFreeText,
} from "@/lib/quiz-agent/scoring";
import { OPENER_SIGNALS } from "@/lib/quiz-agent/prompt";

const MIN_QUESTIONS = 5;
const CONFIDENCE_THRESHOLD = 75;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      sessionId,
      selectedOptionIndex,
      currentQuestion,
      freeText,
    }: {
      sessionId: string;
      selectedOptionIndex: number;
      currentQuestion: {
        question: string;
        options: string[];
      };
      freeText?: string;
    } = body;

    if (!sessionId || selectedOptionIndex === undefined || !currentQuestion) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    // Get session
    const session = getSession(sessionId);
    if (!session) {
      return NextResponse.json(
        { error: "Session not found" },
        { status: 404 }
      );
    }

    // Get the selected answer text
    const selectedAnswer = currentQuestion.options[selectedOptionIndex];
    if (!selectedAnswer) {
      return NextResponse.json(
        { error: "Invalid option index" },
        { status: 400 }
      );
    }

    // Record the answer
    session.questionHistory.push({
      question: currentQuestion.question,
      selectedOption: selectedAnswer,
      optionIndex: selectedOptionIndex,
      freeText: typeof freeText === "string" && freeText.trim() ? freeText.trim() : undefined,
    });

    session.agentHistory.push({
      question: currentQuestion.question,
      options: currentQuestion.options,
      answer: selectedAnswer,
    });

    const questionCount = session.questionHistory.length;
    const freeTextDeltas =
      typeof freeText === "string" && freeText.trim()
        ? scoreFreeText(freeText)
        : null;

    // =========================================================
    // PHASE 1: OPENER - Apply opener score deltas
    // =========================================================
    if (session.phase === "opener") {
      // Apply opener score deltas
      const deltas = OPENER_SCORE_DELTAS[selectedOptionIndex];
      if (deltas) {
        session.philosophyScores = applyScoreDeltas(session.philosophyScores, deltas);
      }
      if (freeTextDeltas) {
        session.philosophyScores = applyScoreDeltas(session.philosophyScores, freeTextDeltas);
      }

      // Save opener choice for guided Q2
      session.openerChoice = selectedOptionIndex;
      session.phase = "guided";

      // Get guided Q2 based on opener choice
      const guidedQ2 = OPENER_SIGNALS[selectedOptionIndex];
      if (guidedQ2) {
        session.currentQuestionId = "guided";
        setSession(sessionId, session);

        return NextResponse.json({
          isComplete: false,
          question: guidedQ2.nextQuestion,
          options: guidedQ2.distinguishingOptions,
          questionNumber: questionCount + 1,
          phase: "guided",
          scores: session.philosophyScores,
        });
      }
    }

    // =========================================================
    // PHASE 2: GUIDED Q2 - Apply guided score deltas
    // =========================================================
    if (session.phase === "guided" && session.openerChoice !== null) {
      const deltas = GUIDED_Q2_SCORE_DELTAS[session.openerChoice]?.[selectedOptionIndex];
      if (deltas) {
        session.philosophyScores = applyScoreDeltas(session.philosophyScores, deltas);
      }
      if (freeTextDeltas) {
        session.philosophyScores = applyScoreDeltas(session.philosophyScores, freeTextDeltas);
      }

      session.phase = "refinement";
    }

    // =========================================================
    // PHASE 3: REFINEMENT - Use question bank
    // =========================================================
    if (session.phase === "refinement") {
      // Apply score deltas for the current question using the tracked ID
      if (session.currentQuestionId && session.currentQuestionId !== "opener" && session.currentQuestionId !== "guided") {
        const { QUESTION_BANK } = await import("@/lib/quiz-agent/scoring");
        const bankQuestion = QUESTION_BANK.find((q) => q.id === session.currentQuestionId);

        if (bankQuestion) {
          const deltas = bankQuestion.scoreDeltas[selectedOptionIndex];
          if (deltas) {
            session.philosophyScores = applyScoreDeltas(session.philosophyScores, deltas);
          }
        }
      }
      if (freeTextDeltas) {
        session.philosophyScores = applyScoreDeltas(session.philosophyScores, freeTextDeltas);
      }

      // Check completion criteria
      const confidence = calculateConfidence(session.philosophyScores);
      const canComplete = questionCount >= MIN_QUESTIONS && confidence >= CONFIDENCE_THRESHOLD;

      if (canComplete) {
        session.phase = "complete";
        const result = deriveResult(session.philosophyScores);
        setSession(sessionId, session);

        return NextResponse.json({
          isComplete: true,
          result: {
            primary: {
              tag: result.primary.tag,
              name: result.primary.name,
              description: result.primary.description,
              score: result.primary.score,
            },
            secondary: result.secondary,
            confidence: result.confidence,
            scores: session.philosophyScores,
          },
          questionCount,
        });
      }

      // Select next question from bank
      const nextQuestion = selectNextQuestion(
        session.philosophyScores,
        session.askedQuestionIds
      );

      if (nextQuestion) {
        session.askedQuestionIds.push(nextQuestion.id);
        session.currentQuestionId = nextQuestion.id;
        setSession(sessionId, session);

        return NextResponse.json({
          isComplete: false,
          question: nextQuestion.question,
          options: nextQuestion.options,
          questionNumber: questionCount + 1,
          phase: "refinement",
          scores: session.philosophyScores,
        });
      }

      // No more questions available - complete anyway
      session.phase = "complete";
      const result = deriveResult(session.philosophyScores);
      setSession(sessionId, session);

      return NextResponse.json({
        isComplete: true,
        result: {
          primary: {
            tag: result.primary.tag,
            name: result.primary.name,
            description: result.primary.description,
            score: result.primary.score,
          },
          secondary: result.secondary,
          confidence: result.confidence,
          scores: session.philosophyScores,
        },
        questionCount,
      });
    }

    // Fallback - shouldn't reach here
    setSession(sessionId, session);
    const result = deriveResult(session.philosophyScores);

    return NextResponse.json({
      isComplete: true,
      result: {
        primary: {
          tag: result.primary.tag,
          name: result.primary.name,
          description: result.primary.description,
          score: result.primary.score,
        },
        secondary: result.secondary,
        confidence: result.confidence,
        scores: session.philosophyScores,
      },
      questionCount,
    });
  } catch (error) {
    console.error("Error processing answer:", error);
    return NextResponse.json(
      { error: "Failed to process answer", details: String(error) },
      { status: 500 }
    );
  }
}
