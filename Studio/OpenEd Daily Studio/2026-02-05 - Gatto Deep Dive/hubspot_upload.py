import requests, os, json

TOKEN = os.environ["HUBSPOT_KEY"]
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

IMAGE_URL = "https://45961901.fs1.hubspotusercontent-na1.net/hubfs/45961901/newsletters/2026-02/tribute.jpg"
BLOG_URL = "https://opened.co/blog/5369"
WSJ_URL = "https://www.educationrevolution.org/blog/i-quit-i-think/"
UNDERGROUND_URL = "https://www.johntaylorgatto.com/underground/"
ARCHIVE_URL = "https://archive.org/details/john-taylor-gatto-archive-library-collection"

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Helvetica, Arial, sans-serif"
PS = f"font-family: {FONT}; font-size: 18px; line-height: 1.65; margin: 0 0 20px 0; color: #333333;"
H1S = f"font-family: {FONT}; font-weight: 700; font-size: 32px; margin: 40px 0 20px 0; text-align: center; color: #333333; line-height: 1.25;"
LS = "color: #03a4ea !important; text-decoration: underline; font-size: 18px; font-family: inherit; line-height: inherit;"
HRS = "border: none; border-top: 1px solid #e0e0e0; margin: 24px 0;"

SQ = "'"  # single quote for use in f-strings

body_html = f"""
<p style="{PS}">Greetings Eddies!</p>

<p style="{PS}">Last year, we published a short piece on John Taylor Gatto - the three-time NYC Teacher of the Year who quit in the Wall Street Journal. It did well enough to land on the second page of Google{SQ}s rankings for his name. We{SQ}d love to push it to the first page, because anyone searching for John Taylor Gatto deserves to find the connection between his work and what{SQ}s happening in education right now.</p>

<p style="{PS}">So we went back in, rewrote it, and gave it the depth it deserved. Gatto was the modern-day prophet of what we{SQ}re watching unfold several decades later. Every few months, another wave of stories hits about homeschool kids &ldquo;falling behind&rdquo; - but nobody asks: compared to what? Gatto asked that question 30 years ago. The open education movement is his legacy in action.</p>

<p style="{PS}">Here{SQ}s our updated deep dive.</p>

<p style="{PS}">&ndash; Charlie (the OpenEd newsletter guy)</p>

<hr style="{HRS}">

<center><a href="{BLOG_URL}"><img src="{IMAGE_URL}" width="600" height="338" style="width: 600px; height: auto; max-width: 600px; margin-left: auto; margin-right: auto; display: block;" align="center"></a></center>

<h1 style="{H1S}">John Taylor Gatto: The Award-Winning Teacher Who Quit to Tell the Truth</h1>

<p style="{PS}">In 1991, John Taylor Gatto did something that shocked the education world. Just months after being named New York State Teacher of the Year, he quit. Not quietly into retirement, but loudly, with a scathing <a href="{WSJ_URL}" style="{LS}"><em>Wall Street Journal</em> op-ed</a> announcing: &ldquo;I can{SQ}t teach this way any longer. If you hear of a job where I don{SQ}t have to hurt kids to make a living, let me know.&rdquo;</p>

<p style="{PS}">&ldquo;Schooling is a form of adoption,&rdquo; Gatto later wrote. &ldquo;You give your kid away at his most plastic years to a group of strangers.&rdquo;</p>

<p style="{PS}">After 30 years in New York City public schools and multiple teaching awards, Gatto walked away at the peak of his career. Why would a celebrated educator abandon the classroom? Because he had observed patterns in the educational system that had little to do with academics and everything to do with diminishing children{SQ}s natural curiosity and potential.</p>

<p style="{PS}">Before Gatto ever stood in front of a classroom, he had lived more lives than most teachers could imagine. A Columbia University graduate, he spent years outside academia entirely - driving a cab through New York City streets, writing advertising copy for Madison Avenue agencies, designing jewelry, and even crafting speeches for political figures including Richard Nixon and Spiro Agnew.</p>

<p style="{PS}">This wasn{SQ}t aimless wandering. Each job taught him something about how the &ldquo;real world&rdquo; actually worked - the world that schools supposedly prepared children for. He watched how successful people operated, noticed what skills actually mattered, and saw firsthand that credentials often mattered less than curiosity and adaptability.</p>

<p style="{PS}">When Gatto finally entered teaching, he brought these lessons with him. He was anything but conventional: he sent students on independent research projects at public libraries, arranged for shy 13-year-olds to interview legislators at the state capitol, and connected &ldquo;at-risk&rdquo; students with real apprenticeships and authentic experiences.</p>

<p style="{PS}">These unorthodox methods earned him recognition as New York City Teacher of the Year three times. But the longer he taught, the more Gatto noticed a troubling disconnect between what schools claimed to do and what they actually accomplished. In his State Teacher of the Year acceptance speech, he stunned the audience by outlining what he called &ldquo;The Seven-Lesson Schoolteacher&rdquo; - the hidden curriculum he believed all institutional schools inevitably teach.</p>

<p style="{PS}"><strong>Confusion.</strong> Everything taught out of context. History separated from literature, math from science, all divided into arbitrary periods marked by bells.</p>

<p style="{PS}"><strong>Class position.</strong> Children sorted, ranked, and labeled from their earliest years. Gifted, average, remedial. &ldquo;I{SQ}m not a math person&rdquo; becomes a self-fulfilling prophecy.</p>

<p style="{PS}"><strong>Indifference.</strong> When the bell rings, drop whatever you{SQ}re doing. This teaches children not to care too deeply about anything.</p>

<p style="{PS}"><strong>Emotional dependency.</strong> &ldquo;By using stars and red checks, smiles and frowns, prizes and punishments, I force children to become emotionally dependent upon my praise,&rdquo; Gatto confessed.</p>

<p style="{PS}">And three more lessons that cut even deeper - about intellectual dependency, provisional self-esteem, and the normalization of constant surveillance.</p>

<p style="{PS}">The longer you sit with Gatto{SQ}s seven lessons, the harder they are to unsee.</p>

<p style="{PS}"><a href="{BLOG_URL}" style="{LS}"><strong>Read the full deep dive</strong></a></p>

<hr style="{HRS}">

<p style="{PS}">That{SQ}s all for today!</p>

<p style="{PS}">&ndash; Charlie (the OpenEd newsletter guy)</p>

<p style="{PS}">P.S. Gatto{SQ}s most ambitious work, <em>The Underground History of American Education</em>, is <a href="{UNDERGROUND_URL}" style="{LS}">available free online</a>. All three of his major books can also be found on the <a href="{ARCHIVE_URL}" style="{LS}">Internet Archive</a>.</p>
"""

# Find most recent OED email to clone
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

# Clone it
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

# Update metadata
subject = "He won Teacher of the Year. Then he quit."
preview = "NYC's best teacher quit in the Wall Street Journal. His critique of the \"hidden curriculum\" is more relevant than ever."
email_name = "2.5 OED - Gatto Deep Dive"

print("Updating metadata...")
meta_resp = requests.patch(
    f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
    headers=headers,
    json={"name": email_name, "subject": subject}
)
print(f"Metadata: {meta_resp.status_code}")

# Update content
print("Updating content...")
content_resp = requests.patch(
    f"https://api.hubapi.com/marketing/v3/emails/{clone_id}",
    headers=headers,
    json={
        "content": {
            "widgets": {
                "deep_dive_content": {"body": {"html": body_html}},
                "preview_text": {"body": {"value": preview}}
            }
        }
    }
)
print(f"Content: {content_resp.status_code}")
if content_resp.status_code != 200:
    print(f"Response: {content_resp.text[:500]}")

print(f"\nDraft ready: https://app.hubspot.com/email/{clone_id}/edit")
