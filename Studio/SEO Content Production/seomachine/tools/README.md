# seomachine tools

## Content Brief Generator

`content_brief_generator.py` generates a competitor-informed SEO content brief for a seed topic/keyword using the existing `DataForSEO` module.

### What it produces

A markdown brief including:
- Primary keyword + metrics (search volume, CPC, competition)
- Secondary keyword cluster (top 15–20)
- Top SERP URLs (top 10)
- Common competitor H2/H3 headings (best-effort scraping)
- Suggested H2 structure
- FAQ questions to answer
- Target word count (based on competitor pages)
- Differentiation opportunities (gap ideas)

### Prerequisites

1. DataForSEO credentials configured in:
   - `data_sources/config/.env`

   Required vars:
   - `DATAFORSEO_LOGIN`
   - `DATAFORSEO_PASSWORD`
   - (optional) `DATAFORSEO_BASE_URL`

2. Python dependencies (see `data_sources/requirements.txt`):

```bash
pip install -r data_sources/requirements.txt
```

### Usage

From the `seomachine/` directory (recommended):

```bash
python tools/content_brief_generator.py "homeschool curriculum"
```

Or from inside `tools/`:

```bash
python content_brief_generator.py "homeschool curriculum"
```

The script writes a markdown file to the `tools/` directory by default.

### Options

- Change location:

```bash
python tools/content_brief_generator.py "homeschool curriculum" --location-code 2840
```

- Change where the markdown file is written:

```bash
python tools/content_brief_generator.py "homeschool curriculum" --output-dir "./output"
```

- Slow down requests (rate limiting / politeness):

```bash
python tools/content_brief_generator.py "homeschool curriculum" --delay-seconds 2
```

### Notes

- Competitor scraping is best-effort. Some sites may block requests or load headings via JavaScript.
- If scraping fails, the brief still includes DataForSEO keyword + SERP sections.

---

## Competitor Gap Finder

`competitor_gap_finder.py` finds keywords competitors rank for that `opened.co` does not, then prioritizes them into an actionable content roadmap.

### What it produces

A prioritized list (Markdown + CSV) with:
- Keyword
- Search volume
- Competitor ranking position
- Our current position (if any)
- Difficulty estimate
- Suggested content type (guide, comparison, how-to)
- Opportunity score (volume / difficulty)

### Usage

Single competitor:

```bash
python tools/competitor_gap_finder.py --competitor cathyduffy.com --min-volume 200
```

Batch mode (runs the default competitor set and deduplicates):

```bash
python tools/competitor_gap_finder.py --batch --min-volume 100
```

### Options

- Control how many competitor keywords are pulled:

```bash
python tools/competitor_gap_finder.py --competitor hslda.org --max-keywords 500
```

- Slow down requests (rate limiting / budget control):

```bash
python tools/competitor_gap_finder.py --batch --delay-seconds 1.5
```

- Write outputs somewhere else:

```bash
python tools/competitor_gap_finder.py --batch --output-dir "./output"
```

### Notes

- Uses DataForSEO Labs domain analysis to fetch competitors’ ranked keywords.
- Uses live SERP checks to confirm whether `opened.co` ranks for each candidate keyword.
- For large runs, expect API cost; start with `--max-keywords 200` and increase as needed.
