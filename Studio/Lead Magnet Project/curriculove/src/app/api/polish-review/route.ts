import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || "");

interface PolishRequest {
  rawTranscript: string;
  curriculumName: string;
  curriculumSlug: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: PolishRequest = await request.json();
    const { rawTranscript, curriculumName, curriculumSlug } = body;

    if (!rawTranscript || !curriculumName) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      );
    }

    const prompt = `You're helping a homeschool parent write a curriculum review. They spoke this raw transcript about "${curriculumName}":

"${rawTranscript}"

Transform this into a helpful, authentic review. Guidelines:
- Keep their genuine voice and opinions
- Remove filler words, false starts, and repetition
- Organize into clear, readable paragraphs
- Don't add information they didn't mention
- Keep it concise (2-4 sentences for short reviews, 1-2 paragraphs for longer ones)
- Make it helpful for other parents considering this curriculum

Return JSON only (no markdown):
{
  "polishedReview": "The cleaned-up review text",
  "rating": 4,
  "highlights": ["positive aspect 1", "positive aspect 2"],
  "concerns": ["concern 1"],
  "bestFor": ["type of learner or family this suits"]
}

Rules for extraction:
- rating: Infer from tone (1=very negative, 3=mixed, 5=very positive). Default to 4 if positive but not glowing.
- highlights: Only include if they explicitly praised something
- concerns: Only include if they explicitly mentioned a downside
- bestFor: Only include if they mentioned who it works well for

If the transcript is too short or unclear, still return valid JSON with your best effort.`;

    const model = genAI.getGenerativeModel({
      model: "gemini-3-flash-preview",
      generationConfig: {
        temperature: 0.3,
        maxOutputTokens: 1024,
      },
    });

    const result = await model.generateContent(prompt);
    const responseText = result.response.text();

    // Parse JSON from response
    let jsonText = responseText;

    // Remove markdown code blocks if present
    const codeBlockMatch = responseText.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (codeBlockMatch) {
      jsonText = codeBlockMatch[1];
    }

    // Find the JSON object
    const jsonMatch = jsonText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      console.error("Could not find JSON in response:", responseText);
      // Fallback: return the raw transcript as the review
      return NextResponse.json({
        curriculumSlug,
        rawTranscript,
        polishedReview: rawTranscript,
        rating: 4,
        highlights: [],
        concerns: [],
        bestFor: [],
      });
    }

    const parsed = JSON.parse(jsonMatch[0]);

    return NextResponse.json({
      curriculumSlug,
      rawTranscript,
      polishedReview: parsed.polishedReview || rawTranscript,
      rating: parsed.rating || 4,
      highlights: parsed.highlights || [],
      concerns: parsed.concerns || [],
      bestFor: parsed.bestFor || [],
    });
  } catch (error) {
    console.error("Error polishing review:", error);
    return NextResponse.json(
      { error: "Failed to polish review", details: String(error) },
      { status: 500 }
    );
  }
}
