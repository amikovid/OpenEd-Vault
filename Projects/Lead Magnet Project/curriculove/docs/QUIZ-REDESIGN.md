# Curriculove Quiz Redesign

**Purpose:** Document current state, proposed changes, and architecture for review.

---

## Current State

### How It Works Now

1. **Fixed opener**: "What draws you most to homeschooling?" with 5 options
2. **Agent decides next questions**: Claude Haiku uses tool-calling to generate follow-ups
3. **Confidence threshold**: Quiz ends when agent is 80%+ confident in primary philosophy
4. **Result**: Returns `{ primary: "MO", confidence: 85, secondary: ["CM"], reasoning: "..." }`
5. **No scores**: No running tally of philosophy scores - agent reasons from conversation history
6. **No result screen**: Goes directly to curriculum swipe cards

### Current Opener Options

```
1. "A rigorous, classical education"        → CL, TR (ambiguous)
2. "Letting my child lead their learning"   → UN, MO (ambiguous)
3. "Faith woven through everything"         → FB (clear)
4. "Nature, wonder, and real experiences"   → WF, NB, CM (ambiguous - 3 philosophies!)
5. "Freedom to mix whatever works best"     → EC (clear)
```

### Problems

1. **Option 4 maps to 3 philosophies** - Not discriminating enough
2. **Missing coverage**: WA, PB, MS never have a clear entry point
3. **No percentages**: User sees "You're a Montessori!" not a breakdown
4. **No result screen**: Missing the "aha moment" of seeing their profile
5. **Agent reasoning is opaque**: We trust Claude but can't see score evolution
6. **Early termination**: Quiz often ends in 3-4 questions (too fast?)

---

## The 12 Philosophies

| Tag | Name | Core Signal |
|-----|------|-------------|
| CL | Classical | Great Books, Latin, Socratic, trivium |
| CM | Charlotte Mason | Living books, narration, short lessons, nature notebooks |
| TR | Traditional | Textbooks, grades, tests, standards |
| MO | Montessori | Prepared environment, child chooses work |
| WA | Waldorf | Rhythm, imagination, delayed academics, handwork |
| UN | Unschooling | No curriculum, child-led, radical trust |
| WF | Wild + Free | Wonder, nature, beauty, community |
| NB | Nature-Based | Forest school, outdoor-focused, risky play |
| PB | Project-Based | Real problems, authentic products |
| EC | Eclectic | Mix and match, pragmatic |
| MS | Microschool | Learning pods, co-ops, shared teaching |
| FB | Faith-Based | Faith integrated throughout |

### Philosophy Clusters (by similarity)

**Structure-Oriented:**
- CL, TR, CM (all have clear methodology, parent-guided)

**Freedom-Oriented:**
- UN, WF, NB (all value nature/freedom, less structure)

**Method-Oriented:**
- MO, WA, PB (specific approaches to how children learn)

**Practical:**
- EC, MS (pragmatic, what works)

**Values-Based:**
- FB (can combine with any other philosophy)

---

## Proposed Changes

### 1. Redesigned Opener (Maximum Orthogonality)

**Question:** "Which best describes your homeschool vision?"

```
1. "Great Books, classics, rigorous academics"     → CL (clear)
2. "Living books, nature study, gentle pace"       → CM, WF, NB cluster
3. "Faith and character at the center"             → FB (clear)
4. "Child-led, following their passions"           → UN, MO cluster
5. "Flexible structure - what works for us"        → TR, EC, PB, MS cluster
```

**Why this is better:**
- Each option maps to a tighter cluster (1-4 philosophies max)
- Clear entry points for all 12 philosophies
- Options 1 and 3 give HIGH-confidence signals
- Options 2, 4, 5 require follow-up but narrow the field

### 2. Guided Second Question (Based on Opener)

Instead of letting the agent free-form, we provide a **structured follow-up** for each opener choice:

**If Option 1 (Classics):**
```
"What's most important in that rigorous education?"
- "Wisdom and virtue from great thinkers"     → CL
- "Academic skills for college readiness"     → TR
- "Both - rigorous AND faith-centered"        → CL + FB
- "Actually, I want more flexibility..."      → EC (pivot)
```

**If Option 2 (Living books, nature):**
```
"What draws you to this gentle approach?"
- "Charlotte Mason's method - narration, copywork"  → CM
- "Wonder and beauty, less method"                  → WF
- "Being outdoors as much as possible"              → NB
- "Protecting childhood imagination"                → WA
```

(Similar for Options 3, 4, 5)

### 3. Philosophy Score Tracking

Instead of agent-only reasoning, maintain running scores:

```typescript
interface PhilosophyScores {
  CL: number;  // 0-100
  CM: number;
  TR: number;
  MO: number;
  WA: number;
  UN: number;
  WF: number;
  NB: number;
  PB: number;
  EC: number;
  MS: number;
  FB: number;
}
```

Each answer updates scores:
```typescript
// Example: User picks "Living books, nature study, gentle pace"
scores.CM += 30;
scores.WF += 20;
scores.NB += 20;
scores.WA += 10;
```

### 4. Result Screen with Breakdown

After quiz completes, show:

```
┌─────────────────────────────────────────┐
│         Your Homeschool Profile         │
├─────────────────────────────────────────┤
│  Primary: Charlotte Mason (72%)         │
│                                         │
│  Secondary Matches:                     │
│    • Wild + Free (58%)                  │
│    • Nature-Based (45%)                 │
│                                         │
│  "You value living books, nature        │
│   study, and a gentle rhythm. You       │
│   believe education should be           │
│   beautiful and unhurried."             │
│                                         │
│  [See Matching Curricula →]             │
└─────────────────────────────────────────┘
```

### 5. Minimum Questions (Reality Check)

Add practical questions after philosophy is determined:
- "How much time can you spend teaching each day?" (1hr/2-3hr/4+hr)
- "What's your curriculum budget?" ($/<$500/<$1000/$1000+)

This enables "aspiration vs reality" filtering - e.g., if someone wants Classical but only has 1 hour/day, we can flag that Classical typically requires 3+ hours.

---

## Architecture Options

### Option A: Guided Flow (Deterministic)

```
Opener → Guided Q2 (based on opener) → Agent generates Q3-6 → Result
```

**Pros:** Predictable, testable, guaranteed coverage
**Cons:** Less "magical", rigid structure

### Option B: Pure Agent (Current)

```
Opener → Agent decides all questions → Result
```

**Pros:** Flexible, can handle edge cases
**Cons:** Unpredictable, opaque reasoning, may miss key distinctions

### Option C: Hybrid (Recommended)

```
Opener → Guided Q2 → Agent refines with Q3-5 → Reality check Q6 → Result
```

**Architecture:**
1. **Questions 1-2**: Fixed, deterministic, maximum discrimination
2. **Questions 3-5**: Agent-generated to refine ambiguities
3. **Question 6+**: Reality check (time, budget, experience)
4. **Scores**: Updated after each question (hybrid of deterministic + agent reasoning)

```typescript
// After Q1 and Q2, we have initial scores
// Agent sees scores + conversation and decides:
// - Ask another question to resolve ambiguity?
// - Complete quiz if confident?

interface QuizState {
  history: QuestionAnswer[];
  scores: PhilosophyScores;
  confidence: number;  // Derived from score spread
  phase: "opener" | "guided" | "refinement" | "reality_check" | "complete";
}
```

---

## Score Calculation

### Initial Signals (from Q1 + Q2)

```typescript
const OPENER_SCORES: Record<string, Partial<PhilosophyScores>> = {
  "Great Books, classics, rigorous academics": { CL: 40, TR: 10 },
  "Living books, nature study, gentle pace": { CM: 30, WF: 20, NB: 20, WA: 10 },
  "Faith and character at the center": { FB: 50 },
  "Child-led, following their passions": { UN: 30, MO: 25, PB: 15 },
  "Flexible structure - what works for us": { EC: 25, TR: 20, PB: 15, MS: 10 },
};
```

### Confidence Calculation

```typescript
function calculateConfidence(scores: PhilosophyScores): number {
  const sorted = Object.values(scores).sort((a, b) => b - a);
  const top = sorted[0];
  const second = sorted[1];

  // Confidence = how much top score leads second
  // If top=70, second=50, confidence = 70 + (70-50)/2 = 80
  return Math.min(100, top + (top - second) / 2);
}
```

### Result Derivation

```typescript
function deriveResult(scores: PhilosophyScores): QuizResult {
  const entries = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const primary = entries[0];
  const secondary = entries.slice(1, 3).filter(([_, score]) => score > 30);

  return {
    primary: { tag: primary[0], score: primary[1] },
    secondary: secondary.map(([tag, score]) => ({ tag, score })),
    confidence: calculateConfidence(scores),
  };
}
```

---

## Open Questions

1. **How many questions?**
   - Current: 3-6 (often too few)
   - Proposed: 5-8 minimum?

2. **Should agent see scores?**
   - Pro: Can make informed decisions about what to ask
   - Con: Might over-rely on scores vs. conversation nuance

3. **How to handle pivots?**
   - User picks "Classical" then later says "actually I want flexibility"
   - Should we reset scores or accumulate?

4. **FB as overlay vs. primary?**
   - Faith-Based often combines with another philosophy
   - Should result be "FB + CM" or just "CM with faith integration"?

5. **Reality check questions:**
   - Ask before or after philosophy determination?
   - Use to filter recommendations or just to warn about conflicts?

---

## Files to Modify

| File | Change |
|------|--------|
| `src/lib/quiz-agent/prompt.ts` | Updated opener, add OPENER_SIGNALS |
| `src/lib/quiz-agent/agent.ts` | Add score tracking, guided Q2 logic |
| `src/app/api/quiz/answer/route.ts` | Return scores in response |
| `src/components/Quiz.tsx` | Track and display running scores? |
| `src/app/page.tsx` | Add "results" phase between quiz and recommendations |
| `src/components/Results.tsx` | NEW - Philosophy breakdown display |

---

## Success Criteria

1. **All 12 philosophies reachable** from opener through follow-ups
2. **User sees percentage breakdown**, not just "You're a X"
3. **5-8 questions** typical (not 3-4)
4. **Predictable discrimination**: Same answers → same result
5. **Reality check** catches aspiration vs. reality conflicts

---

*For review by higher-reasoning model (Codex 5.2)*
