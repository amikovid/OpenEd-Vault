# Curriculum-Specific Targeting Campaign

**Concept:** Target people who already like specific curricula with personalized ads showing that curriculum, driving to Curriculove quiz.

**Status:** Concept phase
**Parent:** `Studio/Meta Ads/`
**Landing Page:** curricu.love

---

## The Idea

Facebook/Meta knows what curricula people follow, like, and engage with. We can create lookalike audiences around specific curriculum keywords - and because these are niche audiences, there's **less competition and lower CPMs**.

**The Hook:** Show users an ad featuring the curriculum they already love, positioned as:
- "Swipe to find more like this"
- "What kind of homeschooler are you?"
- "Love [Curriculum]? Find your perfect match"

**Why It Works:**
1. **Recognition:** User sees their favorite curriculum logo/screenshot - instant relevance
2. **Curiosity:** "This thing knows me... what else might it recommend?"
3. **Low friction:** Quiz is fun, not salesy
4. **Email capture:** Curriculove gates results behind email
5. **Less competition:** Niche curriculum keywords vs. broad "homeschool" targeting

---

## The Funnel

```
Meta Ad (curriculum-specific creative)
    ↓
Click → curricu.love
    ↓
Take Quiz (5-8 questions)
    ↓
See Philosophy Result ("You're Charlotte Mason!")
    ↓
[EMAIL GATE] → HubSpot (with state info)
    ↓
Swipe Curricula (216 matched options)
    ↓
See "FREE through OpenEd" badges
    ↓
Nurture sequence → Program application
```

---

## Creative Approach

### Templated Image Concept

**Visual:** Phone screen mockup showing:
- Curriculum logo or screenshot
- Curriculove UI elements (swipe cards, match percentage)
- "Find your match" or similar CTA

**Batch Processing:** Use Canva's bulk create feature
- One master template
- CSV with curriculum names, logos, taglines
- Generate 50-100 variations in one batch

### Ad Copy Variations

**For fans of [Curriculum]:**
```
Love [Curriculum]? 

There are 215 other curricula that might be perfect for your family.

Take the 2-minute quiz to find your matches.
```

**Discovery angle:**
```
What if there's a curriculum you've never heard of that's PERFECT for your kid?

Swipe through 216 options matched to your homeschool style.
```

**Quiz angle:**
```
What kind of homeschooler are you?

Take the quiz. Get matched with curricula that fit YOUR philosophy.

(It's like Tinder, but for curriculum)
```

---

## Target Curricula (Priority List)

**High-Volume Curricula (large followings):**
- Sonlight
- BJU Press
- Abeka
- Math-U-See
- Teaching Textbooks
- The Good and the Beautiful
- All About Reading
- Memoria Press
- Classical Conversations
- Easy Peasy All-in-One

**Philosophy-Aligned (OpenEd partners):**
- 49 curricula flagged as `isOpenEdVendor: true` in Curriculove database
- Prioritize these for "FREE through OpenEd" messaging

**Niche/Passionate Communities:**
- Charlotte Mason (Ambleside Online, Simply Charlotte Mason)
- Waldorf (Oak Meadow, Christopherus)
- Montessori (various)
- Classical (Memoria Press, Veritas, Classical Academic Press)

---

## Targeting Setup

### Audience Structure

**Option A: Interest-based targeting**
- Target users who like/follow specific curriculum pages
- Advantage: Direct relevance
- Disadvantage: Smaller audiences

**Option B: Lookalike audiences**
- Build lookalikes from people who engage with curriculum content
- Advantage: Larger scale
- Disadvantage: Less precise

**Option C: Hybrid**
- Interest targeting for initial test
- Build custom audiences from converters
- Create lookalikes from custom audiences
- Scale winners

### Recommended Test Structure

```
Campaign: Curriculum Targeting Test
├── Adset: Sonlight Fans
│   ├── Ad: Template A (logo focus)
│   ├── Ad: Template B (quiz angle)
│   └── Ad: Template C (discovery angle)
├── Adset: The Good and the Beautiful Fans
│   ├── Ad: Template A
│   ├── Ad: Template B
│   └── Ad: Template C
└── [Repeat for 5-10 curricula]
```

**Budget:** Start with $20-50/day per adset to gather data
**Duration:** 7-14 days minimum for statistical significance
**Success metric:** Cost per email capture (target: <$3)

---

## Production Workflow

### Phase 1: Template Creation (Day 1)
- [ ] Design master template in Canva (phone mockup + Curriculove UI)
- [ ] Create CSV with curriculum data (name, logo URL, tagline)
- [ ] Test bulk create with 5 curricula
- [ ] Refine template based on output

### Phase 2: Batch Production (Day 2)
- [ ] Pull logos/screenshots for priority curricula (20-30)
- [ ] Run bulk create in Canva
- [ ] Export all variations
- [ ] Write 3 ad copy variations per curriculum

### Phase 3: Campaign Setup (Day 3)
- [ ] Create campaign structure in Meta Ads Manager
- [ ] Set up audiences (interest targeting for each curriculum)
- [ ] Upload creatives
- [ ] Configure tracking (UTM parameters, pixel events)
- [ ] Set budgets and schedule

### Phase 4: Launch & Monitor (Ongoing)
- [ ] Launch initial test (5-10 curricula)
- [ ] Monitor daily for first week
- [ ] Kill underperformers at day 3-5
- [ ] Scale winners
- [ ] Add new curricula based on learnings

---

## Tracking & Attribution

### UTM Structure
```
utm_source=facebook
utm_medium=paid
utm_campaign=curriculum-targeting
utm_content=[curriculum-name]
```

### Pixel Events to Track
- `ViewContent` - Quiz page load
- `Lead` - Email submitted
- `CompleteRegistration` - Quiz completed (if separate event)

### Success Metrics

| Metric | Target | Why |
|--------|--------|-----|
| CPM | <$10 | Niche audiences should be cheaper |
| CTR | >1.5% | High relevance = high click rate |
| Cost per email | <$3 | Benchmark for lead magnets |
| Quiz completion rate | >60% | From email gate to full quiz |

---

## Connection to Retargeting

People who engage but don't convert become Pillar 2 audiences:
- Clicked ad but didn't complete quiz → Retarget with different angle
- Completed quiz but didn't apply → Retarget with "We saved your spot"
- Applied but didn't enroll → Pillar 1 audience

---

## Open Questions

1. **Logo permissions:** Do we need permission to use curriculum logos in ads? (Probably falls under fair use for comparison/recommendation, but worth checking)

2. **Landing page variation:** Should we create curriculum-specific landing pages? (e.g., curricu.love/sonlight that pre-selects their curriculum as a "favorite")

3. **State targeting:** Layer state targeting on top? (Only show to users in our 9 program states)

4. **Budget allocation:** How much of retargeting budget to allocate to this test?

---

## Next Steps

1. **Validate concept:** Create 3-5 sample ads manually, test organic engagement
2. **Build template:** Design Canva template for bulk creation
3. **Pull assets:** Collect logos/screenshots for top 20 curricula
4. **Small test:** $100-200 budget across 5 curricula
5. **Analyze:** Determine if CPL is competitive with other lead gen

---

*Created: 2026-01-20*
*Source: Elijah onboarding call - Charlie's curriculum-specific targeting idea*
