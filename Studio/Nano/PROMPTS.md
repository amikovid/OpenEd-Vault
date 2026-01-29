# Nano Banana Style Prompts

Portable prompt templates for high-end AI image generation. Works with Gemini Imagen (Nano Banana Pro) or similar models.

---

## 1. Crumpled Vinyl Sticker

**Use case:** Brand logos, mascots, icons rendered as worn stickers

```
A sharp, top-down macro photograph of a single, heavily crumpled circular vinyl sticker featuring [SUBJECT].

MATERIAL & TEXTURE (VINYL):
The sticker is made of durable, slight-gloss vinyl material, not paper. It is severely crinkled with sharp, defined ridges and deep stress folds across its entire surface. Unlike soft paper creases, these vinyl wrinkles show plastic stress and catch the light with subtle specular highlights on the peaks of the folds. The edges are slightly curled from wear.

COLOR PALETTE:
The background color of the circular sticker is [PRIMARY COLOR]. The subject is printed in [CONTRASTING COLOR].

LIGHTING (STUDIO BRIGHT):
Bright, clean, high-key overhead white studio lighting. This intense lighting creates strong, clean highlights on the vinyl's crumpled ridges and defined, crisp shadows in the valleys, dramatically emphasizing the 3D topography of the damage.

BACKGROUND & COMPOSITION:
The camera is locked in a strict, perfectly parallel top-down flat lay view. The sticker is adhered flat onto a pure white plastic surface which has a subtle, fine granular texture (like bead-blasted plastic) to provide tactile contrast to the smooth vinyl. The entire sticker is in sharp focus.
```

**Tips:**
- Use with `--input` flag to preserve specific artwork/logo
- Works best at 1:1 aspect ratio
- Specify brand colors explicitly

---

## 2. Floating Editorial Apparel

**Use case:** Swag mockups, merch store images, product shots

```
Act as a fashion photographer and creative director shooting a high-end editorial lookbook for [BRAND NAME].

THE SUBJECT & COMPOSITION (FLOATING & ANGLED):
A single, premium [GARMENT TYPE] is floating suspended in mid-air, centered in the frame. There is no hanger visible. Crucial Angle: The garment is NOT presented flatly frontal. It is rotated slightly (approximately 15 degrees angled view) to show depth, form, and a dynamic profile. Despite floating, the fabric must show realistic weight, deep gravity-defying folds, creases, and natural wrinkles. It must feel like a real, heavy garment frozen in time, not a stiff 3D model.

BRANDED DESIGN & AESTHETICS:
[Describe the specific design elements to preserve - logo placement, graphics, text, colors]

MATERIALITY & TEXTURE (CRITICAL):
The focus remains on luxurious, tactile textures. Fabric: [Describe material - e.g., heavyweight tri-blend cotton with visible heathered texture, technical knit with coarse weave structure, etc.]

ENVIRONMENT & BACKGROUND (WHITE STUDIO):
The garment floats within an abstract, infinite white photo studio cyclorama space. The background is completely seamless, pure, clean white, and minimalist, with absolutely zero distractions, placing total focus on the suspended garment.

LIGHTING & PHOTOGRAPHY STYLE:
Style: Hyper-realistic editorial fashion photography. Clean, high-key aesthetic. Lighting: Sophisticated studio lighting. Soft, diffused light that sculpts the folds of the fabric and highlights the texture against the pure white background. Subtle soft shadows cast on the garment itself to define its form in the white space.
```

**Tips:**
- Use with `--input` flag to preserve specific designs
- 3:4 or 4:5 aspect ratio works well for vertical garments
- Be explicit about preserving design elements

---

## 3. Luxury Concept Product

**Use case:** "What if [X] was a high-end brand?" conceptual products

```
[BRAND/PHILOSOPHY NAME]:
A high-end, glossy concept art magazine editorial photograph of a unique, unexpected functional object conceptualized and designed by the brand.

**1. The Concept & Object (AI Invention):**
Based on the design philosophy, heritage, and material vocabulary of [BRAND/PHILOSOPHY], the AI must invent a novel utility product (NOT standard clothing, shoes, or bags). [Describe the invented object and its function]. The object should feel sculptural yet functional.

**2. Materials & Details (Hyper-Premium):**
[Describe materials characteristic of the brand - e.g., patinated exotic leathers, brushed aerospace-grade titanium, sculpted matte ceramics, molded carbon fiber, reclaimed barn wood, hand-forged brass, etc.]. Every detail is hyper-realistic: visible stitching, microscopic material grain, precision engravings, and complex texture contrasts.

**3. Photography & Lighting (Cinematic Studio):**
Shot on a medium format Phase One camera with a 100mm macro lens. Extremely shallow depth of field, with sharp focus on the hero details of the object and a creamy, smooth bokeh background. The lighting is sophisticated studio softbox lighting: gentle, enveloping fill light with precise rim lighting to accentuate contours and material textures.

**4. Environment:**
A seamless, impeccably clean studio cyclorama background in [PASTEL TONE - e.g., desaturated mint, pale blush, warm cream, sage green], free of shadows.

**5. Layout & UI Elements (Strict Placement):**
- Bottom Right Corner: A small, understated, monochrome gray logo/wordmark of the brand.
- Bottom Left Corner: Small, minimalist monochrome gray text: "CONCEPT STUDY: [PRODUCT NAME]. MATERIAL: [MAIN MATERIALS]. SS25."
```

**Example brand interpretations:**

| Brand/Philosophy | Material Vocabulary | Potential Object |
|------------------|---------------------|------------------|
| Montessori | Beechwood, brass, geometric precision | Tactile learning instruments |
| Classical Education | Dark walnut, aged leather, parchment | Scholar's reading lectern |
| Unschooling | Reclaimed wood, raw brass, blown glass | Curiosity specimen cabinet |
| Nature School | Waxed canvas, forged brass, bridle leather | Field observation kit |
| Public School | High-gloss ABS, chrome steel, laminate | Modular assessment station |
| Homeschool | White oak, slate, linen | Convertible learning table |

---

## 4. Isometric Schematic Diagram

**Use case:** Conceptual infographics, system maps, comparison diagrams

```
Create a hand-drawn isometric schematic diagram of [SUBJECT].

STYLE: Hand-drawn technical illustration with precise linework, visible pencil texture, and architectural drafting aesthetic. Think patent drawings meets urban planning diagrams. Black ink on cream paper with subtle blue annotation marks.

CONCEPT: [Describe the isometric scene - e.g., a district, a system, a process flow represented as physical space]

ELEMENTS (positioned in isometric space):
[List each element with brief description of its visual representation]
1. [ELEMENT] - [Description of building/object/space]
2. [ELEMENT] - [Description]
3. [ELEMENT] - [Description]
...

ANNOTATIONS: Small hand-lettered labels for each element. Dotted lines showing connections and relationships. Small icons indicating key features.

COMPOSITION: [Aspect ratio guidance]. Isometric 30-degree angle. Generous white space. Clean, readable labels.

AVOID: Color fills (or specify muted palette), digital rendering, photorealism. Keep it looking hand-drafted.
```

**Tips:**
- 16:9 works well for wide diagrams
- Can add subtle color washes while keeping hand-drawn feel
- Good for showing relationships between concepts

---

## Generation Notes

**Gemini Nano Banana Pro settings:**
- `--model pro` for quality and aspect ratio control
- `--aspect` options: 1:1, 4:3, 3:4, 16:9, 9:16
- `--input [image]` for rework/reference mode
- `--variations N` for multiple outputs

**General tips:**
- Natural language beats tag soup
- Be explicit about what to preserve vs. what to generate
- Describe materials by feel, not just name
- Include the "why" for better AI inference
