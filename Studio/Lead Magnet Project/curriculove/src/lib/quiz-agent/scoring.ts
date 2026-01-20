/**
 * Deterministic Scoring Engine for Curriculove Quiz
 *
 * Following Oracle's advice: Track a 12-dimensional philosophy profile
 * with explicit score deltas. LLM only selects questions from curated bank.
 */

// All 12 philosophy tags
export type PhilosophyTag =
  | "CL" | "CM" | "TR" | "MO" | "WA" | "UN"
  | "WF" | "NB" | "PB" | "EC" | "MS" | "FB";

export const ALL_PHILOSOPHIES: PhilosophyTag[] = [
  "CL", "CM", "TR", "MO", "WA", "UN", "WF", "NB", "PB", "EC", "MS", "FB"
];

// Full names for display
export const PHILOSOPHY_NAMES: Record<PhilosophyTag, string> = {
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

// Short descriptions for results screen
export const PHILOSOPHY_DESCRIPTIONS: Record<PhilosophyTag, string> = {
  CL: "Great Books, Latin, Socratic method, and the trivium guide your approach",
  CM: "Living books, narration, nature study, and short lessons define your days",
  TR: "Textbooks, grades, and structured lessons provide clear progress markers",
  MO: "A prepared environment where children choose their work at their own pace",
  WA: "Rhythm, imagination, and delayed academics protect childhood wonder",
  UN: "Radical trust in your child to direct their own learning journey",
  WF: "Wonder-based learning, nature, beauty, and community connection",
  NB: "Outdoor-focused learning with risky play and forest school principles",
  PB: "Real-world problems and authentic products drive interdisciplinary learning",
  EC: "Mix-and-match pragmatism - whatever works for your unique family",
  MS: "Small multi-age groups with shared teaching responsibilities",
  FB: "Faith integrated throughout all subjects and daily life",
};

// 12-dimensional score profile
export type PhilosophyScores = Record<PhilosophyTag, number>;

// Initialize all scores to 0
export function initializeScores(): PhilosophyScores {
  return {
    CL: 0, CM: 0, TR: 0, MO: 0, WA: 0, UN: 0,
    WF: 0, NB: 0, PB: 0, EC: 0, MS: 0, FB: 0,
  };
}

// Score deltas: Partial<PhilosophyScores> to update specific tags
type ScoreDeltas = Partial<PhilosophyScores>;

// ============================================================
// STAGE 1: OPENER SCORES
// ============================================================

export const OPENER_SCORE_DELTAS: ScoreDeltas[] = [
  // Option 0: "Great Books, classics, rigorous academics"
  { CL: 40, TR: 15 },
  // Option 1: "Living books, nature study, gentle pace"
  { CM: 35, WF: 20, NB: 15, WA: 10 },
  // Option 2: "Faith and character at the center"
  { FB: 50 },
  // Option 3: "Child-led, following their passions"
  { UN: 35, MO: 25, PB: 15 },
  // Option 4: "Flexible structure - what works for us"
  { EC: 30, TR: 15, PB: 15, MS: 10 },
];

// ============================================================
// STAGE 2: GUIDED Q2 SCORES (based on opener choice)
// ============================================================

export const GUIDED_Q2_SCORE_DELTAS: ScoreDeltas[][] = [
  // After opener 0: "Great Books, classics, rigorous academics"
  [
    { CL: 30 },           // "Wisdom and virtue from great thinkers"
    { TR: 30, CL: -10 },  // "Academic skills for college readiness"
    { CL: 20, FB: 25 },   // "Both - rigorous AND faith-centered"
    { EC: 25, CL: -15 },  // "Actually, I want more flexibility..."
  ],
  // After opener 1: "Living books, nature study, gentle pace"
  [
    { CM: 35 },           // "Charlotte Mason's method - narration, copywork"
    { WF: 30, CM: -5 },   // "Wonder and beauty, less method"
    { NB: 35, WF: 10 },   // "Being outdoors as much as possible"
    { WA: 35 },           // "Protecting childhood imagination"
  ],
  // After opener 2: "Faith and character at the center"
  [
    { FB: 10, CL: 30 },   // "Very structured - classical Christian curriculum"
    { FB: 10, TR: 30 },   // "Structured - textbooks with biblical worldview"
    { FB: 10, CM: 30 },   // "Gentle - faith with living books and nature"
    { FB: 10, EC: 25 },   // "Flexible - faith integrated into whatever works"
  ],
  // After opener 3: "Child-led, following their passions"
  [
    { UN: 35 },           // "Fully child-led - no curriculum, radical trust"
    { MO: 35 },           // "Prepared environment - they choose from options"
    { PB: 30, UN: -10 },  // "Project-based - real problems they care about"
    { WF: 25, UN: -5 },   // "Wonder-based with gentle parent guidance"
  ],
  // After opener 4: "Flexible structure - what works for us"
  [
    { TR: 30, EC: -10 },  // "Online/video curriculum with clear lessons"
    { EC: 30 },           // "Mix of curricula - different for each subject"
    { PB: 30 },           // "Project-based learning with some structure"
    { MS: 35 },           // "Learning pod or co-op with other families"
  ],
];

// ============================================================
// STAGE 3: DISCRIMINATION QUESTION BANK
// Each question targets specific ambiguous pairs
// ============================================================

export interface QuestionBankEntry {
  id: string;
  question: string;
  options: string[];
  scoreDeltas: ScoreDeltas[];
  targetPairs: string[]; // e.g., ["CL-CM", "CL-TR"]
}

export const QUESTION_BANK: QuestionBankEntry[] = [
  // CL vs CM disambiguation
  {
    id: "cl_cm_1",
    question: "When choosing books, what matters most?",
    options: [
      "The Western canon - Plato, Homer, Shakespeare",
      "Living books that spark wonder and discussion",
      "Whatever they're interested in reading",
      "Textbooks with clear learning objectives",
    ],
    scoreDeltas: [
      { CL: 25, TR: 5 },
      { CM: 25, WF: 10 },
      { UN: 20, MO: 10 },
      { TR: 25 },
    ],
    targetPairs: ["CL-CM", "CL-TR"],
  },
  {
    id: "cl_cm_2",
    question: "How do you feel about teaching Latin?",
    options: [
      "Essential - it trains the mind",
      "Nice but not necessary",
      "Would rather focus on nature study",
      "Not interested",
    ],
    scoreDeltas: [
      { CL: 30 },
      { TR: 15, EC: 10 },
      { CM: 20, NB: 15, WF: 10 },
      { UN: 15, MO: 10, PB: 10 },
    ],
    targetPairs: ["CL-CM", "CL-TR"],
  },
  // CM vs WF vs NB disambiguation
  {
    id: "cm_wf_nb",
    question: "What's most important about time outdoors?",
    options: [
      "Nature notebooks and formal observation",
      "Wonder and beauty, no assignments",
      "Risky play and physical challenge",
      "We're fine with mostly indoor learning",
    ],
    scoreDeltas: [
      { CM: 25 },
      { WF: 25 },
      { NB: 30 },
      { TR: 15, CL: 10 },
    ],
    targetPairs: ["CM-WF", "CM-NB", "WF-NB"],
  },
  // UN vs MO disambiguation
  {
    id: "un_mo_1",
    question: "How structured is your child's environment?",
    options: [
      "Carefully prepared with specific materials",
      "Minimal - they create their own spaces",
      "Organized but flexible",
      "Very structured with clear workspaces",
    ],
    scoreDeltas: [
      { MO: 30 },
      { UN: 30 },
      { EC: 20, WF: 10 },
      { TR: 25, CL: 10 },
    ],
    targetPairs: ["UN-MO", "UN-EC"],
  },
  // MO vs WA disambiguation
  {
    id: "mo_wa_1",
    question: "When should formal academics begin?",
    options: [
      "When the child shows readiness (age 3-6)",
      "Not until age 7 - protect imagination first",
      "Age-appropriate from the start",
      "Whenever they're interested - no set time",
    ],
    scoreDeltas: [
      { MO: 30 },
      { WA: 35 },
      { TR: 25, CL: 10 },
      { UN: 25 },
    ],
    targetPairs: ["MO-WA"],
  },
  // TR vs EC disambiguation
  {
    id: "tr_ec_1",
    question: "How do you feel about grade-level standards?",
    options: [
      "Important - I want to track against benchmarks",
      "Useful reference but not rigid",
      "Don't care about grade levels",
      "Depends on the subject",
    ],
    scoreDeltas: [
      { TR: 30 },
      { EC: 20, CM: 10 },
      { UN: 25, MO: 10 },
      { EC: 25 },
    ],
    targetPairs: ["TR-EC"],
  },
  // PB vs UN disambiguation
  {
    id: "pb_un_1",
    question: "How much do you guide project choices?",
    options: [
      "I suggest problems worth solving",
      "Entirely their choice",
      "We brainstorm together",
      "I assign projects with clear goals",
    ],
    scoreDeltas: [
      { PB: 30 },
      { UN: 30 },
      { EC: 20, WF: 10 },
      { TR: 25 },
    ],
    targetPairs: ["PB-UN"],
  },
  // FB overlay detection
  {
    id: "fb_overlay_1",
    question: "How central is faith to your homeschool?",
    options: [
      "Woven into everything we do",
      "Important but separate from academics",
      "Personal choice - not emphasized",
      "We're secular",
    ],
    scoreDeltas: [
      { FB: 35 },
      { FB: 15 },
      { FB: -10 },
      { FB: -20 },
    ],
    targetPairs: ["FB-any"],
  },
  // MS detection
  {
    id: "ms_1",
    question: "How do you feel about teaching with other families?",
    options: [
      "Love it - co-ops are essential",
      "Occasional group activities are nice",
      "Prefer to teach independently",
      "Only for specialized subjects",
    ],
    scoreDeltas: [
      { MS: 35 },
      { WF: 15, EC: 10 },
      { CL: 10, CM: 10 },
      { EC: 20 },
    ],
    targetPairs: ["MS-EC"],
  },
  // Structure spectrum
  {
    id: "structure_1",
    question: "How much daily structure do you want?",
    options: [
      "Clear schedule with timed blocks",
      "Gentle rhythm with flexibility",
      "Follow the child's lead each day",
      "Mix - structured core, flexible extras",
    ],
    scoreDeltas: [
      { TR: 25, CL: 15 },
      { CM: 20, WF: 15, WA: 10 },
      { UN: 25, MO: 15 },
      { EC: 25 },
    ],
    targetPairs: ["TR-CM", "TR-UN", "CM-UN"],
  },
  // Confirmation questions
  {
    id: "confirm_classical",
    question: "What appeals most about classical education?",
    options: [
      "Training the mind through rigorous study",
      "The great conversation across centuries",
      "Clear structure and progression",
      "Actually, I prefer a gentler approach",
    ],
    scoreDeltas: [
      { CL: 20, TR: 10 },
      { CL: 25 },
      { TR: 20, CL: 5 },
      { CM: 20, WF: 15, CL: -10 },
    ],
    targetPairs: ["CL-confirm"],
  },
  {
    id: "confirm_cm",
    question: "What draws you to Charlotte Mason?",
    options: [
      "Narration and living books",
      "Nature study and short lessons",
      "The philosophy of the whole child",
      "Actually, I want less structure",
    ],
    scoreDeltas: [
      { CM: 25 },
      { CM: 20, NB: 10 },
      { CM: 15, WA: 10 },
      { UN: 20, WF: 15, CM: -10 },
    ],
    targetPairs: ["CM-confirm"],
  },
];

// ============================================================
// SCORING FUNCTIONS
// ============================================================

/**
 * Apply score deltas to current scores
 */
export function applyScoreDeltas(
  scores: PhilosophyScores,
  deltas: ScoreDeltas
): PhilosophyScores {
  const newScores = { ...scores };
  for (const [tag, delta] of Object.entries(deltas)) {
    const key = tag as PhilosophyTag;
    newScores[key] = Math.max(0, (newScores[key] || 0) + (delta || 0));
  }
  return newScores;
}

/**
 * Get sorted philosophy entries by score (descending)
 */
export function getSortedPhilosophies(
  scores: PhilosophyScores
): { tag: PhilosophyTag; score: number }[] {
  return ALL_PHILOSOPHIES
    .map((tag) => ({ tag, score: scores[tag] }))
    .sort((a, b) => b.score - a.score);
}

/**
 * Calculate confidence based on score spread
 * Confidence = how decisively top score leads
 */
export function calculateConfidence(scores: PhilosophyScores): number {
  const sorted = getSortedPhilosophies(scores);
  if (sorted.length < 2) return 100;

  const top = sorted[0].score;
  const second = sorted[1].score;

  if (top === 0) return 0;

  // Confidence based on gap between top and second
  // If top=70, second=30, gap=40, confidence = 70 + (40/2) = 90
  const gap = top - second;
  return Math.min(100, Math.round(top + gap / 2));
}

/**
 * Find ambiguous pairs (philosophies within 15 points of each other in top 3)
 */
export function findAmbiguousPairs(scores: PhilosophyScores): string[] {
  const sorted = getSortedPhilosophies(scores).slice(0, 4);
  const pairs: string[] = [];

  for (let i = 0; i < sorted.length - 1; i++) {
    for (let j = i + 1; j < sorted.length; j++) {
      const gap = sorted[i].score - sorted[j].score;
      if (gap <= 15 && sorted[j].score > 10) {
        pairs.push(`${sorted[i].tag}-${sorted[j].tag}`);
      }
    }
  }

  return pairs;
}

/**
 * Select next question based on ambiguous pairs (information gain)
 */
export function selectNextQuestion(
  scores: PhilosophyScores,
  askedQuestionIds: string[]
): QuestionBankEntry | null {
  const ambiguousPairs = findAmbiguousPairs(scores);

  // Find questions that target these ambiguous pairs
  const candidates = QUESTION_BANK.filter(
    (q) =>
      !askedQuestionIds.includes(q.id) &&
      q.targetPairs.some((pair) =>
        ambiguousPairs.some((ambig) =>
          pair.includes(ambig.split("-")[0]) || pair.includes(ambig.split("-")[1])
        )
      )
  );

  // Return first matching candidate (could add more sophisticated selection)
  if (candidates.length > 0) {
    return candidates[0];
  }

  // Fallback: return any unasked question
  const remaining = QUESTION_BANK.filter(
    (q) => !askedQuestionIds.includes(q.id)
  );
  return remaining.length > 0 ? remaining[0] : null;
}

/**
 * Derive final quiz result from scores
 */
export interface QuizResultWithScores {
  primary: {
    tag: PhilosophyTag;
    name: string;
    description: string;
    score: number;
  };
  secondary: {
    tag: PhilosophyTag;
    name: string;
    score: number;
  }[];
  confidence: number;
  scores: PhilosophyScores;
}

export function deriveResult(scores: PhilosophyScores): QuizResultWithScores {
  const sorted = getSortedPhilosophies(scores);
  const primary = sorted[0];

  // Secondary: next 2-3 philosophies with score > 20
  const secondary = sorted
    .slice(1, 4)
    .filter((p) => p.score > 20)
    .map((p) => ({
      tag: p.tag,
      name: PHILOSOPHY_NAMES[p.tag],
      score: p.score,
    }));

  return {
    primary: {
      tag: primary.tag,
      name: PHILOSOPHY_NAMES[primary.tag],
      description: PHILOSOPHY_DESCRIPTIONS[primary.tag],
      score: primary.score,
    },
    secondary,
    confidence: calculateConfidence(scores),
    scores,
  };
}

/**
 * Normalize scores to percentages (for display)
 */
export function normalizeScoresToPercentages(
  scores: PhilosophyScores
): PhilosophyScores {
  const total = Object.values(scores).reduce((sum, s) => sum + s, 0);
  if (total === 0) return scores;

  const normalized = { ...scores };
  for (const tag of ALL_PHILOSOPHIES) {
    normalized[tag] = Math.round((scores[tag] / total) * 100);
  }
  return normalized;
}
