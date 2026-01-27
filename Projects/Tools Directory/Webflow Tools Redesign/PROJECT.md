# Webflow Tools Page Redesign

**Status:** Spec Complete - Awaiting Demand Flow Team
**Owner:** Charlie (content) + Demand Flow (design)
**Updated:** 2026-01-26

---

## Current State

- ✅ 4 reviews drafted (Math-U-See, Saxon, Beast Academy, Teaching Textbooks)
- ✅ Template spec finalized based on Fred's feedback
- ✅ Spec page created in Notion for Ella
- ✅ Permission requests sent to teachers via Slack (2026-01-26)
- ⏳ Awaiting teacher approvals (Rachael Davie, Danielle Randall, Chelsea Forsythe)
- ⏳ Awaiting Demand Flow team's template changes
- ⏳ Then batch-update 76 tools via API

---

## Next Steps (In Order)

### 1. Demand Flow: Template Changes
**Notion spec:** [Tools Page Redesign Spec](https://www.notion.so/Tools-Page-Redesign-Spec-For-Ella-2f4afe52ef5981f39a83d530da2f72b7)

| Task | Details |
|------|---------|
| Add Quick Verdict section | One paragraph above main content, below hero |
| Add author photo | Small headshot next to byline |
| Remove accordion/tab UI | Show all content in one scrollable block |
| Single rich text body | All sections with H2 headers in one field |

**Section order:** Quick Verdict → Teacher's Take → Best For / May Not Fit → What Parents Say → How It Works → Pricing → FAQs → Alternatives

**Note:** Can take down non-live pages if that simplifies the migration.

### 2. Charlie: Content Migration (After Ella)
Once template is updated:
- [ ] Write Quick Verdict intros for all 76 tools
- [ ] Link author references to Authors collection
- [ ] Batch push updates via Webflow API
- [ ] Verify published pages

### 3. Content Backlog (Ongoing)
Priority tools to draft (have podcast/Slack content):
1. Teaching Textbooks (draft ready, awaiting Chelsea approval)
2. Life of Fred
3. All About Reading
4. Singapore Math
5. Khan Academy (3 podcast episodes)
6. Reading Eggs (3 podcast episodes)

---

## Architecture

### CMS Approach (Simplified)

Single rich text body field with H2 headers for each section. No separate CMS fields needed.

**Section order in body:**
1. Quick Verdict (H2)
2. Teacher's Take (H2)
3. Who [Tool] Is Best For (H2)
4. Who [Tool] May Not Fit (H2)
5. What Parents Say (H2)
6. How It Works (H2)
7. Pricing (H2)
8. FAQs (H2)
9. Alternatives (H2)

### Webflow IDs

| Collection | ID |
|------------|-----|
| Tools | `6811bc7ab1372f43ab83dec6` |
| Authors | `68089af9024139c740e4b922` |

---

## Files

| Resource | Location |
|----------|----------|
| Spec (Notion) | [Tools Page Redesign Spec](https://www.notion.so/Tools-Page-Redesign-Spec-For-Ella-2f4afe52ef5981f39a83d530da2f72b7) |
| Spec (local backup) | `TOOLS_PAGE_SPEC.md` |
| Permission requests (Google Doc) | [Teacher Permission Requests](https://docs.google.com/document/d/1omaj39CTcQzP4m1wnVqdsvfC93A3ou4rIu72Y0uUShE/edit) |
| Permission requests (Notion) | [Teacher Permission Requests](https://www.notion.so/Teacher-Permission-Requests-Tool-Reviews-2f4afe52ef5981d29605cca283d92b68) |
| Permission requests (local) | `../permission-requests/` |
| Review template | `../TOOL_REVIEW_TEMPLATE.md` |
| Drafts | `../drafts/` |
| Slack mining report | `../slack-reports/tool-mentions-2026-01-21.md` |

---

## Communication Log

**2026-01-22:** Charlie sent 3 example reviews to Fred
**2026-01-23:** Fred replied with feedback (Quick Verdict above fold, author photos, open accordions, move FAQs)
**2026-01-26:** Spec created and sent to Ella via Notion
**2026-01-26:** Permission requests sent to teachers via Slack (Rachael, Danielle, Chelsea) with Google Doc link
**2026-01-26:** Template change request sent to Demand Flow team (simplified to single rich text body)

---

*Parent project: `../PROJECT.md` (Tools Directory)*
