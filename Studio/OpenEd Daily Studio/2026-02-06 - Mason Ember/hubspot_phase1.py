"""
Phase 1: Mason Ember Email - Bulletproof Widget-Preserving Upload
=================================================================
Key fix: After cloning, GET the full email to extract complete widget
objects (with module_id, type, name, etc.), then replace ONLY body.html
inside each widget, preserving all metadata HubSpot needs to render.
"""
import requests, os, json, sys

# Token with email scopes (seomachine config)
TOKEN = os.environ.get("HUBSPOT_KEY")
PORTAL = "45961901"
GATTO_EMAIL_ID = "206886611767"  # Known working email

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# URLs
BLOG_URL = "https://opened.co/blog/a-16-year-old-filmmaker-spent-a-year-documenting-homeschoolers-heres-what-he-found"
ATG_URL = "https://www.againstthegrade.com/"
NYT_URL = "https://www.nytimes.com/2025/12/24/opinion/letters/home-schooling-debate.html"
MASON_IG = "https://www.instagram.com/embers_insta/"

# ── Step 1: Upload thumbnail image ──────────────────────────────────
IMG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mason-ember-bookclub.jpg")
print(f"[1/6] Uploading thumbnail: {IMG_PATH}")

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
    resp_json = upload_resp.json()
    IMAGE_URL = resp_json.get("url", "") or resp_json.get("objects", [{}])[0].get("url", "")
    print(f"   Image uploaded: {IMAGE_URL}")
else:
    # Fallback to constructed URL
    IMAGE_URL = f"https://{PORTAL}.fs1.hubspotusercontent-na1.net/hubfs/{PORTAL}/newsletters/2026-02/mason-ember-bookclub.jpg"
    print(f"   Image upload returned {upload_resp.status_code}, using fallback: {IMAGE_URL}")

# ── Step 2: Build HTML ──────────────────────────────────────────────
# All styles use !important to override template @media queries on mobile
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"
PS = f"font-family: {FONT} !important; font-size: 18px !important; line-height: 1.65 !important; margin: 0 0 20px 0 !important; color: #333333 !important;"
H1S = f"font-family: {FONT} !important; font-weight: 700 !important; font-size: 32px !important; margin: 40px 0 20px 0 !important; text-align: center !important; color: #333333 !important; line-height: 1.25 !important;"
H2S = f"font-family: {FONT} !important; font-weight: 700 !important; font-size: 24px !important; margin: 32px 0 16px 0 !important; color: #333333 !important; line-height: 1.3 !important;"
LS = "color: #03a4ea !important; text-decoration: underline !important; font-size: 18px !important; font-family: inherit !important; line-height: inherit !important;"
HRS = "border: none !important; border-top: 1px solid #e0e0e0 !important; margin: 24px 0 !important;"
BYS = f"font-family: {FONT} !important; font-size: 16px !important; font-style: italic !important; color: #666666 !important; margin: 0 0 24px 0 !important; text-align: center !important;"
CTAS = f"text-align: center !important; margin: 24px 0 !important; font-family: {FONT} !important; font-size: 18px !important; line-height: 1.65 !important; color: #333333 !important;"

body_html = f'''<p style="{PS}">Greetings Eddies!</p>

<p style="{PS}">Most of what we share about open education and homeschooling is written by parents, teachers, researchers, and policy people. Fair enough - they know things. But today we get to hear from someone who\u2019s actually living it right now.</p>

<p style="{PS}">Mason Ember is 16. He\u2019s been homeschooled his entire life and has spent the past year filming a feature-length documentary called <em>Against the Grade</em>, following four teenagers with radically different approaches to education. When the New York Times published \u201cThe Home-Schooled Kids Are Not All Right\u201d during that process, he wrote a response and got it published in their letters section.</p>

<p style="{PS}">We constantly ask parents and experts what children need. We rarely ask the kids. Here\u2019s the opening of our conversation.</p>

<p style="{PS}">\u2013 Charlie</p>

<hr style="{HRS}">

<center><a href="{BLOG_URL}"><img src="{IMAGE_URL}" width="600" height="338" style="width: 600px !important; height: auto !important; max-width: 600px !important; margin-left: auto !important; margin-right: auto !important; display: block !important;" align="center"></a></center>

<h1 style="{H1S}">A 16-Year-Old Filmmaker Spent a Year Documenting Homeschoolers. Here\u2019s What He Found.</h1>

<p style="{BYS}">By Ela Richmond</p>

<p style="{PS}">Ten teenagers sit in a New York apartment reading <em>Madame Bovary</em>. No parents. No teachers. No one telling them to stay on task. One of them organized the whole thing - the books, the food, the museum trips they take together afterward. Sometimes she makes enough dinner for everyone. Sometimes people go home hungry. She figures it out.</p>

<p style="{PS}">The person who showed me this scene is 16 years old.</p>

<p style="{PS}">Mason Ember is a filmmaker, a lifelong homeschooler, and the creator of a documentary called <a href="{ATG_URL}" style="{LS}"><em>Against the Grade</em></a>, which follows four teenagers with radically different approaches to education. He\u2019s not reflecting on childhood from adulthood. He\u2019s living it right now - filming his subjects while simultaneously building his own education in real time. When the New York Times published a guest essay titled \u201cThe Home-Schooled Kids Are Not All Right,\u201d Mason <a href="{NYT_URL}" style="{LS}">wrote a response</a> that got published in their letters section. His message was simple: anybody can mess up education when they stop paying attention to what individual kids actually need.</p>

<h2 style="{H2S}">The Preschool Dropout</h2>

<p style="{PS}">Mason went to preschool briefly at the Blue School in Manhattan - founded by a member of the Blue Man Group, arts-focused, and as progressive as it gets. It should have been a perfect fit for a curious, creative kid. It lasted two months.</p>

<p style="{PS}">The way he tells it: he was at an art easel, finger painting, totally absorbed. A teacher told him it was time for group sing-along. He argued with her. He wanted to stay with the painting. He was maybe four years old.</p>

<p style="{PS}">His parents pulled him out and tried homeschooling. Not as a permanent ideology - as an experiment. Year by year, they checked in. Is he learning what he needs? Is this still working? Every year, the answer was yes.</p>

<p style="{PS}">What followed was a childhood that looks incoherent from the outside and makes total sense from the inside. Mason wanted to be a stage magician. Then a chef. Then a comedian. Then a pilot. Then a filmmaker. His parents let him chase each one. His mom told him later: \u201cI didn\u2019t really want you to become a stage magician.\u201d But she let him explore it for a year anyway.</p>

<p style="{PS}">His parents did something subtle, though. They didn\u2019t see \u201cfilm\u201d as his through-line. They saw <em>storytelling</em>. Whether he was making cooking shows in the basement at eight, writing jokes for a comedy show he produced, or creating a feature-length documentary at sixteen, the skill beneath the skill stayed consistent. So even today, when they talk about his future, they don\u2019t talk about film. They talk about stories.</p>

<p style="{PS}">The part of our conversation that surprised me most came later - when Mason shared two honest criticisms of homeschooling that even its biggest advocates need to hear.</p>

<p style="{CTAS}"><a href="{BLOG_URL}" style="{LS}"><strong>Watch or Read the Whole Thing &rarr;</strong></a></p>

<hr style="{HRS}">

<p style="{PS}">That\u2019s all for today!</p>

<p style="{PS}">\u2013 Charlie</p>

<p style="{PS}">P.S. Mason\u2019s documentary <em>Against the Grade</em> is currently being submitted to film festivals. Sign up at <a href="{ATG_URL}" style="{LS}">againstthegrade.com</a> to find out when you can watch it. Follow Mason on <a href="{MASON_IG}" style="{LS}">Instagram</a>.</p>'''

# ── Step 3: Clone the working Gatto email ───────────────────────────
print(f"\n[2/6] Cloning Gatto email {GATTO_EMAIL_ID}...")
clone_resp = requests.post(
    "https://api.hubapi.com/marketing/v3/emails/clone",
    headers=headers,
    json={"id": GATTO_EMAIL_ID}
)
if clone_resp.status_code != 200:
    print(f"   FAILED: {clone_resp.status_code} {clone_resp.text[:500]}")
    sys.exit(1)

clone_data = clone_resp.json()
clone_id = clone_data["id"]
print(f"   Cloned as: {clone_id}")

# ── Step 4: GET the full clone to see complete widget structure ─────
print(f"\n[3/6] Fetching full clone to extract widget metadata...")
get_resp = requests.get(
    f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
    headers=headers
)
if get_resp.status_code != 200:
    print(f"   FAILED to fetch clone: {get_resp.status_code} {get_resp.text[:500]}")
    sys.exit(1)

email_data = get_resp.json()
widgets = email_data.get("content", {}).get("widgets", {})

print(f"   Found widgets: {list(widgets.keys())}")
for wname, wdata in widgets.items():
    print(f"   Widget '{wname}' keys: {list(wdata.keys())}")

# ── Step 5: Preserve widget metadata, replace ONLY body.html ───────
print(f"\n[4/6] Building updated widgets (preserving all metadata)...")

updated_widgets = {}

# For each content widget, copy the ENTIRE object, only replace body.html
for widget_name in ["deep_dive_content", "hs_email_body"]:
    if widget_name in widgets:
        # Deep copy the full widget object
        widget_copy = json.loads(json.dumps(widgets[widget_name]))
        # Replace only the body HTML
        if "body" not in widget_copy:
            widget_copy["body"] = {}
        widget_copy["body"]["html"] = body_html
        updated_widgets[widget_name] = widget_copy
        print(f"   Updated '{widget_name}' (preserved keys: {list(widget_copy.keys())})")
    else:
        # Widget doesn't exist in template, create minimal version
        updated_widgets[widget_name] = {"body": {"html": body_html}}
        print(f"   Created '{widget_name}' (new - not in template)")

# Handle preview_text similarly
preview = "He dropped out of preschool. Now he\u2019s making a documentary about education."
if "preview_text" in widgets:
    preview_widget = json.loads(json.dumps(widgets["preview_text"]))
    if "body" not in preview_widget:
        preview_widget["body"] = {}
    preview_widget["body"]["value"] = preview
    updated_widgets["preview_text"] = preview_widget
    print(f"   Updated 'preview_text' (preserved keys: {list(preview_widget.keys())})")
else:
    updated_widgets["preview_text"] = {"body": {"value": preview}}
    print(f"   Created 'preview_text' (new)")

# ── Step 6: PATCH with metadata + preserved widgets ─────────────────
print(f"\n[5/6] Patching metadata...")
subject = "A 16-year-old responds to the New York Times"
email_name = "2.6 OED - Mason Ember"

meta_resp = requests.patch(
    f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
    headers=headers,
    json={"name": email_name, "subject": subject}
)
print(f"   Metadata: {meta_resp.status_code}")

print(f"\n[6/6] Patching content with preserved widget structure...")
content_resp = requests.patch(
    f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
    headers=headers,
    json={
        "content": {
            "widgets": updated_widgets
        }
    }
)
print(f"   Content: {content_resp.status_code}")
if content_resp.status_code != 200:
    print(f"   Response: {content_resp.text[:1000]}")
else:
    result = content_resp.json()
    # Verify the widgets came back correctly
    result_widgets = result.get("content", {}).get("widgets", {})
    print(f"   Result widgets: {list(result_widgets.keys())}")

print(f"\n{'='*60}")
print(f"Draft ready: https://app.hubspot.com/email/{PORTAL}/editor/{clone_id}/settings")
print(f"Direct edit: https://app.hubspot.com/email/{clone_id}/edit")
print(f"{'='*60}")
