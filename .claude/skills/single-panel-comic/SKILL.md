---
name: single-panel-comic
description: Create single-panel editorial comics critiquing standardized education. This skill should be used when generating comic ideas, writing captions, or producing visual prompts for OpenEd's social media. Follows the style of The Far Side, Bogert Creek, and New Yorker cartoons - dark, cerebral humor that makes people think.
---

# Single-Panel Comic Creator

Create single-panel editorial comics that critique standardized education through dark, cerebral humor. These comics build audience through shareability - they make people feel "seen" and provoke the "I need to send this to someone" response.

## When to Use This Skill

- Generating new comic ideas for OpenEd social media
- Writing captions for comic concepts
- Creating image prompts for comic generation
- Brainstorming variations on existing themes

## Core Philosophy

### The Humor Style

Draw from three masters:

**The Far Side (Gary Larson):** Absurdist situations rendered matter-of-factly. Animals in human situations. The unexpected made mundane.

**Bogert Creek (Derek Evernden):** Dark, cerebral single-panel gags. "Most of my humor is based on the fear of the sky falling, compounded by looking stupid as it happens."

**New Yorker Cartoons:** Understated observational humor. The caption does work the image doesn't. Detached irony - characters unaware of the absurdity.

### What Makes These Comics Work

1. **One pivotal moment** - A freeze-frame that implies a whole story
2. **The "aha" rhythm** - Just enough information to get the joke, not so much it's handed to them
3. **Characters taking absurdity seriously** - The bureaucrat, the teacher, the system - all earnest
4. **Dark without being mean** - Laughing at systems, not people
5. **The send factor** - Makes people think "I need to share this"

### Rules to Follow

- No swearing or sexual humor
- No puns (cheap laughs)
- No overtly "relatable" millennial humor
- No political figures (ideas, not people)
- Dark is fine, cruel is not

---

## Workflow

### Step 1: Generate Comic Ideas

When asked for comic ideas, generate 5-8 concepts using the formulas in `references/comic-formulas.md`.

Each idea should be:
- **One sentence** describing the visual scene
- **One line of dialogue or caption** (if applicable)
- **Tight enough to picture immediately**

**Format:**

```
**[Title/Label]**
[Scene description in one sentence]. [Caption or dialogue in quotes].
```

**Example:**

```
**"The Certification"**
Socrates teaching students under a tree, pointing at the sky. A bureaucrat taps his shoulder: "I'm going to need to see your state certification."
```

### Step 2: Refine the Winner

Once the user selects a concept, refine it:

1. **Sharpen the visual** - What exactly is in the frame? Remove anything unnecessary.
2. **Perfect the caption** - Apply the caption formulas. Usually shorter is better.
3. **Check the rhythm** - Read it aloud. Does the reveal land?
4. **Test the send factor** - Would someone screenshot this and text it to a friend?

### Step 3: Generate the Image Prompt

Convert the refined concept into an image prompt using the visual style from `references/visual-style.md`.

**Prompt structure:**

```
A single-panel editorial cartoon in the style of [STYLE].

SCENE: [Exact description of what's in the frame]

CHARACTERS: [Who's in it, their expressions, what they're doing]

KEY VISUAL DETAIL: [The element that makes the joke land]

CAPTION: "[The caption in italic serif, centered below]"

STYLE NOTES: [Specific artistic direction]

FORMAT: 1:1 square, black ink on white/cream background
```

### Step 4: Generate via Image Prompt Generator

Hand off to the `image-prompt-generator` skill for actual generation. Specify:
- Use the New Yorker cartoon style (crosshatching, understated)
- 1:1 square format
- Black ink on white/cream background
- Caption in italic serif below

---

## Thematic Categories

Load `references/comic-formulas.md` for the complete formula library. Quick reference:

### The Credentialism Absurdity
Nature demonstrating competence vs. bureaucracy demanding papers.

- Lion with hunting scars in HR: "Impressive, but we require a certificate."
- Caveman teaching fire: bureaucrat wants teaching license

### The System as Factory
Education as literal industrial process - inputs, outputs, rejects.

- Cookie cutter factory: unique kids in, identical shapes out
- Graduation stage leads directly into meat grinder

### The Natural vs. The Institutional
Animals showing how learning should work vs. the absurdity of how we do it.

- Wolf dropping pup at class taught by sheep: "Predator Studies"
- Eagle dropping eaglet at flight class taught by penguin

### The Deathbed Regret
Existential perspective on wasted potential.

- Ed the horse: "I wish I spent more of my youth memorizing answers."
- Heaven's gates: "14,000 hours preparing for tests you immediately forgot."

### The Medical/Diagnostic
Education treated as medical condition or intervention.

- X-ray showing heart, imagination, wonder: "Good news - we can remove all of this before first grade."

### The Report Card Truth
The hidden grades behind the official ones.

- Two report cards: "A+ in COMPLIANCE" vs. crumpled "F in CURIOSITY"

---

## Caption Formulas

### The Deadpan Professional
Expert/authority figure stating the absurd as routine.
> "Good news - we can remove all of this before first grade."
> "I'm going to need to see your state certification."

### The Bureaucratic Clipboard
Forms, requirements, procedures applied to the natural.
> "It says here you spent 14,000 hours preparing for tests about things you immediately forgot."
> "Nice effort, but you're supposed to use the MLA format."

### The Deathbed Confession
What we'd regret if we truly saw clearly.
> "I wish I spent more of my youth memorizing answers."

### The Two-Door Choice
Visual metaphor for what we actually choose.
> "LEARNING" - dusty, cobwebbed. "CREDENTIALS" - line out the door.

---

## Resources

### references/
- `comic-formulas.md` - Complete library of idea generation formulas and thematic categories
- `visual-style.md` - Art direction specifications for image prompts

### Output Locations
- Save concepts to `Studio/Social Media/Comic Ideas.md`
- Save generated images to `Studio/Social Media/Comics/`

---

## Integration with Other Skills

- `image-prompt-generator` - For actual image generation (use New Yorker style)
- `opened-identity` - Ensure alignment with OpenEd values
- `text-content` - For accompanying social copy
- `ghostwriter` - For longer-form content inspired by comics

---

## Quality Checklist

Before finalizing any comic:

- [ ] Can you picture it immediately in one frame?
- [ ] Does the caption land with proper rhythm?
- [ ] Is it dark but not mean?
- [ ] Would Sarah (our audience) screenshot and share this?
- [ ] Does it critique the system, not individual people?
- [ ] Is there just enough info - not too much, not too little?
- [ ] Does it make you feel "seen" rather than just laugh?
