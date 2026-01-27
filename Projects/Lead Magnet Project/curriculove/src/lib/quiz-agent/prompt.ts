/**
 * Curriculove Quiz Agent - True Agentic Approach
 *
 * The agent REASONS about each answer to understand the person,
 * then decides what to ask next to distinguish between close philosophies.
 */

export const QUIZ_SYSTEM_PROMPT = `You are a quiz agent determining someone's homeschool philosophy. You ask short, punchy questions and reason about what their answers reveal.

## The 12 Philosophies

**Structure-Focused:**
- Classical (CL): Great Books, Latin, Socratic method, trivium
- Traditional (TR): Textbooks, grades, tests, school-at-home
- Charlotte Mason (CM): Living books, short lessons, narration, nature study

**Freedom-Focused:**
- Unschooling (UN): Child-led, no curriculum, radical trust
- Wild + Free (WF): Wonder-based, nature, beauty, community
- Nature-Based (NB): Forest school, outdoor focus, risky play

**Method-Focused:**
- Montessori (MO): Prepared environment, child chooses work, hands-on materials
- Waldorf (WA): Rhythm, imagination, no early academics, handwork
- Project-Based (PB): Real problems, authentic products, interdisciplinary

**Practical:**
- Eclectic (EC): Mix and match, pragmatic, whatever works
- Microschool (MS): Small group, shared teaching, hybrid

**Values-Driven:**
- Faith-Based (FB): Faith integrated throughout, biblical worldview

## Your Behavior

1. **Ask short questions with short options** - 5-8 words per option max
2. **Make options ORTHOGONAL** - Each option should map to different philosophies, not overlap
3. **Reason about each answer** - What does this reveal? What's still unclear?
4. **Target ambiguity** - If CM and CL are close, ask something that distinguishes them
5. **No hypotheticals** - Ask about values, preferences, instincts - not "what would you do if your kid..."
6. **Confidence check** - Stop when you're 80%+ confident in primary philosophy

## Orthogonal Options

BAD (overlapping):
- "Follow my child's interests" → UN, MO, WF, CM (too many!)
- "Rich education" → CL, CM, TR (vague)

GOOD (distinct clusters):
- "Let them explore freely" → UN
- "Guide with great books" → CL, CM
- "Structured daily lessons" → TR
- "Hands-on, self-directed" → MO

## Question Style

GOOD: "What matters most in education?"
- Mastering the classics
- Following curiosity
- Building character
- Real-world skills

BAD: "Your 8-year-old wants to skip math to build a cardboard city. How do you respond?"
- [paragraph A]
- [paragraph B]
- [paragraph C]

## Output Format

Always respond with JSON:

For questions:
{
  "type": "question",
  "question": "Short question text?",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "reasoning": "Why I'm asking this - what I'm trying to distinguish"
}

For completion:
{
  "type": "result",
  "primary": "CL",
  "confidence": 85,
  "secondary": ["TR", "CM"],
  "reasoning": "Summary of what their answers revealed"
}
`;

export const OPENER_QUESTION = {
  question: "Which best describes your homeschool vision?",
  options: [
    "Great Books, classics, rigorous academics",     // → CL (clear signal)
    "Living books, nature study, gentle pace",       // → CM, WF, NB cluster
    "Faith and character at the center",             // → FB (clear signal)
    "Child-led, following their passions",           // → UN, MO cluster
    "Flexible structure - what works for us"         // → TR, EC, PB, MS cluster
  ]
};

// What each opener answer tells us and what we need to distinguish next
export const OPENER_SIGNALS: Record<number, {
  strongSignals: string[];
  possibleSignals: string[];
  nextQuestion: string;
  distinguishingOptions: string[];
}> = {
  0: { // "Great Books, classics, rigorous academics"
    strongSignals: ["CL"],
    possibleSignals: ["TR", "FB"],
    nextQuestion: "What's most important in that rigorous education?",
    distinguishingOptions: [
      "Wisdom and virtue from great thinkers",     // → CL
      "Academic skills for college readiness",     // → TR
      "Both - rigorous AND faith-centered",        // → CL + FB
      "Actually, I want more flexibility..."       // → EC (pivot)
    ]
  },
  1: { // "Living books, nature study, gentle pace"
    strongSignals: ["CM"],
    possibleSignals: ["WF", "NB", "WA"],
    nextQuestion: "What draws you to this gentle approach?",
    distinguishingOptions: [
      "Charlotte Mason's method - narration, copywork",  // → CM
      "Wonder and beauty, less method",                  // → WF
      "Being outdoors as much as possible",              // → NB
      "Protecting childhood imagination",                // → WA
    ]
  },
  2: { // "Faith and character at the center"
    strongSignals: ["FB"],
    possibleSignals: ["CL", "TR", "CM", "EC"],
    nextQuestion: "How much structure do you want alongside faith?",
    distinguishingOptions: [
      "Very structured - classical Christian curriculum",  // → FB + CL
      "Structured - textbooks with biblical worldview",    // → FB + TR
      "Gentle - faith with living books and nature",       // → FB + CM
      "Flexible - faith integrated into whatever works",   // → FB + EC
    ]
  },
  3: { // "Child-led, following their passions"
    strongSignals: ["UN"],
    possibleSignals: ["MO", "PB", "WF"],
    nextQuestion: "How much do you want to guide vs. let them explore?",
    distinguishingOptions: [
      "Fully child-led - no curriculum, radical trust",    // → UN
      "Prepared environment - they choose from options",   // → MO
      "Project-based - real problems they care about",     // → PB
      "Wonder-based with gentle parent guidance",          // → WF
    ]
  },
  4: { // "Flexible structure - what works for us"
    strongSignals: ["EC"],
    possibleSignals: ["TR", "PB", "MS"],
    nextQuestion: "What does 'flexible structure' look like for you?",
    distinguishingOptions: [
      "Online/video curriculum with clear lessons",        // → TR
      "Mix of curricula - different for each subject",     // → EC
      "Project-based learning with some structure",        // → PB
      "Learning pod or co-op with other families",         // → MS
    ]
  }
};

// Philosophy disambiguation - which questions help distinguish close pairs
export const DISAMBIGUATION_HINTS: Record<string, string> = {
  "CL-CM": "Ask about structure vs. delight, or Great Books vs. living books",
  "CL-TR": "Ask about intellectual formation vs. career prep, or classics vs. standards",
  "UN-WF": "Ask about radical trust vs. curated wonder, or no structure vs. gentle rhythm",
  "UN-MO": "Ask about environment - none vs. carefully prepared",
  "UN-EC": "Ask about philosophical commitment vs. pragmatism",
  "MO-WA": "Ask about early academics vs. play-first, or materials vs. imagination",
  "CM-WF": "Ask about method (narration, copywork) vs. pure wonder",
  "FB-any": "Ask about faith integration - is it central or alongside?",
  "TR-EC": "Ask about following standards vs. picking what works",
  "PB-UN": "Ask about teacher guidance in projects vs. pure child-led",
};
