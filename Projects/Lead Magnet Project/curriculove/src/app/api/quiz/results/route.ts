import { NextRequest, NextResponse } from "next/server";
import { getSession } from "@/lib/sessionStore";
import { PHILOSOPHIES, PhilosophyTag } from "@/data/philosophies";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const sessionId = searchParams.get("sessionId");

    if (!sessionId) {
      return NextResponse.json(
        { error: "Missing sessionId" },
        { status: 400 }
      );
    }

    // Get session from memory
    const session = getSession(sessionId);

    if (!session) {
      return NextResponse.json(
        { error: "Session not found" },
        { status: 404 }
      );
    }

    // Calculate results from scores
    const scores = Object.entries(session.philosophyScores) as [PhilosophyTag, number][];
    const sorted = scores.sort(([, a], [, b]) => b - a);

    const [primaryTag, primaryScore] = sorted[0];
    const primary = PHILOSOPHIES[primaryTag];

    const secondary = sorted.slice(1, 3).map(([tag, score]) => ({
      tag,
      name: PHILOSOPHIES[tag].name,
      category: PHILOSOPHIES[tag].category,
      description: PHILOSOPHIES[tag].resultDescription,
      score,
    }));

    // Calculate confidence
    const lead = sorted[0][1] - sorted[1][1];
    const totalScore = sorted.reduce((sum, [, score]) => sum + score, 0);
    const confidence = totalScore > 0 ? Math.round((lead / totalScore) * 100) : 0;

    return NextResponse.json({
      result: {
        primary: {
          tag: primaryTag,
          name: primary.name,
          category: primary.category,
          description: primary.resultDescription,
          keyIndicators: primary.keyIndicators,
          keyResources: primary.keyResources,
          shareText: primary.shareText,
          score: primaryScore,
        },
        secondary,
        confidence: Math.min(confidence, 100),
        questionCount: session.questionHistory.length,
      },
    });
  } catch (error) {
    console.error("Error fetching results:", error);
    return NextResponse.json(
      { error: "Failed to fetch results" },
      { status: 500 }
    );
  }
}
