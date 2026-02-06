---
id: opened-20260205-031
title: Switch Curriculove to production Clerk keys
status: todo
project: lead-magnet
assignee: charlie
priority: high
effort: 1
due: 2026-02-10
tags: [curriculove, auth, launch-blocker]
created: 2026-02-05
updated: 2026-02-05
---

## Context
App at curricu.love is using dev Clerk keys. Must switch to production before any external users. Blocks public launch.

## Steps
- [ ] Create production Clerk instance
- [ ] Update env vars in Vercel
- [ ] Delete .next folder and redeploy
- [ ] Verify auth flow works in production

## Spec Reference
Projects/Lead Magnet Project/curriculove/CLAUDE.md
