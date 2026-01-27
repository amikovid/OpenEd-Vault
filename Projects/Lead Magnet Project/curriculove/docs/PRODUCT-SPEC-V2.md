# Curriculove Product Spec v2

**Two workstreams:** AI-generated curriculum images + UI polish

---

## Workstream 1: AI-Generated Curriculum Images

### Goal
Generate unique hero images for all 146 curricula currently missing images.

### Visual Strategy

**Style:** Watercolor-line (ink linework with watercolor washes)
- Warm, approachable, hand-crafted feel
- Brand-integrated: subtle orange (#f24915) and blue (#03a4ea) accents woven into images
- No text in images (UI provides text overlay)

**Concept driver:** Curriculum name/brand identity
- Playful interpretation of the curriculum name
- "Beast Academy" = friendly math-loving monsters
- "Saxon Math" = structured, orderly visual elements
- "1000 Hours Outside" = nature immersion scene

**Format:** Square (1:1) for flexibility in cards and thumbnails

**Text legibility:** CSS gradient overlay on frontend (not baked into images)
- Allows adjustment without regenerating
- Consistent treatment across varying image brightness

### Generation Process

**Phase 1: Style validation (5 test images)**
1. Saxon Math - strong brand, structured
2. 1000 Hours Outside - nature-based, movement
3. Abeka - faith-based, traditional
4. Khan Academy - digital, free
5. Beast Academy - playful name, math

Handcraft prompts for each. Review results. Refine style guide.

**Phase 2: Bulk generation (141 remaining)**
Once style is validated, scale up:
- Group similar curricula (all math, all reading, etc.)
- Generate in batches
- Manual QA pass before integration

### Prompt Template (starting point)

```
Create a watercolor-line illustration for "[Curriculum Name]" - a homeschool curriculum.

CONCEPT: [Playful visual interpretation of the curriculum name/identity]

STYLE: Ink linework with soft watercolor washes. Hand-crafted, warm feel.

COLORS: Warm palette with subtle orange and sky blue accents.

COMPOSITION: Centered focal point, generous negative space, square format.

TEXTURE: Visible brushstrokes, paper texture, analog warmth.

AVOID: Text, photorealism, generic educational imagery (no lightbulbs, no happy children raising hands), cluttered composition.

FORMAT: Square (1:1)
```

### Output Location

`/curriculove/public/images/curricula/[slug].png`

### Integration

Update `curricula-convex.json` to reference generated images:
```json
{
  "slug": "beast-academy",
  "imageUrl": "/images/curricula/beast-academy.png",
  ...
}
```

---

## Workstream 2: UI Polish

### OpenEd Partner Badge

**Priority feature:** Create SVG icon badge for "FREE through OpenEd" indicator.

**Source:** OpenEd logo brackets icon (PNG imported - needs conversion to SVG)

**Placement:** On curriculum cards for `isOpenEdVendor: true` entries (49 curricula)

**Action item:** Convert the imported OpenEd icon PNG to clean SVG, integrate into card component.

### Color Direction

Light touch on branding. Let curriculum images be the star.

Options to test:
- Minimal/neutral UI (grays, whites, subtle accents)
- Warm but unbranded (cream, sage, muted tones)
- Keep current green, just polish edges

**OpenEd badge exception:** The partner badge should stand out visually (use brand orange or distinct treatment) since it's the funnel moment.

### Typography

Keep Inter throughout for app-native feel. Don't introduce Playfair serif.

### Placeholder Image Update

Current: Dark green gradient with curriculum initial
Target: Replace with AI-generated images

Fallback for any remaining missing images: Keep gradient placeholder or use philosophy-archetype fallback.

---

## Immediate Next Steps

1. **Generate 5 test images** (Saxon, 1000 Hours Outside, Abeka, Khan Academy, Beast Academy)
2. **Review and refine** style/prompt template
3. **Convert OpenEd icon** PNG → SVG for badge
4. **Integrate badge** into card components
5. **Scale image generation** once style is validated

---

*Spec created: 2026-01-26*
