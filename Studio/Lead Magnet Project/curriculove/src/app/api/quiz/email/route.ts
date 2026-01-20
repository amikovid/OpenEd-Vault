import { NextRequest, NextResponse } from "next/server";
import { getSession } from "@/lib/sessionStore";

// Simple email collection (no HubSpot for now)
const collectedEmails: { email: string; sessionId: string; timestamp: number }[] = [];

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { sessionId, email } = body;

    if (!sessionId || !email) {
      return NextResponse.json(
        { error: "Missing sessionId or email" },
        { status: 400 }
      );
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: "Invalid email format" },
        { status: 400 }
      );
    }

    // Get session to verify it exists
    const session = getSession(sessionId);
    if (!session) {
      return NextResponse.json(
        { error: "Session not found" },
        { status: 404 }
      );
    }

    // Store email (in memory for now)
    collectedEmails.push({
      email,
      sessionId,
      timestamp: Date.now(),
    });

    console.log(`[Email Captured] ${email} for session ${sessionId}`);
    console.log(`Total emails collected: ${collectedEmails.length}`);

    return NextResponse.json({
      success: true,
      message: "Email captured successfully",
    });
  } catch (error) {
    console.error("Error capturing email:", error);
    return NextResponse.json(
      { error: "Failed to capture email" },
      { status: 500 }
    );
  }
}

// Export for debugging
export { collectedEmails };
