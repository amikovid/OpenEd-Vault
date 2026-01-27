# Nearbound Extraction Queries

Queries to find people mentioned in OpenEd content for the quick index.

## Source 1: Podcast Episodes

**Location:** `Studio/Open Ed Podcasts/*/`

**Query pattern:**
```
grep -r "guest" Studio/Open\ Ed\ Podcasts/
```

**Expected format in podcast folders:**
- Guest name in folder name
- Guest bio in PROJECT.md or transcript

**Priority:** Podcast guests are highest-warmth contacts.

## Source 2: Blog Posts

**Location:** `Content/Master Content Database/Blog/`

**Query patterns:**
- Look for bylines
- Look for quotes with attribution
- Look for "according to [Name]" patterns

**Grep examples:**
```
grep -r "according to" Content/
grep -r "says [A-Z]" Content/
grep -r "told OpenEd" Content/
```

## Source 3: Newsletter Mentions

**Location:** `Content/Master Content Database/Daily/`

**Query patterns:**
- Names in TOOL segment recommendations
- Expert quotes
- Referenced researchers

## Source 4: Master Content Index

**Location:** `.claude/references/Master_Content_Index.md`

Review podcast section - all 66 episodes have guest names.

---

## Extraction Process

### Phase 1: Podcast Guest List

1. List all podcast folders
2. Extract guest names
3. Create profile for each

**Estimated:** 40-50 unique guests

### Phase 2: Blog Featured People

1. Search for quotes and attributions
2. Extract names
3. Cross-reference with podcast list
4. Create profiles for new people

**Estimated:** 20-30 additional people

### Phase 3: Newsletter Mentions

1. Search daily newsletters for names
2. Focus on TREND and TOOL segments
3. Add to existing profiles or create new

**Estimated:** 10-20 additional people

---

## Profile Priority

| Priority | Criteria | Action |
|----------|----------|--------|
| **1 - High** | Podcast guest | Full profile |
| **2 - Medium** | Featured in blog | Full profile |
| **3 - Low** | Newsletter mention only | Basic profile |

---

## Top 50 Target List

Build profiles for these categories first:

1. **All podcast guests** (40-50)
2. **Education thought leaders** (quoted repeatedly)
3. **Tool/curriculum founders** (product mentions)
4. **Partner organizations** (state orgs, co-ops)

---

## Social Handle Research

For each person, research handles:

1. **Web search:** "[Name] Twitter" / "[Name] LinkedIn"
2. **Podcast show notes:** Often include links
3. **Company about pages:** Team bios with social links

**Note handles found in profile.**
