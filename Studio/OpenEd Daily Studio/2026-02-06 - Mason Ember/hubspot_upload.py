import requests, os, json

TOKEN = os.environ.get("HUBSPOT_KEY")
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

BLOG_URL = "https://opened.co/blog/a-16-year-old-filmmaker-spent-a-year-documenting-homeschoolers-heres-what-he-found"
ATG_URL = "https://www.againstthegrade.com/"
NYT_URL = "https://www.nytimes.com/2025/12/24/opinion/letters/home-schooling-debate.html"
MASON_IG = "https://www.instagram.com/embers_insta/"

# Step 1: Upload thumbnail image to HubSpot
IMG_PATH = os.path.join(os.path.dirname(__file__), "mason-ember-bookclub.jpg")
print("Uploading thumbnail to HubSpot...")
upload_headers = {"Authorization": f"Bearer {TOKEN}"}
with open(IMG_PATH, "rb") as f:
    upload_resp = requests.post(
        "https://api.hubapi.com/filemanager/api/v3/files/upload",
        headers=upload_headers,
        data={
            "options": json.dumps({
                "access": "PUBLIC_INDEXABLE",
                "overwrite": True,
                "duplicateValidationStrategy": "NONE",
                "duplicateValidationScope": "ENTIRE_PORTAL"
            }),
            "folderPath": "/newsletters/2026-02"
        },
        files={"file": ("mason-ember-bookclub.jpg", f, "image/jpeg")}
    )
if upload_resp.status_code in (200, 201):
    IMAGE_URL = upload_resp.json().get("objects", [{}])[0].get("url", "") if "objects" in upload_resp.json() else upload_resp.json().get("url", "")
    print(f"Image uploaded: {IMAGE_URL}")
else:
    print(f"Image upload failed: {upload_resp.status_code} {upload_resp.text[:300]}")
    print("Falling back to placeholder...")
    IMAGE_URL = ""

# Style constants - ALL properties need !important for mobile override
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"
PS = f"font-family: {FONT} !important; font-size: 18px !important; line-height: 1.65 !important; margin: 0 0 20px 0 !important; color: #333333 !important;"
H1S = f"font-family: {FONT} !important; font-weight: 700 !important; font-size: 32px !important; margin: 40px 0 20px 0 !important; text-align: center !important; color: #333333 !important; line-height: 1.25 !important;"
H2S = f"font-family: {FONT} !important; font-weight: 700 !important; font-size: 24px !important; margin: 32px 0 16px 0 !important; color: #333333 !important; line-height: 1.3 !important;"
LS = "color: #03a4ea !important; text-decoration: underline !important; font-size: 18px !important; font-family: inherit !important; line-height: inherit !important;"
HRS = "border: none !important; border-top: 1px solid #e0e0e0 !important; margin: 24px 0 !important;"
BYS = f"font-family: {FONT} !important; font-size: 16px !important; font-style: italic !important; color: #666666 !important; margin: 0 0 24px 0 !important; text-align: center !important;"

SQ = "'"

body_html = f"""
<p style="{PS}">Greetings Eddies!</p>

<p style="{PS}">Most of what we share about open education and homeschooling is written by parents, teachers, researchers, and policy people. Fair enough - they know things. But today we get to hear from someone who{SQ}s actually living it right now.</p>

<p style="{PS}">Mason Ember is 16. He{SQ}s been homeschooled his entire life and has spent the past year filming a feature-length documentary called <em>Against the Grade</em>, following four teenagers with radically different approaches to education. When the New York Times published &ldquo;The Home-Schooled Kids Are Not All Right&rdquo; during that process, he wrote a response and got it published in their letters section.</p>

<p style="{PS}">We constantly ask parents and experts what children need. We rarely ask the kids. Here{SQ}s the opening of our conversation.</p>

<p style="{PS}">&ndash; Charlie</p>

<hr style="{HRS}">

<center><a href="{BLOG_URL}"><img src="{IMAGE_URL}" width="600" height="338" style="width: 600px; height: auto; max-width: 600px; margin-left: auto; margin-right: auto; display: block;" align="center"></a></center>

<h1 style="{H1S}">A 16-Year-Old Filmmaker Spent a Year Documenting Homeschoolers. Here{SQ}s What He Found.</h1>

<p style="{BYS}">By Ela Richmond</p>

<p style="{PS}">Ten teenagers sit in a New York apartment reading <em>Madame Bovary</em>. No parents. No teachers. No one telling them to stay on task. One of them organized the whole thing - the books, the food, the museum trips they take together afterward. Sometimes she makes enough dinner for everyone. Sometimes people go home hungry. She figures it out.</p>

<p style="{PS}">The person who showed me this scene is 16 years old.</p>

<p style="{PS}">Mason Ember is a filmmaker, a lifelong homeschooler, and the creator of a documentary called <a href="{ATG_URL}" style="{LS}"><em>Against the Grade</em></a>, which follows four teenagers with radically different approaches to education. He{SQ}s not reflecting on childhood from adulthood. He{SQ}s living it right now - filming his subjects while simultaneously building his own education in real time. When the New York Times published a guest essay titled &ldquo;The Home-Schooled Kids Are Not All Right,&rdquo; Mason <a href="{NYT_URL}" style="{LS}">wrote a response</a> that got published in their letters section. His message was simple: anybody can mess up education when they stop paying attention to what individual kids actually need.</p>

<h2 style="{H2S}">The Preschool Dropout</h2>

<p style="{PS}">Mason went to preschool briefly at the Blue School in Manhattan - founded by a member of the Blue Man Group, arts-focused, and as progressive as it gets. It should have been a perfect fit for a curious, creative kid. It lasted two months.</p>

<p style="{PS}">The way he tells it: he was at an art easel, finger painting, totally absorbed. A teacher told him it was time for group sing-along. He argued with her. He wanted to stay with the painting. He was maybe four years old.</p>

<p style="{PS}">His parents pulled him out and tried homeschooling. Not as a permanent ideology - as an experiment. Year by year, they checked in. Is he learning what he needs? Is this still working? Every year, the answer was yes.</p>

<p style="{PS}">What followed was a childhood that looks incoherent from the outside and makes total sense from the inside. Mason wanted to be a stage magician. Then a chef. Then a comedian. Then a pilot. Then a filmmaker. His parents let him chase each one. His mom told him later: &ldquo;I didn{SQ}t really want you to become a stage magician.&rdquo; But she let him explore it for a year anyway.</p>

<p style="{PS}">His parents did something subtle, though. They didn{SQ}t see &ldquo;film&rdquo; as his through-line. They saw <em>storytelling</em>. Whether he was making cooking shows in the basement at eight, writing jokes for a comedy show he produced, or creating a feature-length documentary at sixteen, the skill beneath the skill stayed consistent. So even today, when they talk about his future, they don{SQ}t talk about film. They talk about stories.</p>

<p style="{PS}">The part of our conversation that surprised me most came later - when Mason shared two honest criticisms of homeschooling that even its biggest advocates need to hear.</p>

<p style="{PS}"><a href="{BLOG_URL}" style="{LS}"><strong>Watch or Read the Whole Thing &rarr;</strong></a></p>

<hr style="{HRS}">

<p style="{PS}">That{SQ}s all for today!</p>

<p style="{PS}">&ndash; Charlie</p>

<p style="{PS}">P.S. Mason{SQ}s documentary <em>Against the Grade</em> is currently being submitted to film festivals. Sign up at <a href="{ATG_URL}" style="{LS}">againstthegrade.com</a> to find out when you can watch it. Follow Mason on <a href="{MASON_IG}" style="{LS}">Instagram</a>.</p>
"""

# Step 2: Find most recent OED email to clone
print("Finding most recent OED email...")
resp = requests.get(
    "https://api.hubapi.com/email/public/v1/campaigns",
    headers=headers,
    params={"limit": 100}
)
campaigns = resp.json().get("campaigns", [])

content_id = None
for c in campaigns:
    detail = requests.get(
        f"https://api.hubapi.com/email/public/v1/campaigns/{c['id']}",
        headers=headers
    ).json()
    name = detail.get("name", "")
    email_type = detail.get("type", "")
    is_batch = email_type == "BATCH_EMAIL"
    is_oed = " OED " in name or " OED -" in name or " OEW " in name
    if is_batch and is_oed:
        print(f"Found template: {name}")
        content_id = detail.get("contentId")
        break

if not content_id:
    print("ERROR: No OED email found")
    exit(1)

# Step 3: Clone it
print("Cloning template...")
clone_resp = requests.post(
    "https://api.hubapi.com/marketing/v3/emails/clone",
    headers=headers,
    json={"id": str(content_id)}
)
if clone_resp.status_code != 200:
    print(f"Clone failed: {clone_resp.status_code} {clone_resp.text[:300]}")
    exit(1)

clone_id = clone_resp.json()["id"]
print(f"Cloned as: {clone_id}")

# Step 4: Update metadata
subject = "A 16-year-old responds to the New York Times"
preview = "He dropped out of preschool. Now he's making a documentary about education."
email_name = "2.6 OED - Mason Ember"

print("Updating metadata...")
meta_resp = requests.patch(
    f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
    headers=headers,
    json={"name": email_name, "subject": subject}
)
print(f"Metadata: {meta_resp.status_code}")

# Step 5: Update content (both widgets for mobile safety)
print("Updating content...")
content_resp = requests.patch(
    f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
    headers=headers,
    json={
        "content": {
            "widgets": {
                "deep_dive_content": {"body": {"html": body_html}},
                "hs_email_body": {"body": {"html": body_html}},
                "preview_text": {"body": {"value": preview}}
            }
        }
    }
)
print(f"Content: {content_resp.status_code}")
if content_resp.status_code != 200:
    print(f"Response: {content_resp.text[:500]}")

print(f"\nDraft ready: https://app.hubspot.com/email/{clone_id}/edit")
