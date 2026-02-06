---
id: opened-20260205-007
title: Automate RSS feed fetching with launchd
status: later
project: rss-curation
assignee: charlie
priority: low
effort: 3
due:
tags: [automation, rss]
created: 2026-02-05
updated: 2026-02-05
---

## Context
RSS curation dashboard is working. Currently requires manual `python3 rss_curation.py` runs. Automate with launchd for daily 7am fetches.

## Steps
- [ ] Create launchd plist for daily 7am execution
- [ ] Point to rss_curation.py with correct Python path
- [ ] Test with `launchctl load`
- [ ] Verify tracking.json updates automatically
- [ ] Add error logging
