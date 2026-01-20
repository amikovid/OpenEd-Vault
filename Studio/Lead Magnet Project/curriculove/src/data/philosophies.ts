// Philosophy tags used throughout the system
export type PhilosophyTag =
  | "CL" // Classical
  | "CM" // Charlotte Mason
  | "MO" // Montessori
  | "WA" // Waldorf/Steiner
  | "TR" // Traditional
  | "UN" // Unschooling
  | "WF" // Wild + Free
  | "PB" // Project-Based
  | "MS" // Microschool/Pod
  | "NB" // Nature-Based/Forest School
  | "EC" // Eclectic
  | "FB"; // Faith-Based

export interface Philosophy {
  tag: PhilosophyTag;
  name: string;
  category: "core" | "movement" | "values";
  coreDistinction: string;
  keyIndicators: string[];
  keyResources: string[];
  resultDescription: string;
  shareText: string;
}

export const PHILOSOPHIES: Record<PhilosophyTag, Philosophy> = {
  // Core Philosophical Approaches
  CL: {
    tag: "CL",
    name: "Classical",
    category: "core",
    coreDistinction:
      "Trivium (grammar/logic/rhetoric), Great Books, Latin, Western canon",
    keyIndicators: [
      "Values formal logic and rhetoric",
      "Interested in Latin or Greek",
      "Appreciates Great Books curriculum",
      "Sees education as training in wisdom and virtue",
      "Structures learning by developmental stages",
    ],
    keyResources: [
      "Classical Conversations",
      "Veritas Press",
      "Memoria Press",
      "Well-Trained Mind",
    ],
    resultDescription:
      "You believe in the power of great ideas and the time-tested methods of Western education.",
    shareText:
      "I got Classical! Apparently I believe in wisdom, virtue, and a little Latin. 📚",
  },

  CM: {
    tag: "CM",
    name: "Charlotte Mason",
    category: "core",
    coreDistinction:
      "Living books, nature study, short lessons (15-20 min), narration",
    keyIndicators: [
      "Prefers narrative books over textbooks",
      "Values daily nature time",
      "Believes in short, focused lessons",
      "Uses narration to check understanding",
      "Appreciates beauty and art in education",
    ],
    keyResources: [
      "Ambleside Online",
      "Simply Charlotte Mason",
      "A Gentle Feast",
      "Charlotte Mason Original Writings",
    ],
    resultDescription:
      "You value living books, nature study, and the belief that education is an atmosphere, a discipline, a life.",
    shareText:
      "I got Charlotte Mason! Time for nature walks and living books. 🌿",
  },

  MO: {
    tag: "MO",
    name: "Montessori",
    category: "core",
    coreDistinction:
      "Prepared environment, specific materials, child chooses work",
    keyIndicators: [
      "Values child-led learning within structure",
      "Appreciates hands-on materials",
      "Believes children learn through doing",
      "Supports mixed-age learning",
      "Trusts children to choose their work",
    ],
    keyResources: [
      "Montessori Services",
      "AMI (Association Montessori Internationale)",
      "Montessori for Today",
    ],
    resultDescription:
      "You believe in following the child within a carefully prepared environment full of purposeful materials.",
    shareText:
      "I got Montessori! The prepared environment awaits. 🎨",
  },

  WA: {
    tag: "WA",
    name: "Waldorf/Steiner",
    category: "core",
    coreDistinction:
      "No academics before 7, imagination first, rhythm, handwork, storytelling",
    keyIndicators: [
      "Values imagination and play in early years",
      "Believes in protecting childhood",
      "Appreciates rhythm and routine",
      "Values handwork and crafts",
      "Limits early academics intentionally",
    ],
    keyResources: [
      "Oak Meadow",
      "Waldorf Essentials",
      "Christopherus",
      "Live Education",
    ],
    resultDescription:
      "You believe in protecting childhood, nurturing imagination, and following natural developmental rhythms.",
    shareText:
      "I got Waldorf! Imagination first, academics later. ✨",
  },

  TR: {
    tag: "TR",
    name: "Traditional",
    category: "core",
    coreDistinction: "School-at-home, textbooks, grade levels, tests, structured",
    keyIndicators: [
      "Values clear structure and routine",
      "Appreciates grade-level benchmarks",
      "Comfortable with textbooks and tests",
      "Wants documented progress",
      "Prepares for conventional academic success",
    ],
    keyResources: ["Abeka", "Saxon Math", "BJU Press", "Time4Learning"],
    resultDescription:
      "You value structure, clear expectations, and the security of knowing your children are on track.",
    shareText:
      "I got Traditional! Textbooks, checklists, and confidence. ✓",
  },

  UN: {
    tag: "UN",
    name: "Unschooling",
    category: "core",
    coreDistinction:
      "Radical trust, no curriculum, life as learning, child-directed entirely",
    keyIndicators: [
      "Trusts children to direct their learning",
      "Sees life as the curriculum",
      "Comfortable without formal structure",
      "Believes intrinsic motivation is key",
      "Values freedom over coverage",
    ],
    keyResources: [
      "John Holt books",
      "Peter Gray's Free to Learn",
      "Sandra Dodd",
      "Pam Laricchia",
    ],
    resultDescription:
      "You trust that learning happens naturally when children follow their interests in a rich environment.",
    shareText:
      "I got Unschooling! Life is the curriculum. 🌍",
  },

  // Named Movements & Communities
  WF: {
    tag: "WF",
    name: "Wild + Free",
    category: "movement",
    coreDistinction:
      "Nature-centered wonder, outdoor learning, freedom, community",
    keyIndicators: [
      "Values outdoor learning and nature",
      "Appreciates beauty and wonder",
      "Wants freedom with gentle structure",
      "Values community with like-minded families",
      "Loves the aesthetic of natural learning",
    ],
    keyResources: [
      "The Call of the Wild + Free (book)",
      "Wild + Free community",
      "Wild + Free curriculum",
    ],
    resultDescription:
      "You believe in cultivating wonder through nature, beauty, and the freedom to follow curiosity.",
    shareText:
      "I got Wild + Free! Wonder, nature, and the great outdoors. 🦋",
  },

  PB: {
    tag: "PB",
    name: "Project-Based",
    category: "movement",
    coreDistinction:
      "Real-world problems, authentic products, student agency",
    keyIndicators: [
      "Values learning through doing",
      "Appreciates real-world application",
      "Wants children to create authentic products",
      "Believes in student-driven inquiry",
      "Comfortable with messy, non-linear learning",
    ],
    keyResources: ["Synthesis", "Maker education", "Acton Academy materials"],
    resultDescription:
      "You believe learning is most powerful when it solves real problems and creates real products.",
    shareText:
      "I got Project-Based! Learning by building and doing. 🛠️",
  },

  MS: {
    tag: "MS",
    name: "Microschool/Learning Pod",
    category: "movement",
    coreDistinction: "Small multi-age groups, shared teaching, community-based",
    keyIndicators: [
      "Values community learning",
      "Wants to share teaching responsibilities",
      "Appreciates multi-age groupings",
      "Interested in hybrid models",
      "Values both independence and structure",
    ],
    keyResources: ["Prenda", "KaiPod", "Acton Academy", "Microschool Revolution"],
    resultDescription:
      "You believe in the power of small learning communities where families share the journey.",
    shareText:
      "I got Microschool! Learning is better together. 👥",
  },

  NB: {
    tag: "NB",
    name: "Nature-Based/Forest School",
    category: "movement",
    coreDistinction: "Outdoor-focused, risky play, seasonal rhythms, minimal indoor",
    keyIndicators: [
      "Prioritizes outdoor time above all",
      "Values risky play and natural consequences",
      "Follows seasonal rhythms",
      "Minimizes indoor/screen time",
      "Believes nature is the best teacher",
    ],
    keyResources: [
      "1000 Hours Outside",
      "Forest School Association",
      "Scandinavian education models",
    ],
    resultDescription:
      "You believe that nature is the ultimate classroom and that children thrive outdoors.",
    shareText:
      "I got Nature-Based! The forest is calling. 🌲",
  },

  EC: {
    tag: "EC",
    name: "Eclectic",
    category: "movement",
    coreDistinction: 'Mix-and-match, customized per child, pragmatic "whatever works"',
    keyIndicators: [
      "Comfortable mixing approaches",
      "Adapts to each child's needs",
      "Pragmatic about what works",
      "Not attached to any single philosophy",
      "Values flexibility over consistency",
    ],
    keyResources: [
      "Cathy Duffy Reviews",
      "Homeschool curriculum reviews",
      "Eclectic homeschool communities",
    ],
    resultDescription:
      "You're the ultimate curator - taking the best from every approach to create something uniquely suited to your family.",
    shareText:
      "I got Eclectic! A little of this, a little of that. 🎯",
  },

  // Values-Based
  FB: {
    tag: "FB",
    name: "Faith-Based",
    category: "values",
    coreDistinction:
      "Faith integrated into all subjects, character formation, biblical worldview",
    keyIndicators: [
      "Integrates faith into all subjects",
      "Values character formation",
      "Wants biblical worldview in curriculum",
      "Appreciates Christian community",
      "Sees education as discipleship",
    ],
    keyResources: [
      "Classical Conversations",
      "Veritas Press",
      "Memoria Press",
      "Apologia",
      "The Good and the Beautiful",
    ],
    resultDescription:
      "You believe education is an opportunity to integrate faith into every subject and form character.",
    shareText:
      "I got Faith-Based! Education as discipleship. ✝️",
  },
};

// Philosophy disambiguation guide - helps Claude distinguish similar pairs
export const DISAMBIGUATION_PAIRS = [
  {
    pair: ["CM", "CL"],
    distinction: `
      Both value "great books" but mean different things:
      - CM: "Living books" = narrative-rich, engaging authors. Short 15-20 min lessons. Nature as equal priority. Narration over testing.
      - CL: "Great Books" = specific Western canon. Formal logic/rhetoric stages. Latin. More teacher-directed.

      Key distinguishing questions:
      - How do you assess if your child understood a book? (CM: narrate it back / CL: discuss + analyze)
      - How important is formal grammar and Latin? (CL prioritizes)
      - Is daily nature time essential? (CM: yes / CL: nice but not core)
    `,
  },
  {
    pair: ["MO", "WA"],
    distinction: `
      Both emphasize developmental stages but differ sharply:
      - MO: Child chooses work from prepared materials. Real-world focus. Reading/math when ready (often early).
      - WA: Teacher-led rhythms. Imagination before intellect. NO academics before 7. Fantasy and fairy tales central.

      Key distinguishing questions:
      - Your eager 4-year-old wants to learn to read. You... (MO: follow the child / WA: protect imagination)
      - Fairies and gnomes in education are... (WA: essential / MO: not emphasized)
      - Your child chooses their work from... (MO: prepared materials / WA: teacher-led rhythm)
    `,
  },
  {
    pair: ["UN", "EC"],
    distinction: `
      Spectrum of child-direction:
      - UN: Zero curriculum. Radical trust. No "should" for any subject.
      - EC: Parent curates mix of approaches. Still parent-directed in overall structure.

      Key distinguishing questions:
      - Your child hasn't done any math in 6 months. You... (UN: trust them / EC: gently introduce)
      - Who decides what subjects to cover? (UN: child entirely / EC: parent designs with child input)
    `,
  },
  {
    pair: ["TR", "CL"],
    distinction: `
      Both structured but different goals:
      - TR: Match grade-level standards, textbooks, tests. Prep for conventional success.
      - CL: Develop thinkers, great books, virtue, intellectual formation. Less concerned with grade levels.

      Key distinguishing questions:
      - Grade-level benchmarks are... (TR: essential / CL: less important than intellectual growth)
      - The goal of education is... (TR: career/college readiness / CL: wisdom and virtue)
    `,
  },
  {
    pair: ["WF", "NB"],
    distinction: `
      Both nature-focused but different emphasis:
      - WF: Aesthetic and community focus. Nature as one element of wonder-based learning. Instagram-friendly.
      - NB: Nature as THE primary environment. Risky play. Minimal indoor time. Scandinavian roots.

      Key distinguishing questions:
      - Where do you spend MOST of your school time? (NB: outdoors / WF: varies)
      - How do you feel about risky play? (NB: essential / WF: valued but not core)
    `,
  },
  {
    pair: ["CM", "WF"],
    distinction: `
      Both value nature and beauty but:
      - CM: Specific methodology - living books, narration, short lessons. Structured approach with flexibility.
      - WF: Community and aesthetic focus. More freedom-oriented. Less methodologically specific.

      Key distinguishing questions:
      - Do you follow a specific educational methodology? (CM: yes, Charlotte Mason / WF: more flexible)
      - How important is the homeschool community/aesthetic? (WF: central / CM: not emphasized)
    `,
  },
];

// Overlays - preferences that can apply to any philosophy
export interface Overlay {
  key: string;
  name: string;
  options: { value: string; label: string }[];
}

export const OVERLAYS: Overlay[] = [
  {
    key: "techStance",
    name: "Technology in Learning",
    options: [
      { value: "essential", label: "Essential tool" },
      { value: "supplement", label: "Helpful supplement" },
      { value: "minimal", label: "Minimal" },
      { value: "child-determined", label: "Child-determined" },
    ],
  },
  {
    key: "stemFocus",
    name: "STEM Priority",
    options: [
      { value: "high", label: "High priority" },
      { value: "balanced", label: "Balanced" },
      { value: "humanities", label: "Humanities-focused" },
    ],
  },
  {
    key: "budget",
    name: "Curriculum Budget",
    options: [
      { value: "$", label: "Free/minimal" },
      { value: "$$", label: "Moderate" },
      { value: "$$$", label: "Investment" },
      { value: "$$$$", label: "Premium" },
    ],
  },
  {
    key: "roadschooling",
    name: "Travel-Based Learning",
    options: [
      { value: "extensive", label: "We travel extensively" },
      { value: "occasional", label: "Occasional trips" },
      { value: "home-based", label: "Primarily home-based" },
    ],
  },
];

// Helper to get all philosophy tags
export const ALL_PHILOSOPHY_TAGS: PhilosophyTag[] = Object.keys(
  PHILOSOPHIES
) as PhilosophyTag[];

// Helper to get philosophy by tag
export function getPhilosophy(tag: PhilosophyTag): Philosophy {
  return PHILOSOPHIES[tag];
}

// Helper to find ambiguous pairs given current scores
export function findAmbiguousPairs(
  scores: Record<PhilosophyTag, number>,
  threshold: number = 15
): [PhilosophyTag, PhilosophyTag][] {
  const sorted = (Object.entries(scores) as [PhilosophyTag, number][])
    .sort(([, a], [, b]) => b - a)
    .slice(0, 4); // Top 4

  const pairs: [PhilosophyTag, PhilosophyTag][] = [];

  for (let i = 0; i < sorted.length - 1; i++) {
    for (let j = i + 1; j < sorted.length; j++) {
      const diff = sorted[i][1] - sorted[j][1];
      if (diff < threshold) {
        pairs.push([sorted[i][0], sorted[j][0]]);
      }
    }
  }

  return pairs;
}
