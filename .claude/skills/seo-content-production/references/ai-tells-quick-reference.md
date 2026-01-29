# AI Tells Quick Reference

Patterns that make writing sound AI-generated. Apply ruthlessly to ALL SEO content.

---

## Priority 1: Correlative Constructions (Kill on Sight)

The #1 AI tell. Never use:

- "X isn't just Y - it's Z"
- "It's not about X, it's about Y"
- "X didn't Y. It Z."
- "The goal isn't X - it's Y"

**Fix:** Find another way to make the point. Usually the "Y" part is the real insight.

---

## Priority 2: Forbidden Words

| Kill | Replace With |
|------|--------------|
| delve, dive into, dig into | explore, examine, look at |
| comprehensive, robust | thorough, complete |
| utilize | use |
| leverage (as verb) | use, apply |
| crucial, vital, essential | important, key |
| unlock, unleash, supercharge | enable, improve |
| game-changer, revolutionary | significant, notable |
| landscape, navigate | environment, work through |
| tapestry, multifaceted, myriad | varied, many, diverse |
| foster, facilitate, enhance | support, help, improve |
| realm, paradigm, synergy | area, approach, combination |
| embark, journey (for processes) | start, begin, process |
| plethora, bevy | many, several |
| nuanced, intricate, seamless | subtle, complex, smooth |
| cutting-edge | modern, current |

---

## Priority 3: Forbidden Phrases

**Opening patterns:**
- "In today's fast-paced world..."
- "In today's digital age..."
- "In the ever-evolving..."

**Filler phrases:**
- "It's important to note that..."
- "When it comes to..."
- "In order to..." (just use "to")
- "Without further ado"
- "At the end of the day"
- "It goes without saying"

**Setup phrases:**
- "The best part? ..."
- "The secret? ..."
- "Here's the thing..."
- "Let's be honest..."
- "And here's the kicker"
- "Enter: [thing]"

**Fake questions:**
- "Are you looking for..."
- "Want access?"
- "Ready to level up?"
- "Sound familiar?"
- "Curious?"

**Ending patterns:**
- "In conclusion"
- "In summary"
- "Let that sink in"
- "Now more than ever"

**Empty enthusiasm:**
- "Absolutely!"
- "Great question!"
- "You're absolutely right!"

---

## Priority 4: Structural Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Triple Threat Syndrome | AI groups everything in threes | Vary: use 2, 4, 5 items |
| Perfect Parallelism | Every bullet same length | Mix it up |
| Hedge Stack | "While X, it's important to consider Y, but also Z" | Commit to a position |
| Fake Objectivity | "Some experts say... others believe..." | Take a stance |
| Summary Sandwich | Intro summarizes, body covers, conclusion re-summarizes | Add new value in conclusion |
| Empty Transitions | "Now that we've covered X, let's move on to Y" | Cut or make meaningful |
| Staccato | "No fluff. No filler. Just results." | Write normally |
| Negation Structure | "No X. No Y. Just Z." | Positive framing |

---

## Priority 5: Formatting

- Use hyphens with spaces - like this
- Never em dashes (—)
- No emojis in body content
- No bold for emphasis in articles

---

## The Detection Checklist

Before publishing, verify:

- [ ] No correlative constructions
- [ ] No forbidden words
- [ ] No forbidden phrases
- [ ] Not everything in threes
- [ ] At least one personal opinion stated directly
- [ ] At least one specific number from real experience
- [ ] At least one admission of limitation or uncertainty
- [ ] Sentence lengths vary (some under 5 words, some over 20)
- [ ] Would I say this out loud to a smart friend?
- [ ] Does it sound like a specific person, or a committee?

---

## Quick Grep Commands

```bash
# Forbidden words
grep -inE "delve|comprehensive|crucial|leverage|landscape|journey|tapestry|myriad|seamless" DRAFT*.md

# Correlative constructions
grep -inE "isn't just|not just .* - it's|It's not about .* it's about" DRAFT*.md

# Em dashes (should be hyphens with spaces)
grep -n "—" DRAFT*.md

# Setup phrases
grep -inE "The best part\?|Here's the thing|Let's be honest" DRAFT*.md
```

---

*Updated: 2026-01-29*
