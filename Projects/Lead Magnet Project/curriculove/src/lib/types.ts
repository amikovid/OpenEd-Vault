/**
 * Shared types for Curriculove
 */

/**
 * OpenEd Insight - structured expert review data
 *
 * Supports both legacy string format (backwards compatible)
 * and new object format with quote, attribution, synthesis
 */
export interface OpenEdInsight {
  quote?: string;           // Real teacher/parent quote
  attribution?: string;     // "First Name L." format
  synthesis?: string;       // 1-2 sentence editorial summary
  hasFullReview: boolean;   // Whether opened.co/tool/[slug] exists
}

/**
 * Curriculum data structure
 */
export interface Curriculum {
  name: string;
  slug: string;
  description: string;
  pricingSummary: string;
  priceTier: string;
  website: string;
  gradeRange: string;
  philosophyTags: string[];
  subjectTags?: string[];
  methodTags?: string[];
  audienceTags?: string[];
  // Supports both legacy string and new object format
  openedInsight: string | OpenEdInsight;
  logoUrl: string | null;
  imageUrl: string | null;
  isOpenEdVendor: boolean;
  prepTimeScore?: number;
  teacherInvolvementLevel?: string;
  lessonDuration?: string;
}

/**
 * Recommendation with curriculum data
 */
export interface Recommendation {
  slug: string;
  name: string;
  matchScore: number;
  reason: string;
  curriculum: Curriculum | null;
}

/**
 * Helper to extract insight data from either format
 */
export function getInsightData(insight: string | OpenEdInsight | undefined): {
  quote?: string;
  attribution?: string;
  synthesis: string;
  hasFullReview: boolean;
} {
  if (!insight) {
    return { synthesis: '', hasFullReview: false };
  }

  if (typeof insight === 'string') {
    // Legacy format - treat as synthesis
    return { synthesis: insight, hasFullReview: false };
  }

  // New object format
  return {
    quote: insight.quote,
    attribution: insight.attribution,
    synthesis: insight.synthesis || '',
    hasFullReview: insight.hasFullReview,
  };
}

/**
 * Philosophy tag short names
 */
export const PHILOSOPHY_SHORT: Record<string, string> = {
  CL: "Classical",
  CM: "Charlotte Mason",
  TR: "Traditional",
  MO: "Montessori",
  WA: "Waldorf",
  UN: "Unschooling",
  WF: "Wild + Free",
  NB: "Nature-Based",
  PB: "Project-Based",
  EC: "Eclectic",
  MS: "Microschool",
  FB: "Faith-Based",
};
