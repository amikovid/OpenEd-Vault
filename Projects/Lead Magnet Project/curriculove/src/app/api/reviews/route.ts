import { NextResponse } from "next/server";
import { ConvexHttpClient } from "convex/browser";
import { api } from "../../../../convex/_generated/api";

interface ReviewSubmission {
  curriculumSlug: string;
  curriculumName: string;
  rawTranscript: string;
  polishedReview: string;
  rating: number;
  highlights: string[];
  concerns: string[];
  bestFor: string[];
  userEmail?: string;
  userName?: string;
}

const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL;

function getConvexClient() {
  if (!convexUrl) {
    throw new Error("NEXT_PUBLIC_CONVEX_URL is not set");
  }
  return new ConvexHttpClient(convexUrl);
}

export async function POST(request: Request) {
  try {
    const body: ReviewSubmission = await request.json();

    const client = getConvexClient();

    const reviewId = await client.mutation(api.reviews.submitReview, {
      curriculumSlug: body.curriculumSlug,
      curriculumName: body.curriculumName,
      rawTranscript: body.rawTranscript,
      polishedReview: body.polishedReview,
      rating: body.rating,
      highlights: body.highlights,
      concerns: body.concerns,
      bestFor: body.bestFor,
      userEmail: body.userEmail,
      userName: body.userName,
    });

    console.log("Review saved to Convex:", {
      reviewId,
      curriculum: body.curriculumName,
      email: body.userEmail,
      rating: body.rating,
    });

    return NextResponse.json({
      success: true,
      message: "Review saved successfully",
      reviewId: reviewId,
    });
  } catch (error) {
    console.error("Error saving review:", error);
    return NextResponse.json(
      { error: "Failed to save review" },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    const client = getConvexClient();
    const reviews = await client.query(api.reviews.getAllReviews, {});

    return NextResponse.json({
      reviews,
      count: reviews.length,
    });
  } catch (error) {
    console.error("Error loading reviews:", error);
    return NextResponse.json(
      { error: "Failed to load reviews" },
      { status: 500 }
    );
  }
}
