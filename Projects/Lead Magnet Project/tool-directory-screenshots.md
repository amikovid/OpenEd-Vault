# Tool Directory Screenshots

## Shpigford Skills Library

**Repo:** https://github.com/Shpigford/skills

Agent Skills for AI coding assistants (Claude Code, Cursor, Copilot, etc.)

### Screenshots Skill ⭐

The `screenshots` skill is perfect for capturing curriculum website images for tool reviews.

**Features:**
- Auto-detects routes/features from codebase
- True HiDPI (2x retina) resolution → 2880x1800
- Handles authentication automatically
- Supports dark mode, modals, full-page captures

**Install:**
```bash
npx skills add Shpigford/skills
```

**Usage:**
```
/screenshots http://localhost:3000
# or
Generate screenshots for Product Hunt
```

**Requires:** Playwright (`npm install -D playwright`)

---

## Use Case: Curriculove Tool Reviews

1. Capture homepage screenshots of curriculum providers
2. Use as featured images in tool directory/reviews
3. Consistent quality/sizing across all entries
4. Could batch process the 110+ providers list

### Workflow Idea

```
For each tool in OpenEd_Tool_Database.md:
  → Visit website
  → /screenshots {url}
  → Store in curriculove/public/tools/{slug}/
  → Reference in tool review page
```

---

## Other Useful Skills from this Repo

| Skill | Use for Curriculove |
|-------|---------------------|
| `readme` | Auto-generate docs |
| `favicon` | Generate favicons from logo |
| `build` | Feature development pipeline |

---

*Added: 2026-01-24*
