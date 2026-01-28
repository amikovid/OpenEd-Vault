---
name: nano-banana-image-generator
description: Generate AI images using Nano Banana Pro (Gemini). Use this skill when the user needs images - thumbnails, social posts, blog headers, or creative visuals. Follows an iterative workflow - brainstorm concepts, select direction, generate in multiple styles, then produce via API.
---

# Nano Banana Image Generator

Generate professional, non-generic images using Nano Banana Pro (Gemini API).

## Workflow Overview

1. **Brainstorm Concepts** - Generate 4-6 high-level visual ideas
2. **Select Direction** - User picks the concept they like
3. **Optimize Prompt** - Refine into a strong, detailed prompt
4. **Style Variations** - Adapt to 2-3 different visual styles
5. **Generate Images** - Run via Gemini API

## Step 1: Brainstorm Concepts

### When to Ask Clarifying Questions

Before brainstorming, assess if you have enough information. Ask 2-4 focused questions if:
- **Subject** is unclear or too generic
- **Purpose/Context** is missing (what's this for?)
- **Style** preferences are unspecified
- **Text requirements** are ambiguous

**Skip questions if:** The user provides a detailed brief or says "just generate it." Don't create friction when the request is already clear.

**Example:**
> User: "Can you write me a prompt for a hero image for my landing page?"
>
> You: "A few quick questions:
> 1. What's the product/service?
> 2. Any specific mood - modern/minimal, bold/energetic, warm/approachable?
> 3. Should there be text in the image itself?"

### Generating Concepts

When the user provides a topic or use case, generate 4-6 high-level visual concepts. Each concept should be:

- **One sentence** describing the visual idea
- **Concrete and immediate** - you can picture it instantly
- **Conceptual but not abstract** - a clear object/scene with meaning
- **Non-generic** - avoid cliches (no lightbulbs for ideas, no books for education)

**Format:**

```
1. **[Short label]** - One sentence description of the visual concept and why it works.

2. **[Short label]** - One sentence description...
```

**Example for "newsletter about self-directed learning":**

```
1. **Compass with crayon needle** - A compass where the needle is a crayon, suggesting direction comes from the learner's own hand.

2. **Path that branches into many paths** - A single dirt path splitting into dozens of colorful trails, each heading somewhere different.

3. **Empty frame on an easel** - A blank canvas on an easel in a field, suggesting the learner creates their own picture.

4. **Backpack with roots** - A school backpack sitting on grass, but roots are growing out the bottom into the soil - learning that plants itself.
```

Wait for user to select before proceeding.

## Step 2: Optimize the Prompt

Once the user selects a concept, develop it into a full prompt. Structure:

```
Create a [style type] illustration of [subject].

CONCEPT: [Expand the one-sentence idea into a clear visual description]

STYLE: [Artistic approach - load from references/styles/ if brand-specific]

COMPOSITION: [Framing, focal point, negative space, balance]

COLORS: [Palette - describe by name, not hex codes which may render as text]

TEXTURE: [Surface qualities, analog/digital feel]

AVOID: [What should NOT appear - be specific]

FORMAT: [Aspect ratio]
```

**Key principles:**
- Natural language, full sentences - no tag soup
- Describe colors by name (burnt orange, sky blue, near-black) not hex codes
- Maximum 2-3 elements - if it feels busy, remove something
- Favor metaphor over literal depiction

## Step 3: Style Variations

Adapt the optimized prompt to 2-3 different styles from `references/styles/`:

- **watercolor-line.md** - Ink linework with watercolor washes, warm **(DEFAULT for thumbnails)**
- **opened-editorial.md** - Conceptual, brand colors, editorial wit
- **minimalist-ink.md** - High-contrast black and white, crosshatching
- **newyorker-cartoon.md** - Single-panel observational humor, crosshatching, italic serif caption **(for editorial commentary)**

**Default behavior:** For blog thumbnails and article headers, use watercolor-line style unless otherwise specified. This style provides warmth and approachability while maintaining editorial quality.

**New Yorker style:** When user asks for "New Yorker cartoon," "editorial cartoon," or observational humor illustrations, load `references/newyorker-cartoon.md` for the full style guide including caption formulas, humor principles, and prompt template.

Present all variations to user so they can choose which to generate, or generate all.

## Step 4: Generate via API

### Setup

The Gemini API key is stored in the vault root `.env` file. The script looks for `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

**Requirements:** `pip install google-genai pillow`

### Running the Script

The script lives at `.claude/skills/nano-banana-image-generator/scripts/generate_image.py`.

```bash
# From the OpenEd Vault root directory:
cd "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault"

# Set the API key and run
export GEMINI_API_KEY=$(grep GEMINI_API_KEY .env | cut -d'=' -f2) && \
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "Your prompt here" \
  --model pro \
  --aspect 16:9 \
  --output "Studio/Content Engine Deck" \
  --name "my-image"
```

**Options:**
- `--model pro` (higher quality, supports aspect ratio) or `--model flash` (faster, cheaper)
- `--aspect 16:9`, `1:1`, `9:16`, `3:4`, `4:3` (only works with pro model)
- `--variations N` - generate N versions
- `--output ./path` - save location (default: current directory)
- `--name prefix` - filename prefix (output: `{prefix}_{timestamp}_{model}.png`)

**Note:** For flash model, aspect ratio config is ignored - include the ratio in your prompt text instead.

**Output location:** ALWAYS save images in the same folder as the content they belong to - not a generic images dump. This is critical for organization.

**Routing by content type:**

| Content Type | Output Location |
|--------------|-----------------|
| Newsletter | `Studio/OpenEd Daily/[date-folder]/` |
| Podcast episode | `Studio/Open Ed Podcasts/[episode-folder]/` |
| Blog article | `Studio/SEO Content Production/[article-folder]/` |
| Guest contributor | `Studio/SEO Content Production/Guest Contributors/[name]/` |
| Social media | `Studio/Social Media Transformation/[campaign]/` |
| Hub page | `Content/Open Education Hub/[topic]/` |

**Before generating:** Identify the content context and determine the correct output path. If a project folder exists, route there. If not, create the folder first.

**Naming convention:** Use descriptive prefixes that indicate purpose:
- `thumbnail-draft.png` - Working thumbnail
- `thumbnail-final.png` - Approved thumbnail  
- `header-[concept].png` - Article header
- `social-[platform].png` - Platform-specific social image

## Step 5: Iterate

After user reviews generated images:
- **80% good?** Request specific edits conversationally rather than regenerating
- **Composition off?** Adjust framing or element placement in prompt
- **Wrong style?** Try a different style reference
- **Too busy?** Simplify to fewer elements
- **Colors wrong?** Be more explicit about palette

## Prompting Principles

### Write Like a Creative Director

Brief the model like a human artist. Use proper grammar, full sentences, and descriptive adjectives.

| Don't | Do |
|-------|-----|
| "Cool car, neon, city, night, 8k" | "A cinematic wide shot of a futuristic sports car speeding through a rainy Tokyo street at night. The neon signs reflect off the wet pavement and the car's metallic chassis." |

**Be specific about:**
- **Subject:** Instead of "a woman," say "a sophisticated elderly woman wearing a vintage chanel-style suit"
- **Materiality:** Describe textures - "matte finish," "brushed steel," "soft velvet," "crumpled paper"
- **Setting:** Define location, time of day, weather
- **Lighting:** Specify mood and light source
- **Mood:** Emotional tone of the image

### Provide Context

Context helps the model make logical artistic decisions. Include the "why" or "for whom."

**Example:** "Create an image of a sandwich for a Brazilian high-end gourmet cookbook."
*(Model infers: professional plating, shallow depth of field, perfect lighting)*

### Keep It Simple

- One clear focal point
- Maximum 2-3 elements total
- Generous negative space
- If it feels busy, remove something

### Avoid the Generic

- No lightbulbs for "ideas"
- No stacks of books for "education"
- No happy children raising hands
- No glossy AI aesthetic

## Resources

### references/styles/
Brand and aesthetic style definitions:
- `opened-editorial.md` - OpenEd brand style
- `minimalist-ink.md` - Black and white ink illustration
- `watercolor-line.md` - Ink with watercolor washes
- `newyorker-cartoon.md` - New Yorker single-panel cartoon (crosshatching, understated humor, italic serif caption)

### references/concepts/
Saved prompts for reusable images:
- `paper-airplane-newsletter.md` - Newsletter header variations
- `ed-horse-error.md` - Ed mascot for error states

### scripts/ (in this skill folder)
- `generate_image.py` - Gemini API image generation (Nano Banana / Nano Banana Pro)

## Prompt Modifiers Reference

| Category | Examples |
|----------|----------|
| **Lighting** | golden hour, dramatic shadows, soft diffused light, neon glow, overcast |
| **Style** | cinematic, editorial, technical diagram, hand-drawn, photorealistic |
| **Texture** | matte finish, brushed steel, soft velvet, crumpled paper, weathered wood |
| **Composition** | wide shot, close-up, bird's eye view, dutch angle, symmetrical |
| **Mood** | energetic, serene, dramatic, playful, sophisticated |
| **Quality** | 4K, high-fidelity, pixel-perfect, professional grade |

## Advanced Capabilities

### Text Rendering & Infographics

Put exact text in quotes. Specify style: "polished editorial," "technical diagram," or "hand-drawn whiteboard."

**Example prompts:**

```
Earnings Report Infographic:
"Generate a clean, modern infographic summarizing the key financial highlights from this earnings report. Include charts for 'Revenue Growth' and 'Net Income', and highlight the CEO's key quote in a stylized pull-quote box."
```

```
Whiteboard Summary:
"Summarize the concept of 'Transformer Neural Network Architecture' as a hand-drawn whiteboard diagram suitable for a university lecture. Use different colored markers for the Encoder and Decoder blocks, and include legible labels for 'Self-Attention' and 'Feed Forward'."
```

### Character Consistency & Thumbnails

Use reference images and state "Keep the person's facial features exactly the same as Image 1." Describe expression/action changes while maintaining identity.

**Example prompt:**

```
Viral Thumbnail:
"Design a viral video thumbnail using the person from Image 1.
Face Consistency: Keep the person's facial features exactly the same as Image 1, but change their expression to look excited and surprised.
Action: Pose the person on the left side, pointing their finger towards the right side of the frame.
Subject: On the right side, place a high-quality image of a delicious avocado toast.
Graphics: Add a bold yellow arrow connecting the person's finger to the toast.
Text: Overlay massive, pop-style text in the middle: 'Done in 3 mins!'. Use a thick white outline and drop shadow.
Background: A blurred, bright kitchen background. High saturation and contrast."
```

### Image Reworking (Edit Existing Images)

The `--input` flag enables "rework mode" - pass an existing image to Gemini and describe the changes you want.

**Key use cases:**
- **Small tweaks** - Adjust colors, add/remove elements, change lighting
- **Style transfer** - Keep composition but change artistic style
- **Object manipulation** - Remove, add, or modify specific objects
- **Seasonal/temporal changes** - Same scene, different time/season

**Running in rework mode:**

```bash
cd "/Users/charliedeist/Library/Mobile Documents/com~apple~CloudDocs/Root Docs/OpenEd Vault"

# Basic edit - add something
export GEMINI_API_KEY=$(grep GEMINI_API_KEY .env | cut -d'=' -f2) && \
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "Add snow to the roof and yard" \
  --input ./path/to/house.png \
  --model pro

# Color adjustment
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "Change the accent color from red to teal, keep everything else identical" \
  --input ./path/to/thumbnail.png \
  --model pro

# Style transfer - keep composition, change aesthetic
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "Convert this to watercolor style with soft washes and visible brushstrokes" \
  --input ./path/to/photo.png \
  --model pro

# Generate variations of an edit
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "Make the lighting warmer, like golden hour" \
  --input ./path/to/portrait.png \
  --variations 3 \
  --model pro
```

**Prompting tips for rework mode:**

1. **Be specific about what to preserve:**
   - "Keep the person's facial features exactly the same"
   - "Maintain the composition and framing"
   - "Don't change the background"

2. **Be explicit about what to change:**
   - "Change ONLY the color of the shirt from blue to red"
   - "Add snow to the roof and nothing else"
   - "Remove the text overlay"

3. **Use comparative language:**
   - "Make the colors more vibrant"
   - "Increase the contrast slightly"
   - "Make the lighting softer and more diffused"

**Output naming:** Files from rework mode are named `{prefix}_{timestamp}_edit_{model}.png` to distinguish from generated images (`_gen_`).

### Advanced Editing Examples

**Object Removal:**
```bash
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "Remove the tourists from the background and fill with matching cobblestones and storefronts" \
  --input ./street-photo.png \
  --model pro
```

**Seasonal Control:**
```bash
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "Turn this into winter. Add snow to the roof and yard. Change lighting to cold, overcast afternoon. Keep architecture identical." \
  --input ./house-summer.png \
  --model pro
```

**Character Consistency (thumbnail series):**
```bash
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "Keep the person's face exactly the same. Change expression to surprised. Add a pointing gesture toward the right side of the frame." \
  --input ./person-reference.png \
  --model pro
```

### Dimensional Translation (2D to 3D)

```
Floor Plan to Interior Design:
"Based on the uploaded 2D floor plan, generate a professional interior design presentation board in a single image.
Layout: A collage with one large main image at the top (wide-angle perspective of the living area), and three smaller images below (Master Bedroom, Home Office, and a 3D top-down floor plan).
Style: Apply a Modern Minimalist style with warm oak wood flooring and off-white walls across ALL images.
Quality: Photorealistic rendering, soft natural lighting."
```

### Storyboarding & Sequential Art

```
Commercial Storyboard:
"Create an addictively intriguing 9-part story with 9 images featuring a woman and man in an award-winning luxury luggage commercial. The story should have emotional highs and lows, ending on an elegant shot of the woman with the logo. The identity of the woman and man and their attire must stay consistent throughout but they can and should be seen from different angles and distances. Please generate images one at a time. Make sure every image is in a 16:9 landscape format."
```

### Structural Control & Layout

Upload sketches to define text/object placement. Use wireframes for UI mockups.

```
Sketch to Ad:
"Create an ad for a [product] following this sketch."
```

```
Sprite Sheet:
"Sprite sheet of a woman doing a backflip on a drone, 3x3 grid, sequence, frame by frame animation, square aspect ratio. Follow the structure of the attached reference image exactly."
```

---

## OpenEd Content Playbooks

### Instagram Carousel Playbook

For OpenEd deep dives, blog posts, and educational content - use this workflow to create consistent, branded carousels.

**Specs:**
- **Dimensions:** 1080x1350 (4:5 portrait) - use `--aspect 3:4`
- **Style:** Watercolor-line (default for OpenEd)
- **Typical structure:** Intro → Numbered steps → CTA

**Workflow:**

1. **Generate Slide 1 first** - This establishes the visual style
   - Include step number, title, visual concept
   - Use watercolor-line style from `references/styles/watercolor-line.md`

2. **Use Slide 1 as reference for all subsequent slides**
   ```bash
   python3 generate_image.py "prompt" \
     --input path/to/slide1.png \
     --model pro --aspect 3:4
   ```
   - This ensures consistent style, colors, positioning across all slides

3. **Slide structure:**
   - **Intro slide:** Title + subtitle + OpenEd logo (see logo reference below)
   - **Step slides:** Large number (upper left), step title, visual that represents the concept
   - **CTA slide:** Can reuse/edit the intro or create distinct CTA

4. **Adding the OpenEd logo:**
   - Logo file: `references/assets/opened-logo.png`
   - Use rework mode to add logo to existing slide:
   ```bash
   python3 generate_image.py \
     "Replace the 'O' in 'OpenEd' with the OpenEd logo - two curved parentheses forming an O, left half burnt orange, right half sky blue. Keep watercolor style." \
     --input path/to/intro-slide.png \
     --model pro
   ```

5. **Common edits:**
   - Character appearance (race, age, etc.): Regenerate with explicit description
   - Adding CTA text: Use rework mode
   - Style consistency fixes: Reference slide 1 in prompt

**Example carousel structure (7-step method):**

| Slide | Type | Content |
|-------|------|---------|
| 0 | Intro | Title + "in 7 Steps" + logo |
| 1-7 | Steps | Number + title + visual |
| 8 | CTA | "Subscribe to OpenEd Daily" or similar |

**Naming convention:**
- `carousel-intro.png`
- `carousel-step1.png` through `carousel-step7.png`
- `carousel-cta.png`

### Infographic Playbook

For wide-format infographics (spectrum diagrams, comparisons, timelines):

**Specs:**
- **Dimensions:** 21:9 ultra-wide or 16:9 - use `--aspect 16:9` (closest supported)
- **Style:** Watercolor-line with Vox-style information hierarchy
- **Text:** Minimal - labels only, no explanatory paragraphs

**Key principles:**
- Visual hierarchy does the work, not text
- Icons should be hand-drawn style (not emoji)
- Generous white space
- Clear left-to-right or top-to-bottom flow

### Thumbnail Playbook

For blog posts and deep dives:

**Specs:**
- **Dimensions:** 16:9 - use `--aspect 16:9`
- **Style:** Watercolor-line (default)

**Concepts that work for education content:**
- Child engaged in hands-on activity
- The "before/after" or "wrong way/right way" tension
- Metaphorical objects (treehouse = building your own path)
- Avoid: Clipart children, raised hands, classroom settings

### New Yorker Cartoon Playbook

For editorial commentary, LinkedIn posts, newsletter illustrations:

**Specs:**
- **Dimensions:** 1:1 square - use `--aspect 1:1`
- **Style:** See `references/styles/newyorker-cartoon.md`

**Key principles:**
- Simple pen-and-ink, NOT heavily crosshatched
- Plain white background, NO texture
- Caption in italic serif below
- The humor is understated, observational
- 80% white space - restraint is everything

---

## References

### references/assets/
Brand assets for OpenEd content:
- `opened-logo.png` - OpenEd logo mark (orange/blue parentheses)

### references/styles/
(as listed above)
