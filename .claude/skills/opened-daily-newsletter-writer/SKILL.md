---
name: opened-daily-newsletter-writer
description: Creates Monday-Thursday OpenEd Daily newsletters (500-800 words) with Thought-Trend-Tool structure. Use when the user asks to create a daily newsletter, write daily content, or transform source material into newsletter segments. Not for Friday Weekly digests.
---

# OpenEd Daily Newsletter Writer

Creates Monday-Thursday daily newsletters (500-800 words) that challenge standardized education with contrarian angles and authentic voice.

**Not for:** Friday Weekly digests (use `weekly-newsletter-workflow`), social media only, or blog posts.

---

## Workflow Overview

```
Phase 1: Content Curation     → Source_Material.md
Phase 2: Angle Development    → Checkpoint_1.md (USER APPROVAL REQUIRED)
Phase 3: Newsletter Writing   → Newsletter_DRAFT.md
Phase 4: Social Media         → Optional repurposing
Phase 5: QA & Archive         → Newsletter_FINAL.md
```

---

## Phase 1: Content Curation

### Pull Staging Content from Notion

```
notion-search:
  query: "staging Thought Tool Trend"
  query_type: "internal"
  data_source_url: "collection://5d0c1ad8-e111-4162-91da-2cac9bd1269b"
  filters:
    created_date_range:
      start_date: "2025-10-01"
```

For specific items, use `notion-fetch` with the page ID.

### Segment Types

- **THOUGHT:** Contrarian takes, educational philosophy (~100-120 words)
- **TREND:** Current developments, research, data (~100-120 words)
- **TOOL:** Practical resources readers can use immediately (~100-120 words)

**Standard order:** THOUGHT → TREND → TOOL

### Sourcing Rules

**TOOLs:**
- Primary: [Tool Database](../../../Studio/Lead Magnet Project/OpenEd_Tool_Database.md)
- Must have concrete detail (stats, quotes, specific features)

**THOUGHTs:**
- Named individuals + direct quotes work best
- "Happy, not Fortune 500" > generic philosophy

**TRENDs:**
- Vary topics — avoid repeating "enrollment surge" every issue
- Look for: learning science, tech/AI, parent behavior, international comparisons
- Specific numbers + authoritative sources

**Avoid:**
- Heavy ESA/school choice policy content
- Federal tax programs
- State-specific policy details (unless story transcends the state)

### Create Working Folder

```bash
mkdir "Studio/OpenEd Daily/[YYYY-MM-DD] - [Brief Theme]/"
```

Create `Source_Material.md` with URLs, key quotes, and angle notes.

---

## Phase 2: Angle Development

🛑 **CHECKPOINT 1 - Do not proceed to Phase 3 without user approval.**

Create `Checkpoint_1_Angles.md` with:

### For Each Segment (3-4 angle options)

Ask yourself:
- What's the contrarian but obviously true take?
- How does this challenge standardized education?
- Would Sarah (our One True Fan) forward this?

### Subject Lines (10 options, 8-10 words max)

- 3-4 Curiosity-Based
- 3-4 Specificity-Based
- 2-3 Hybrid

### Preview Text

Formula: `[Specific claim]. [Context]. [Gap/tension]. PLUS: [bonus]`

Example: "Students who test themselves retain 80% more. Researchers have known this since the 1900s. Schools still don't do it. PLUS: an app that does."

### Checkpoint Template

```markdown
# Checkpoint 1: Angles & Structure - [Date]

## SUBJECT LINE OPTIONS
[Organize by type: Curiosity, Specificity, Hybrid]

## PREVIEW TEXT
[Draft]

## SEGMENT 1: [TITLE] (Type)
**Source:** [URL]
**Angle Options:** [3-4 options]
**Recommended:** [Which and why]

## SEGMENT 2: [TITLE] (Type)
[Same format]

## SEGMENT 3: [TITLE] (Type)
[Same format]

## ORTHOGONALITY CHECK
- [ ] Thought and Trend are distinct (not repetitive)
- [ ] Aligns with OpenEd beliefs
- [ ] Would Sarah forward this?
```

### User Feedback Notation

- `***` = preferred choice
- `<>` = extrapolate contextually
- `{question}` = answer directly
- `~~text~~` = delete

---

## Phase 3: Newsletter Writing

Create `Newsletter_DRAFT.md` after Checkpoint 1 approval.

### Opening Letter (~100-150 words)

**Structure:**
1. **Greeting:** "Greetings Eddies!", "Welcome Eddies!", or "Greetings!"
2. **Hook:** Story, startling statistic, contrarian question, or community milestone
3. **Pivot:** Connect to "opening up education" or today's specific value
4. **Tease:** Mention what's coming without summarizing
5. **Sign-off:** "Let's dive in."

**Opening Letter Examples:**

**Milestone/Community:**
> Greetings Eddies! It just came to my attention that the OpenEd Daily hit a new milestone: 20,000 subscribers! Rather than resting on our laurels, we take this as a sign of the growing appetite for trustworthy content related to the opening up of education. Onward & upward,

**Contrarian/Data:**
> Greetings! An education expert recently published something that's making a lot of parents nervous. Chad Aldeman looked at data from 250,000 kids across 1,400 schools and concluded: if your child isn't reading on track by kindergarten, don't wait. Act fast. The data sounds brutal, but is he interpreting it correctly? Let's dive in.

**Story-Driven:**
> Greetings! Ken Danford had spent six years teaching eighth-grade U.S. history when a colleague handed him The Teenage Liberation Handbook. In it, he found case studies of teens who left school and turned out... fine! That was 1996. He quit his job, and ever since, he's been running North Star—a physical community center where teens can legally homeschool. Let's dive in.

**Personal/Humorous:**
> Greetings Eddies! Did you know that OpenEd is on Instagram? While I may not be able to compete with top-tier influencer homeschool moms, we're always looking for new ways to share the message (even if that means putting on a smelly latex horse mask and A/B testing silly gimmicks until we find something that sticks).

**Parental Anxiety:**
> Greetings! A few months ago, an OpenEd parent reached out with a familiar dilemma. Her student had done 9th grade on the diploma path, but she was switching to non-diploma-seeking status. Yet she still had concerns: "I worry a lot about not following the traditional path." Society has pushed one linear path for so long. Except that path is just one among many. Let's dive in.

### Newsletter Structure

```markdown
**SUBJECT:** [From Checkpoint 1]
**PREVIEW:** [From Checkpoint 1]
---

[Opening Letter]
---

## [SEGMENT 1 TITLE - ALL CAPS]
[100-120 words]
---

## [SEGMENT 2 TITLE - ALL CAPS]
[100-120 words]
---

## [SEGMENT 3 TITLE - ALL CAPS]
[100-120 words]
---

That's all for today!

– Charlie (the OpenEd newsletter guy)

P.S. [Optional announcement]
```

### Format Requirements

- ❌ NO EMOJIS (non-negotiable)
- ✅ ALL CAPS H2 titles for segments
- ✅ **Bold** for key quotes/stats
- ✅ Hyperlinks throughout (not just at ends)
- ✅ `---` between sections
- ✅ 500-800 words total

---

## Segment Archetypes

Use these patterns to structure each segment type.

### THOUGHT Archetypes

**1. THE PARABLE (Best performer)**
Story with embedded lesson. Reader discovers the insight through narrative, not lecture.

> An old man lived alone. One day, local kids start throwing rocks at his house. Instead of yelling, he offers them a dollar each to come back tomorrow. They do. Next day, fifty cents. Then a quarter. Finally, he says he can't afford to pay them anymore. The kids, now feeling underpaid, never return.

Pattern: [Surprising situation] → [Counterintuitive action] → [Unexpected resolution] → [Reader draws conclusion]

**2. THE VIVID ANALOGY**
Maps education concepts onto familiar objects.

> Homeschooling used to mean a specific thing. Now it's like 'cable' - a bundle of options (co-ops, pods, tutors, online courses) that you assemble yourself.

Pattern: [Old understanding] → [New reality] → [Clarifying metaphor]

**3. THE SUBVERSIVE REFRAME**
Concede the conventional view, then flip it.

> Schools say they're preparing kids for the real world. But Ansel Adams's mother pulled him OUT of school precisely because the real world - nature, exploration, self-direction - couldn't be found inside one.

Pattern: [Acknowledge common belief] → [Historical example that subverts it] → [New frame]

**4. THE GUT-PUNCH QUOTE**
Let someone else deliver the insight.

> A mother shares her child's question: "Mommy, did you get distracted too?" after being pulled from traditional school.

Pattern: [Brief setup] → [Powerful quote] → [Let it land without over-explaining]

**5. THE ONE-LINER**
Single sentence that reframes everything. Rare, but devastating when done right.

> "Education isn't filling a bucket. It's lighting a fire."

Only use when you find genuine gold. Don't manufacture these.

### TREND Archetypes

**1. ALARMING STAT + HUMAN VOICE**
Data creates urgency; human story creates connection.

> 83% of parents believe schools aren't preparing kids for the AI economy. But talk to Maria Gonzales in Houston, and it's not abstract: "My son's math teacher spent three months on a unit the Khan Academy covered in two weeks."

Pattern: [Stat] → [Named person + location] → [Direct quote]

**2. FOLLOW THE SMART MONEY**
What are sophisticated actors actually doing?

> When you hear what Google executives are doing with their own kids' education, it makes you wonder what they know that they're not telling us.

Pattern: [High-status group] + [Surprising behavior] → [Implication]

**3. HISTORICAL PARALLEL**
Today's trend maps onto past movements.

Pattern: [Current trend] → [Historical parallel] → [What happened then] → [What it suggests now]

**4. CONCRETE CASE STUDY**
One family, one school, one district - told in detail.

> The Johnsons in Tampa have three kids in three different arrangements: one full-time homeschool, one hybrid with the district, one in a microschool. Here's how they make it work.

Pattern: [Family/school name] + [Location] + [Specific arrangement] + [How/why]

### TOOL Archetypes

**1. HOW-TO IN DISGUISE**
Don't describe the tool - show how to use it.

> Open your state's ESA application portal. Click 'Account Setup.' Before you fill in anything, do this first...

Pattern: [Immediate action verb] + [Specific first step] + [One useful tip]

**2. PERSONAL ENDORSEMENT**
You or a named source vouches for it.

> I've tried every transcript tool. This is the only one I still use three months later.

Pattern: [Credibility statement] + [Specific endorsement] + [Why it stuck]

**3. PROBLEM-SOLUTION FRAME**
Name the pain point first.

> Tracking learning across three different platforms is a nightmare. Until you discover [Tool], which...

Pattern: [Specific pain point] + [Tool introduction] + [How it solves it]

**4. "WE TRIED THIS" ENDORSEMENT**
Team/community validation.

> Three of our team members ran their curriculum through [Tool] last month. Here's what they found...

Pattern: [Group who tried it] + [Results/findings] → [Recommendation]

---

## Voice & Writing Style

### The Core Principle: Context + Substance

Every segment must deliver both:
1. **Context** - Who is this person? What did they do? Why should I care?
2. **Substance** - What's the actual insight, data, or takeaway?

**Bad:** "Justin Skycak runs Math Academy and has interesting ideas about education."

**Good:** "Justin Skycak runs Math Academy. His argument: schools use teaching methods that research abandoned decades ago - spaced repetition, retrieval practice, deliberate practice. Researchers have studied this since the 1900s. Schools just don't do it."

The second version delivers substance. The first is a placeholder.

### High-Density Prose

Every sentence should carry meaning. If a sentence exists only to create dramatic space for the next sentence, cut it.

**Low-density (bad):**
> A new MIT study just dropped.
> It claims LLM users "consistently underperform" on cognitive tests.
> AI doomers are obsessed with it.
> But here's the thing.
> None of them actually read the report.

**High-density (good):**
> A new MIT study claims LLM users "consistently underperform" on cognitive tests - and AI doomers are obsessed. Of course, none of them read the 206-page report, which reveals 18 college students had 20 minutes to write essays based on boring SAT prompts using only ChatGPT.

Six units became one. "But here's the thing" disappeared. The substance undermines the panic - that's the insight, delivered in the flow.

### Setup Phrases to Eliminate

These signal "the important part is coming" instead of delivering it:

- "Here's the thing..."
- "But here's the kicker..."
- "The clever part:"
- "What's interesting:"
- "Here's why that matters..."
- "Let that sink in."

If you need to tell the reader something is important, it probably isn't.

### Rhythm vs. Staccato

Short sentences are fine when they carry meaning:
> Take away their devices. Give them chores. Chalk. Challenges.

Short sentences are NOT fine when they're dramatic pauses:
> Schools aren't working. Not anymore. Not for most kids. And here's why.

**The test:** Does the short sentence carry meaning, or create a pause before meaning?

### The Vibe

A smart person talking to another smart person. No performance. No manipulation. Just: here's what happened, here's why it matters.

- **Trust the reader.** Don't tell them how to feel. Show them the thing.
- **Say less.** If you wrote it twice, delete one.
- **No fake questions.** "The top concerns?" is a crutch. Just tell them.
- **Short sentences are fine.** Fragments too. "Stomach aches gone." works.

---

## AI Tells to Avoid

### #1 CRITICAL - Correlative Constructions

This is the biggest AI tell. Never use:
- "X isn't just Y - it's Z"
- "It's not about X, it's about Y"
- "She wasn't X. She was Y."
- "The secret isn't X. It's Y."

Find another way. Rewrite the sentence. This pattern screams AI.

### Other AI Tells

- Rhetorical questions that set up your own point
- "Meanwhile:" at the start of paragraphs (use sparingly)
- Trying to sound punchy instead of actually being clear
- "X:" pattern before explanations ("The classic study:" / "The clever part:")
- Triple Threat Syndrome (grouping everything in threes)
- Empty enthusiasm ("Absolutely!", "Great question!")
- Thesaurus abuse ("utilize" instead of "use")
- Forced transitions ("Speaking of X..." / "On a related note...")
- Editorializing with judgments you can't back up

**The test:** Read it aloud. Does it sound like a person talking? Or like someone performing "good writing"?

---

## Tone: Curious > Accusatory

Notice things. Don't blame.

When critiquing institutions, observe the gap rather than attack. Let the reader draw conclusions.

**Bad:** "Schools prioritize fun over learning. Educators are failing our kids."

**Good:** "Skycak's point isn't that educators are villains. It's that maximizing learning isn't the only thing schools are trying to do, and maybe not even the main thing."

The reader will notice. You don't have to tell them how to feel.

### Don't Editorialize

Stick to what you can prove. Avoid sweeping claims like:
- "There weren't any protests. Just millions of families quietly making a different choice."
- "The institutions still don't get it."

If you can't cite it, soften it to a question or cut it.

**Instead of:** "Institutions keep waiting for families to come back. They're not coming back."

**Try:** "The question worth asking is what families discovered during those COVID years at home that made them decide not to go back."

The question form invites curiosity. The statement form invites argument.

---

## Headlines

Section titles (H2s) should create an information gap - reader needs to read to close it.

### Patterns That Work

- **The Label:** "THE GETTING BY TRAP" - names a phenomenon
- **The Stat:** "83% OF PARENTS AGREE" - specific number creates credibility
- **The Object:** "TOOL: CHOMPSAW" - clear, direct

### Avoid

- Generic labels ("WHAT WE LEARNED")
- Questions as headlines ("WHAT IF...?")
- Clickbait that doesn't deliver
- Puns that sacrifice clarity

**Counterintuitive framing works:** "The other kind of testing" challenges assumptions (testing = bad?) without revealing the answer.

---

## Transitions

Avoid clunky transitions between segments:
- ❌ "Speaking of Janssen..."
- ❌ "On a related note..."
- ❌ "While we're on the topic of..."

Jump straight into the new segment with a hook that stands alone. The `---` divider already signals a new section.

If segments are thematically connected, let the reader make the connection. Don't spell it out.

---

## Phase 4: Social Media (Optional)

For social repurposing, use the `social-content-creation` skill or create `Social_Media_Plan.md`.

---

## Phase 5: QA & Archive

### Final Checklist

- [ ] Segments are orthogonal (related but not repetitive)
- [ ] NO EMOJIS in body
- [ ] ALL CAPS H2 titles
- [ ] 500-800 words total
- [ ] All links work
- [ ] Voice sounds human, not performative
- [ ] Headlines create information gaps

### Archive

```bash
cp [working-folder]/Newsletter_FINAL.md daily-newsletter-workflow/examples/[YYYY-MM-DD]-newsletter.md
```

---

## Quick Reference

### Edition Types

**Type A (Integrated):** All 3 segments orbit a single theme. Use when you have one strong anchor piece.

**Type B (Modular):** Segments stand alone, connected by voice. Use when pieces don't naturally connect - don't force integration.

### Anti-Patterns

- **Forced cheerfulness:** "TGIF Eddies! Hope your week was AMAZING!" → Just "Greetings Eddies."
- **Transcript dump:** Pasting quotes with minimal synthesis → Extract one insight, reframe in your voice
- **Info overload:** 5 stats and 3 sources → One stat, one human voice, one implication
- **Fake question:** "What if schools actually taught kids to think?" → Just tell them
- **Setup-payoff crutch:** "The clever part: [explanation]" → Remove the label, write naturally

---

## Reference Files

**Content resources:**
- [Tool Database](../../../Studio/Lead Magnet Project/OpenEd_Tool_Database.md)
- [Content Queue](../../../Studio/OpenEd Daily/CONTENT_QUEUE.md)
- [OpenEd Identity Framework](../../Frameworks/Basic Context/OpenEd Identity Framework.md)

**Related skills:**
- `weekly-newsletter-workflow` - Friday digest
- `social-content-creation` - Social repurposing

---

## File Naming

Working folder: `Studio/OpenEd Daily/[YYYY-MM-DD] - [Theme]/`

Files:
- `Source_Material.md`
- `Checkpoint_1_Angles.md`
- `Newsletter_DRAFT.md`
- `Newsletter_FINAL.md` (only after approval)
