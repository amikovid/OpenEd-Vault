# Webflow Tools Page Redesign

**Status:** Planning
**Owner:** Charlie (content) + Dev/Design (implementation)
**Created:** 2026-01-21

---

## Problem Statement

The current tools pages on opened.co have a toggle UI element that needs to be removed/redesigned. Fred (SEO consultant) and Melissa have been waiting on updates to:
1. Remove the toggle from tools pages
2. Update the tools page template

This is a Webflow CMS + Designer task that requires understanding the current architecture before making changes.

---

## Current State

### Tools CMS Collection
- **76 tools** currently in Webflow
- URL pattern: `/tools/[slug]`
- Full inventory in: `SEO Content Production/Tools Directory/webflow_tools_inventory.json`

### Sample Tools
```
/tools/khan-academy
/tools/math-u-see
/tools/saxon-math
/tools/ixl
/tools/outschool
/tools/beast-academy-online
/tools/brave-writer
... (76 total)
```

### Unknown (Needs Investigation)
- [ ] What is the toggle element? (accordion? show/hide? tabs?)
- [ ] Is it hardcoded in the Webflow Designer template or driven by CMS fields?
- [ ] What should replace it?

---

## Tasks

### Phase 1: Discovery
- [ ] Screenshot current tools page layout
- [ ] Identify the toggle element in Webflow Designer
- [ ] Document current CMS fields for Tools collection
- [ ] Understand what content the toggle shows/hides

### Phase 2: Design Decision
- [ ] Determine new layout (remove toggle entirely? replace with sections?)
- [ ] Get Fred's input on SEO implications
- [ ] Mock up new template

### Phase 3: Implementation
- [ ] Update Webflow Designer template
- [ ] Test on staging
- [ ] Bulk update any CMS fields if needed
- [ ] Deploy

---

## Related Projects

This connects to the larger **Tools Directory** SEO initiative:
- `SEO Content Production/Tools Directory/PROJECT.md`
- Goal: Parent-authored reviews with real quotes from Slack
- The template update should accommodate the new review format

### New Review Template Structure
From `TOOL_REVIEW_TEMPLATE.md`:
```
- Hero with tool name + quick verdict
- What parents say (real quotes)
- What we love
- What didn't work
- Who this is for
- How to access through OpenEd
```

---

## Questions for Next Session

1. Can you access Webflow Designer to show me the current template?
2. What exactly is the "toggle" - is it the FAQ accordion? A show/hide section?
3. Is this a bulk operation (all 76 tools) or per-tool customization?

---

## Files & Resources

| Resource | Location |
|----------|----------|
| Tools inventory | `SEO Content Production/Tools Directory/webflow_tools_inventory.json` |
| Review template | `SEO Content Production/Tools Directory/TOOL_REVIEW_TEMPLATE.md` |
| Webflow sync scripts | `agents/webflow_sync_agent.py` |
| Tool database (content) | `Lead Magnet Project/OpenEd_Tool_Database.md` |

---

*Created from SEO meeting follow-up, 2026-01-21*
