import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";
import curricula from "@/data/curricula-convex.json";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || "");

// Philosophy full names for context
const PHILOSOPHY_NAMES: Record<string, string> = {
  CM: "Charlotte Mason",
  CL: "Classical",
  TR: "Traditional",
  MO: "Montessori",
  WA: "Waldorf",
  UN: "Unschooling",
  EC: "Eclectic",
  PB: "Project-Based",
  NB: "Nature-Based",
  FB: "Faith-Based",
  WF: "Wild + Free",
  MS: "Microschool",
};

interface Curriculum {
  slug: string;
  name: string;
  imageUrl: string | null;
  logoUrl: string | null;
  website: string;
  gradeRange: string;
  philosophyTags: string[];
  philosophyText: string;
  methodTags: string[];
  audienceTags: string[];
  description: string;
  teachingFormat: string;
  pricingSummary: string;
  priceTier: string;
  parentInvolvement: string;
  openedInsight: string;
  subjectTags: string[];
  isOpenEdVendor: boolean;
  source: string;
  // New enrichment fields
  originalPhilosophyTags?: string[];
  philosophyReasoning?: string;
  prepTimeScore?: number;
  teacherInvolvementLevel?: string;
  lessonDuration?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      primaryPhilosophy,
      secondaryPhilosophies,
      confidence,
      reasoning,
    }: {
      primaryPhilosophy: string;
      secondaryPhilosophies: string[];
      confidence: number;
      reasoning?: string;
    } = body;

    if (!primaryPhilosophy) {
      return NextResponse.json(
        { error: "Missing primaryPhilosophy" },
        { status: 400 }
      );
    }

    // Pre-filter curricula by philosophy tags (reduce context for Gemini)
    const relevantTags = [primaryPhilosophy, ...(secondaryPhilosophies || [])];
    const filteredCurricula = (curricula as Curriculum[]).filter((c) =>
      c.philosophyTags.some((tag) => relevantTags.includes(tag))
    );

    // If not enough, include some Eclectic ones
    let candidateCurricula = filteredCurricula;
    if (filteredCurricula.length < 30) {
      const eclecticCurricula = (curricula as Curriculum[]).filter(
        (c) => c.philosophyTags.includes("EC") && !filteredCurricula.includes(c)
      );
      candidateCurricula = [...filteredCurricula, ...eclecticCurricula.slice(0, 20)];
    }

    // Sanitize text for JSON (remove problematic characters)
    const sanitize = (text: string | object | undefined | null): string => {
      if (!text) return "";
      // Handle objects (like openedInsight with {quote, synthesis, etc.})
      if (typeof text === "object") {
        const obj = text as Record<string, unknown>;
        // Try to extract useful text from object
        const textValue = obj.synthesis || obj.quote || obj.summary || "";
        return sanitize(String(textValue));
      }
      return String(text)
        .replace(/[\u0000-\u001F\u007F-\u009F]/g, " ") // Control characters
        .replace(/\\/g, "\\\\") // Backslashes
        .replace(/"/g, '\\"') // Quotes
        .trim();
    };

    // Build curriculum summary for Gemini (include new enrichment fields)
    const curriculaSummary = candidateCurricula.map((c) => ({
      slug: c.slug,
      name: sanitize(c.name),
      description: sanitize(c.description).slice(0, 300),
      tags: c.philosophyTags,
      pricing: sanitize(c.pricingSummary).slice(0, 100),
      priceTier: c.priceTier,
      notes: sanitize(c.openedInsight).slice(0, 200),
      prepTime: c.prepTimeScore,
      teacherInvolvement: c.teacherInvolvementLevel,
      isOpenEdVendor: c.isOpenEdVendor,
    }));

    const primaryName = PHILOSOPHY_NAMES[primaryPhilosophy] || primaryPhilosophy;
    const secondaryNames = (secondaryPhilosophies || [])
      .map((t) => PHILOSOPHY_NAMES[t] || t)
      .join(", ");

    const prompt = `You are a homeschool curriculum advisor. A parent just completed a quiz and their results are:

Primary Philosophy: ${primaryName} (${primaryPhilosophy})
Secondary Matches: ${secondaryNames || "None"}
Confidence: ${confidence}%
${reasoning ? `Quiz Reasoning: ${reasoning}` : ""}

Here are ${curriculaSummary.length} curricula that might match their philosophy:

${JSON.stringify(curriculaSummary, null, 2)}

Select the TOP 3 curricula that best match this parent's philosophy. For each, explain in 1 sentence why it's a good fit.

Return JSON only:
{
  "recommendations": [
    {
      "slug": "curriculum_slug",
      "name": "Curriculum Name",
      "matchScore": 95,
      "reason": "Why this matches their philosophy"
    }
  ]
}

Prioritize curricula that:
1. Have the primary philosophy tag
2. Match the style and approach implied by the philosophy
3. Have positive OpenEd notes if available
4. Offer good value for the approach

Return ONLY valid JSON, no markdown.`;

    // Call Gemini 3 Flash
    const model = genAI.getGenerativeModel({
      model: "gemini-3-flash-preview",
      generationConfig: {
        temperature: 0.3,
        maxOutputTokens: 4096, // Increased to prevent truncation
      },
    });

    const result = await model.generateContent(prompt);
    const responseText = result.response.text();

    // Parse JSON from response (handle potential markdown code blocks)
    let jsonText = responseText;

    // Remove markdown code blocks if present
    const codeBlockMatch = responseText.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (codeBlockMatch) {
      jsonText = codeBlockMatch[1];
    }

    // Find the JSON object
    let jsonMatch = jsonText.match(/\{[\s\S]*\}/);

    // Try to repair truncated JSON
    if (!jsonMatch) {
      // Maybe JSON was truncated - try to find partial and close it
      const partialMatch = jsonText.match(/\{[\s\S]*/);
      if (partialMatch) {
        let partial = partialMatch[0];
        // Count open/close brackets and try to close
        const openBrackets = (partial.match(/\[/g) || []).length;
        const closeBrackets = (partial.match(/\]/g) || []).length;
        const openBraces = (partial.match(/\{/g) || []).length;
        const closeBraces = (partial.match(/\}/g) || []).length;

        // Remove any incomplete last item (ends with comma or incomplete string)
        partial = partial.replace(/,\s*"[^"]*$/, "");
        partial = partial.replace(/,\s*\{[^}]*$/, "");
        partial = partial.replace(/,\s*$/, "");

        // Close arrays and objects
        for (let i = 0; i < openBrackets - closeBrackets; i++) partial += "]";
        for (let i = 0; i < openBraces - closeBraces; i++) partial += "}";

        jsonMatch = [partial];
        console.log("Repaired truncated JSON");
      }
    }

    if (!jsonMatch) {
      console.error("Could not find JSON in response:", responseText.slice(0, 500));
      throw new Error("Could not parse recommendations JSON");
    }

    let recommendations;
    try {
      recommendations = JSON.parse(jsonMatch[0]);
    } catch (parseError) {
      console.error("JSON parse error:", parseError);
      console.error("Attempted to parse:", jsonMatch[0].slice(0, 500));

      // Fallback: return simple recommendations without AI reasoning
      console.log("Falling back to simple recommendations");
      const simpleRecs = candidateCurricula.slice(0, 3).map((c, i) => ({
        slug: c.slug,
        name: c.name,
        matchScore: 95 - i * 5,
        reason: `Matches your ${primaryName} philosophy.`,
      }));
      recommendations = { recommendations: simpleRecs };
    }

    // Enrich with full curriculum data
    const enrichedRecommendations = recommendations.recommendations.map(
      (rec: { slug: string; matchScore: number; reason: string }) => {
        const fullCurriculum = (curricula as Curriculum[]).find((c) => c.slug === rec.slug);
        return {
          ...rec,
          curriculum: fullCurriculum
            ? {
                name: fullCurriculum.name,
                slug: fullCurriculum.slug,
                description: fullCurriculum.description,
                pricingSummary: fullCurriculum.pricingSummary,
                priceTier: fullCurriculum.priceTier,
                website: fullCurriculum.website,
                gradeRange: fullCurriculum.gradeRange,
                philosophyTags: fullCurriculum.philosophyTags,
                openedInsight: fullCurriculum.openedInsight,
                logoUrl: fullCurriculum.logoUrl,
                imageUrl: fullCurriculum.imageUrl,
                isOpenEdVendor: fullCurriculum.isOpenEdVendor,
                // New enrichment fields
                prepTimeScore: fullCurriculum.prepTimeScore,
                teacherInvolvementLevel: fullCurriculum.teacherInvolvementLevel,
                lessonDuration: fullCurriculum.lessonDuration,
              }
            : null,
        };
      }
    );

    return NextResponse.json({
      primaryPhilosophy: {
        tag: primaryPhilosophy,
        name: primaryName,
      },
      recommendations: enrichedRecommendations,
      totalCandidates: candidateCurricula.length,
    });
  } catch (error) {
    console.error("Error generating recommendations:", error);
    return NextResponse.json(
      { error: "Failed to generate recommendations", details: String(error) },
      { status: 500 }
    );
  }
}
