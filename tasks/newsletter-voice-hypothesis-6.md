---
id: opened-20260205-006
title: Test newsletter voice hypothesis 6 - TTT format
status: todo
project: newsletter
assignee: claude
priority: medium
effort: 3
due: 2026-02-12
tags: [voice, newsletter, testing]
created: 2026-02-05
updated: 2026-02-05
---

## Context
Hypothesis 5 replaced Pirate Wires examples with Charlie's actual published newsletters in the daily newsletter writer skill. Now we're shifting to a **3 Quick Takes (Thought/Tool/Trend)** daily format.

**New daily format (TTT):**
- **Thought:** Opinion/insight on education topic
- **Tool:** Curriculum or resource recommendation
- **Trend:** Industry data point or news item

This format mirrors Pirate Wires' approach (3 quick takes) and satisfies CEO's desire for daily cadence while being lightweight enough for Claude to draft autonomously from the RSS curation pipeline.

Target voice: "Homeschool Data Gap" edition - real rhythm, asides that interrupt thought, "I just noticed this" energy. NOT punchy/staccato - conversational and unhurried.

**RSS pipeline integration:** Articles starred in the RSS curation dashboard become source material for TTT takes. This means Claude can draft each morning's newsletter from the previous day's curated articles.

## Steps
- [ ] Update opened-daily-newsletter-writer skill with TTT structure
- [ ] Generate TTT newsletter draft using RSS pipeline articles as source
- [ ] Compare against Design Over Delivery v1-v5
- [ ] Score against Homeschool Data Gap voice target
- [ ] Document findings and iterate if needed
- [ ] If TTT format works, update CLAUDE.md with new cadence
