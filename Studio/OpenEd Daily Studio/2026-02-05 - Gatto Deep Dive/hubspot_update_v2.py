import requests, os

TOKEN = os.environ["HUBSPOT_KEY"]
CLONE_ID = "206879068814"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

IMAGE_URL = "https://45961901.fs1.hubspotusercontent-na1.net/hubfs/45961901/newsletters/2026-02/tribute.jpg"
BLOG_URL = "https://opened.co/blog/5369"
WSJ_URL = "https://www.educationrevolution.org/blog/i-quit-i-think/"
UNDERGROUND_URL = "https://www.johntaylorgatto.com/underground/"
ARCHIVE_URL = "https://archive.org/details/john-taylor-gatto-archive-library-collection"

# Clean HTML - no inline styles. Let HubSpot template handle fonts.
body_html = """
<p>Greetings Eddies!</p>

<p>Last year, we published a blog post on John Taylor Gatto - the three-time NYC Teacher of the Year who publicly resigned in the pages of <a href="{wsj}">the Wall Street Journal</a>. The post resonated enough that it landed on the second page of Google\u2019s rankings for his name (#11 - the top 10 show up on the first page of results). We\u2019d love to push it to the first page, so that anyone searching for John Taylor Gatto can discover the connection between his work and what\u2019s happening in education right now.</p>

<p>So we went back in, rewrote it, and gave it the depth it deserved. Gatto was a modern-day prophet of what we\u2019re watching unfold several decades later. The open education movement is his legacy in action.</p>

<p>Here\u2019s our updated deep dive.</p>

<p>\u2013 Charlie (the OpenEd newsletter guy)</p>

<hr>

<center><a href="{blog}"><img src="{img}" width="600" height="338" style="width: 600px; height: auto; max-width: 600px; margin-left: auto; margin-right: auto; display: block;" align="center"></a></center>

<h1><strong>John Taylor Gatto: The Award-Winning Teacher Who Quit to Tell the Truth</strong></h1>

<p>In 1991, John Taylor Gatto did something that shocked the education world. Just months after being named New York State Teacher of the Year, he quit. Not quietly into retirement, but loudly, with a scathing <a href="{wsj}"><em>Wall Street Journal</em> op-ed</a> announcing: \u201CI can\u2019t teach this way any longer. If you hear of a job where I don\u2019t have to hurt kids to make a living, let me know.\u201D</p>

<p>\u201CSchooling is a form of adoption,\u201D Gatto later wrote. \u201CYou give your kid away at his most plastic years to a group of strangers.\u201D</p>

<p>After 30 years in New York City public schools and multiple teaching awards, Gatto walked away at the peak of his career. Why would a celebrated educator abandon the classroom? Because he had observed patterns in the educational system that had little to do with academics and everything to do with diminishing children\u2019s natural curiosity and potential.</p>

<p>Before Gatto ever stood in front of a classroom, he had lived more lives than most teachers could imagine. A Columbia University graduate, he spent years outside academia entirely - driving a cab through New York City streets, writing advertising copy for Madison Avenue agencies, designing jewelry, and even crafting speeches for political figures including Richard Nixon and Spiro Agnew.</p>

<p>This wasn\u2019t aimless wandering. Each job taught him something about how the \u201Creal world\u201D actually worked - the world that schools supposedly prepared children for. He watched how successful people operated, noticed what skills actually mattered, and saw firsthand that credentials often mattered less than curiosity and adaptability.</p>

<p>When Gatto finally entered teaching, he brought these lessons with him. He was anything but conventional: he sent students on independent research projects at public libraries, arranged for shy 13-year-olds to interview legislators at the state capitol, and connected \u201Cat-risk\u201D students with real apprenticeships and authentic experiences.</p>

<p>These unorthodox methods earned him recognition as New York City Teacher of the Year three times. But the longer he taught, the more Gatto noticed a troubling disconnect between what schools claimed to do and what they actually accomplished. In his State Teacher of the Year acceptance speech, he stunned the audience by outlining what he called \u201CThe Seven-Lesson Schoolteacher\u201D - the hidden curriculum he believed all institutional schools inevitably teach.</p>

<ol>
<li><strong>Confusion.</strong> Everything taught out of context. History separated from literature, math from science, all divided into arbitrary periods marked by bells.</li>
<li><strong>Class position.</strong> Children sorted, ranked, and labeled from their earliest years. Gifted, average, remedial. \u201CI\u2019m not a math person\u201D becomes a self-fulfilling prophecy.</li>
<li><strong>Indifference.</strong> When the bell rings, drop whatever you\u2019re doing. This teaches children not to care too deeply about anything.</li>
<li><strong>Emotional dependency.</strong> \u201CBy using stars and red checks, smiles and frowns, prizes and punishments, I force children to become emotionally dependent upon my praise,\u201D Gatto confessed.</li>
</ol>

<p>And three more lessons that cut even deeper - about intellectual dependency, provisional self-esteem, and the normalization of constant surveillance.</p>

<p>The longer you sit with Gatto\u2019s seven lessons, the harder they are to unsee.</p>

<p><a href="{blog}"><strong>Read the full deep dive</strong></a></p>

<hr>

<p>That\u2019s all for today!</p>

<p>\u2013 Charlie (the OpenEd newsletter guy)</p>

<p>P.S. Gatto\u2019s most ambitious work, <em>The Underground History of American Education</em>, is <a href="{underground}">available free online</a>. All three of his major books can also be found on the <a href="{archive}">Internet Archive</a>.</p>
""".format(
    wsj=WSJ_URL,
    blog=BLOG_URL,
    img=IMAGE_URL,
    underground=UNDERGROUND_URL,
    archive=ARCHIVE_URL
)

preview = "We wrote about Gatto and it landed on Google page 2. Here\u2019s the updated deep dive."

print("Updating with clean HTML (no inline font styles)...")
content_resp = requests.patch(
    f"https://api.hubapi.com/marketing/v3/emails/{CLONE_ID}",
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
print(f"Content update: {content_resp.status_code}")
if content_resp.status_code != 200:
    print(f"Response: {content_resp.text[:500]}")
else:
    print(f"\nDraft updated: https://app.hubspot.com/email/{CLONE_ID}/edit")
