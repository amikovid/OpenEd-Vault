# Visual Style Guide for Single-Panel Comics

Art direction specifications for generating educational editorial cartoons. These comics should feel like editorial illustrations from The New Yorker, The Far Side, or Bogert Creek - cerebral, understated, timeless.

---

## Primary Style: Editorial Ink Cartoon

### Line Work
- **Fine crosshatching** - Not solid fills, let the lines breathe
- **Soft, organic strokes** - Avoid rigid digital precision
- **Variable line weight** - Thicker for outlines, finer for detail and shading
- **Hand-drawn feeling** - Imperfect but intentional

### Shading
- **Crosshatching only** - No gradients, no smooth fills
- **Strategic shadow** - Just enough to give form, not dramatic lighting
- **White space matters** - Let the paper work

### Format
- **1:1 square** - Optimized for social media (Instagram, LinkedIn, Twitter)
- **Clean margins** - White/cream border around illustration
- **Soft vignette** - Fade at edges, not hard borders

### Color Palette
**Option A: Pure Black & White**
- Black ink on white/cream paper
- No gray tones except from crosshatching
- Maximum contrast, maximum timelessness

**Option B: Limited Sepia/Vintage**
- Black ink with cream/aged paper tone
- Subtle warmth, still essentially monochrome

---

## Caption Typography

### Font Style
- **Italic serif** - Garamond, Times, or similar
- **Centered below illustration** - Not inside the panel
- **Modest size** - The image leads, caption supports

### Caption Rules
- One sentence maximum
- End with period (never exclamation mark)
- Quotation marks around dialogue
- No bold, no caps for emphasis

### Caption Placement
```
┌─────────────────────────┐
│                         │
│     [ILLUSTRATION]      │
│                         │
│                         │
└─────────────────────────┘
   "Caption goes here."
```

---

## Character Design Principles

### Human Characters
- **Simplified features** - Not caricature, not realistic
- **Everyman quality** - Relatable, not specific
- **Posture tells story** - Body language over facial detail
- **Period-neutral clothing** - Avoid dating the cartoon

### Animal Characters
- **Anthropomorphized but not cute** - Animals doing human things seriously
- **Maintain animal proportions** - Not cartoon mascots
- **Deadpan expressions** - The humor is in the situation

### The Bureaucrat (Recurring)
- Suit or official attire
- Clipboard or paperwork
- Glasses optional
- Earnest, helpful expression (not villainous)
- The system personified, not a bad person

### Ed the Horse (Mascot)
- Simple horse form
- Expressive eyes (windows to the soul)
- Often shown in profile
- Ages through different comics (young → old)

---

## Scene Composition

### Single Focal Point
Every comic has ONE clear center of attention:
- The moment of confrontation
- The reveal
- The contrast

### Reading Order
Western left-to-right, top-to-bottom:
1. Eye enters at top-left or center
2. Moves through scene
3. Lands on punchline element
4. Caption delivers final beat

### What to Include
- Only elements necessary for the joke
- Environmental context (minimal)
- The contrast or absurdity (clear)
- The caption (separate)

### What to Exclude
- Background clutter
- Multiple action points
- Text within the illustration (except signs)
- Anything that dilutes the single gag

---

## Prompt Template for Image Generation

Use this structure when handing off to `image-prompt-generator`:

```
A single-panel editorial cartoon in New Yorker style.

SCENE: [One sentence describing the setting and situation]

CHARACTERS: [Who is present, their positions, their expressions/postures]

KEY VISUAL: [The specific element that makes the joke work - the contrast, the sign, the object]

STYLE: Fine crosshatching ink illustration. Soft organic lines, hand-drawn quality. Black ink on white/cream paper. Soft vignette fade at edges, no hard border.

COMPOSITION: [Where the eye should go, what's the focal point]

CAPTION: "[The exact caption text in quotes]" - Italic serif font, centered below illustration.

FORMAT: 1:1 square aspect ratio.

AVOID: Color, digital perfection, cute/cartoony style, busy backgrounds, multiple gags, text within the illustration except for signs/labels integral to the joke.
```

---

## Style Variations

### The Far Side Mode
- Slightly more absurdist
- Animals in very human situations
- More detailed crosshatching
- Wider panels sometimes

### New Yorker Mode
- More understated
- Domestic/office settings
- Minimal crosshatching
- The caption does heavy lifting

### Bogert Creek Mode
- Darker subject matter
- More existential
- Strong crosshatching
- Single figures often

---

## Common Mistakes to Avoid

### Visual
- Too much detail (cluttered)
- Too clean/digital (loses warmth)
- Color (breaks the editorial feel)
- Cute animal characters (undermines seriousness)
- Hard panel borders (feels like comic strip)

### Conceptual
- Multiple jokes in one panel
- Caption explaining what's visible
- Punchline in the image AND caption
- Too much setup, not enough payoff

### Technical
- Wrong aspect ratio (not 1:1)
- Caption inside the illustration
- Sans-serif caption font
- Caption with exclamation marks

---

## Reference Artists

Study these for visual inspiration:

- **Gary Larson (The Far Side)** - Absurdist situations, deadpan execution
- **Derek Evernden (Bogert Creek)** - Dark cerebral humor, crosshatching
- **Roz Chast** - Anxiety, domestic chaos, scribbly energy
- **Edward Steed** - Surreal New Yorker, loose lines
- **Tom Gauld** - Minimal, existential, literary

---

## Quality Checklist for Visuals

Before generating:
- [ ] Is there ONE clear focal point?
- [ ] Can the joke be understood without the caption?
- [ ] Is the style hand-drawn feeling, not digital-clean?
- [ ] Is it black ink on white only?
- [ ] Is the format 1:1 square?
- [ ] Is the caption italic serif, below the image?
- [ ] Does it avoid cuteness in favor of understated?
