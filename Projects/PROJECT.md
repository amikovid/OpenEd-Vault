# Notion Backlog Pipeline

Two-way sync between programming projects/backlogs and Notion, plus automated content feeds.

## Inspiration

[@geoffreylitt's kanban for Claude agents](https://x.com/geoffreylitt/status/2014454144103539175):
- Monitor progress on all tasks in one view
- See when Claude is blocked, respond in context
- Read Claude's plans with nice formatting (not raw markdown)
- Process voice notes into structured tasks
- Get explanations of code changes

**Key insight:** "Having a stable zoomed-out map of all tasks helps offload cognitive load"

---

## Project Goals

### 1. Notion Database for Projects/Backlogs
- All programming projects live in Notion
- Two-way sync (changes reflect both directions)
- Kanban view for task management
- Voice notes → structured tasks (like Geoffrey's flow)

### 2. Automated Feed Pipeline
**Flow:** Sources → Slack → (optionally) Notion

**Principles:**
- Smooth as butter, no friction
- As complicated as it needs to be (no more)
- Slack as primary triage layer
- Notion as archive/reference

**Sources to gather:**
- [ ] Inventory all newsletters Charlie subscribes to
- [ ] RSS/Atom feeds from key blogs
- [ ] X/Twitter lists or accounts

**Pipeline options:**
- Feedbin/Feedly → Slack via Zapier/n8n
- Clawdbot cron jobs polling feeds → Slack
- Slack bot for triage → approved items to Notion

---

## Implementation Steps

### Phase 1: Inventory
- [ ] List all newsletters (email subscriptions)
- [ ] List key blogs/RSS feeds to follow
- [ ] List X accounts to monitor

### Phase 2: Feed Infrastructure
- [ ] Set up feed aggregator (Feedbin, Feedly, or self-hosted)
- [ ] Configure Slack channel for content staging
- [ ] Build approval workflow (react to approve → Notion)

### Phase 3: Notion Database
- [ ] Design project/backlog schema
- [ ] Set up Notion API integration
- [ ] Build two-way sync mechanism

### Phase 4: Voice Notes Integration
- [ ] Connect Clawdbot voice transcription
- [ ] Auto-route transcribed tasks to Notion backlog

---

## Related Clawdbot Tools

- `notion` skill - Notion API for pages/databases
- Voice transcription (whisper)
- `cron` for scheduled feed checks
- `message` for Slack delivery

---

## Questions to Resolve

1. What's the Notion workspace structure? (New DB or existing?)
2. Which newsletters are highest priority?
3. Slack channel: new or existing?
4. Two-way sync tech: Notion API direct, or middleware like n8n?

---

*Created: 2026-01-23*
*Source: Voice note + Geoffrey Litt tweet*
