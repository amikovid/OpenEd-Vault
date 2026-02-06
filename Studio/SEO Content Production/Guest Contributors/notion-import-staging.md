# Guest Contributor Pipeline - Notion Import Staging

**Purpose:** High-level tracker for Notion. Detailed work stays in markdown vault.

**Notion Database Schema:**
- Name (title)
- Email (email)
- Status (select: Prospect / Pitched / Drafting / Review / Published / Declined)
- Topic (text)
- Warmth (number 1-5)
- Wave (select: 1 / 2 / 3 / 4)
- Vault Link (url - link to markdown folder)
- Last Contact (date)
- Notes (text)

---

## Wave 1: Ready to Execute

| Name | Email | Status | Topic | Warmth | Notes |
|------|-------|--------|-------|--------|-------|
| Amir Nathoo | [FILL] | Drafted | Network Schooling | 5 | Outschool CEO. Draft complete. |
| Jon England | [FILL] | Drafted | How to Start a Microschool | 4 | Libertas Institute. Draft ready. |
| Matt Beaudreau | [FILL] | Prospect | Microschooling (Apogee plug) | 4 | Will say yes. Gathering sources. |
| Mason Pashia | [FILL] | Pitched | Getting Smart collab | 4 | Active conversation Dec 2025. |
| Janssen Bradshaw | [FILL] | Agreed | Literacy/Reading (TBD) | 4 | AGREED. Needs SEO topic research. |
| Michael Velardo | [FILL] | Prospect | Netflix of Education | 3 | Subject.com founder. Via Hollie Sterling. |

---

## Wave 2: High Value Warm (Podcast → Article)

| Name | Email | Status | Topic | Warmth | Notes |
|------|-------|--------|-------|--------|-------|
| Peter Gray | [FILL] | Prospect | Self-Directed Education | 4 | THE academic authority. Podcast done. |
| Michael Horn | [FILL] | Prospect | Disruptive Innovation | 4 | Gave book blurb! Christensen Institute. |
| Ray Ravaglia | [FILL] | Prospect | Online School Philosophy | 4 | Stanford Online HS founder. |
| Connor Boyack | [FILL] | Prospect | Liberty Education / Tuttle Twins | 4 | Tuttle Twins creator. High reach. |
| Ben Somers | [FILL] | Prospect | TBD | 4 | Podcast done. Need angle. |

---

## Wave 3: Strategic (Need Topic Discovery)

| Name | Email | Status | Topic | Warmth | Notes |
|------|-------|--------|-------|--------|-------|
| Lenore Skenazy | [FILL] | Prospect | Free-Range Education | 3 | 46.7K X followers. High value. |
| Em Liebtag | emily@educationreimagined.org | Prospect | Learner-Centered Ed | 3 | Education Reimagined. Blog post discussed. |
| Hannah Frankman | [FILL] | Prospect | Post-COVID Education Trends | 4 | WARM. Review podcast. |
| Dr. Brian Ray | [FILL] | Prospect | Homeschool Research | 4 | NHERI founder. THE data guy. |
| Michelle Rhee | [FILL] | Prospect | Education Reform | 4 | Former DC Schools Chancellor. Controversial. |
| Joshua Fields Millburn | [FILL] | Prospect | Minimalism + Education | 4 | The Minimalists. High profile. |
| Claire Honeycutt | [FILL] | Pitched | Montessori / Joyful Learning | 3 | Outreach sent. Follow up. |
| Josh Rosenblat | [FILL] | Prospect | Synthesis / Game-Based Learning | 3 | "Synthesis at OpenEd" discussed. |

---

## Wave 4: Research Needed

| Name | Email | Status | Topic | Warmth | Notes |
|------|-------|--------|-------|--------|-------|
| Jenny (1000 Hours Outside) | [FIND] | Research | Outdoor Education | ? | Major IG. Create profile. |
| Ana Fabrega Lorenas | [FIND] | Research | TBD | ? | Need to research. |
| Getting Smart writers | [via Mason] | Research | Various | ? | Explore via Mason. |
| Matt Barnes | [FIND] | Research | TBD | ? | Need to research. |
| Austin Scholar | [FIND] | Research | TBD | ? | Need to research. |
| Roland Fryer | [FIND] | Research | Education Economics | ? | Harvard. Need warm intro. |
| McKenzie Price | [FIND] | Research | TBD | ? | Need to research. |

---

## CSV Export (for Notion import)

```csv
Name,Email,Status,Topic,Warmth,Wave,Notes
Amir Nathoo,,Drafted,Network Schooling,5,1,Outschool CEO. Draft complete.
Jon England,,Drafted,How to Start a Microschool,4,1,Libertas Institute. Draft ready.
Matt Beaudreau,,Prospect,Microschooling (Apogee plug),4,1,Will say yes. Gathering sources.
Mason Pashia,,Pitched,Getting Smart collab,4,1,Active conversation Dec 2025.
Janssen Bradshaw,,Agreed,Literacy/Reading (TBD),4,1,AGREED. Needs SEO topic.
Michael Velardo,,Prospect,Netflix of Education,3,1,Subject.com. Via Hollie Sterling.
Peter Gray,,Prospect,Self-Directed Education,4,2,THE academic authority.
Michael Horn,,Prospect,Disruptive Innovation,4,2,Gave book blurb!
Ray Ravaglia,,Prospect,Online School Philosophy,4,2,Stanford Online HS founder.
Connor Boyack,,Prospect,Liberty Education,4,2,Tuttle Twins creator.
Ben Somers,,Prospect,TBD,4,2,Need angle.
Lenore Skenazy,,Prospect,Free-Range Education,3,3,46.7K X followers.
Em Liebtag,emily@educationreimagined.org,Prospect,Learner-Centered Ed,3,3,Education Reimagined.
Hannah Frankman,,Prospect,Post-COVID Trends,4,3,WARM. Review podcast.
Dr. Brian Ray,,Prospect,Homeschool Research,4,3,NHERI founder.
Michelle Rhee,,Prospect,Education Reform,4,3,Former DC Schools Chancellor.
Joshua Fields Millburn,,Prospect,Minimalism + Education,4,3,The Minimalists.
Claire Honeycutt,,Pitched,Montessori,3,3,Outreach sent.
Josh Rosenblat,,Prospect,Synthesis,3,3,Game-based learning.
Jenny (1000 Hours Outside),,Research,Outdoor Education,,4,Major IG presence.
Ana Fabrega Lorenas,,Research,TBD,,4,Need to research.
Matt Barnes,,Research,TBD,,4,Need to research.
Austin Scholar,,Research,TBD,,4,Need to research.
Roland Fryer,,Research,Education Economics,,4,Harvard. Need warm intro.
McKenzie Price,,Research,TBD,,4,Need to research.
```

---

## Vault Links (add to Notion after import)

| Name | Vault Path |
|------|------------|
| Matt Beaudreau | `Guest Contributors/contributors/matt-beaudreau/` |
| Janssen Bradshaw | `Guest Contributors/contributors/janssen-bradshaw/` |
| Michael Velardo | `Guest Contributors/contributors/michael-velardo/` |

---

## Next Steps

1. Fill in email addresses from CRM/contacts
2. Import CSV to Notion as new database
3. Add vault links as URL property
4. Create Kanban view by Status
5. Keep Notion as tracking layer, do actual work in markdown

---

*Staged: 2026-01-26*
