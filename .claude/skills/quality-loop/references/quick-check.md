# Quality Loop Quick Check

Automated patterns for faster quality control. Use these grep patterns to quickly identify issues.

---

## Human Detector - Grep Patterns

### Forbidden Words (Auto-Fail)
```bash
# Run from article directory
grep -inE "delve|comprehensive|crucial|vital|leverage|landscape|navigate|foster|facilitate|realm|paradigm|embark|journey|tapestry|myriad|multifaceted|seamless|cutting-edge" DRAFT*.md
```

### Correlative Constructions (Auto-Fail)
```bash
# "X isn't just Y - it's Z" pattern
grep -inE "isn't just|isn't merely|not just .* - it's|not just .* it's|didn't .* It |doesn't .* It " DRAFT*.md

# "It's not about X, it's about Y" pattern
grep -inE "not about .*, it's about|not about .* it's about" DRAFT*.md
```

### Dramatic Contrast Reveals (Auto-Fail)
```bash
# "Not X. Y." fragment pattern
grep -inE "Not [A-Za-z]+\. [A-Z]" DRAFT*.md
```

### Em Dashes (Should be hyphens with spaces)
```bash
grep -n "—" DRAFT*.md
```

### Staccato Patterns
```bash
grep -inE "No [a-z]+\. No [a-z]+\.|Just [a-z]+\.$" DRAFT*.md
```

---

## OpenEd Voice - Link Count

### Count Internal Links
```bash
# Count links to opened.co
grep -oE '\[.*?\]\(https://opened\.co[^)]*\)' DRAFT*.md | wc -l

# Count relative internal links
grep -oE '\[.*?\]\(/[^)]*\)' DRAFT*.md | wc -l
```

**Minimum required:** 3 internal links for articles

### List All Links
```bash
grep -oE '\[.*?\]\([^)]+\)' DRAFT*.md
```

---

## SEO Advisor - Keyword Check

### Check Keyword in Key Locations
```bash
# Replace KEYWORD with your primary keyword
KEYWORD="montessori vs reggio"

# In title (H1)
head -5 DRAFT*.md | grep -i "$KEYWORD"

# In first 100 words
head -20 DRAFT*.md | grep -i "$KEYWORD"

# In H2 headers
grep -E "^## " DRAFT*.md | grep -i "$KEYWORD"
```

---

## Quick Checklist

Copy this to the top of draft files for tracking:

```markdown
## Quality Check Status

### Human Detector
- [ ] No forbidden words (grep check)
- [ ] No correlative constructions
- [ ] No dramatic contrast reveals
- [ ] Hyphens with spaces, not em dashes
- [ ] No staccato patterns

### Accuracy
- [ ] Dates verified
- [ ] Names spelled correctly
- [ ] Quotes attributed to real sources
- [ ] No unverifiable claims

### OpenEd Voice
- [ ] Pro-child framing (not anti-school)
- [ ] Descriptive tone (not prescriptive)
- [ ] Practical takeaways present
- [ ] 3+ internal links
- [ ] Proprietary content included

### Reader Advocate
- [ ] Hook creates curiosity
- [ ] Logical section flow
- [ ] Scannable (headers, bullets, tables)
- [ ] Strong ending

### SEO (Advisory)
- [ ] Primary keyword in title
- [ ] Keyword in first 100 words
- [ ] Keyword in 2+ H2s
- [ ] Meta description present
- [ ] FAQ section for featured snippets
```

---

## Verdict Output Format

After running checks, output in this format:

```json
{
  "article": "article-name",
  "date_checked": "2026-01-29",
  "judges": {
    "human_detector": {
      "status": "PASS|FAIL",
      "issues": [
        {"line": 45, "issue": "forbidden word 'comprehensive'", "fix": "change to 'thorough'"}
      ]
    },
    "accuracy": {
      "status": "PASS|FAIL",
      "issues": []
    },
    "opened_voice": {
      "status": "PASS|FAIL",
      "internal_links": 4,
      "issues": []
    },
    "reader_advocate": {
      "status": "PASS|FAIL",
      "issues": []
    },
    "seo_advisor": {
      "status": "PASS",
      "recommendations": []
    }
  },
  "overall": "READY|BLOCKED",
  "blocking_issues": 0
}
```

---

## Batch Check Script

For checking multiple articles:

```bash
#!/bin/bash
# Save as check-articles.sh

for dir in */; do
  if [ -f "${dir}DRAFT"*.md ]; then
    echo "=== Checking: $dir ==="

    # Forbidden words
    echo "Forbidden words:"
    grep -cinE "delve|comprehensive|crucial|vital|leverage|landscape|navigate" "${dir}"DRAFT*.md || echo "  None found ✓"

    # Em dashes
    echo "Em dashes:"
    grep -cn "—" "${dir}"DRAFT*.md || echo "  None found ✓"

    # Internal links
    echo "Internal links:"
    grep -coE '\(https://opened\.co|\(/[^)]+\)' "${dir}"DRAFT*.md

    echo ""
  fi
done
```
