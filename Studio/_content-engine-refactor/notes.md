Summary

### AI-Assisted Workflow Process

- The session demonstrated using AI to create spec sheets by pasting transcripts into chat and asking it to isolate conversations and generate actionable to-do lists
- Currently working in Zed (similar to Cursor) with agent mode, though preferring to work with multiple terminals simultaneously

### GitHub and Skills Repository Refactoring

- Successfully gained access to GitHub and is in the middle of a major refactor of the skills folder/repository
- Working on improving workflow clarity and addressing issues with siloed skills that need better triggers and flow
- Encountering challenges with broken references when chaining skills together during refactoring - comparing it to changing from one language to another in a codebase

### Curation Pipeline Project

- **Purpose**: Automated content discovery system that will scrape blogs and newsletters for relevant content
- **Delivery Method**: Daily morning reports delivered via Slack before wake-up time, containing articles with analysis explaining relevance
- **Content Sources**: Existing feeds, Google alerts, and keyword searches aggregated into daily news summaries
- **Filtering Capabilities**: Built-in gates to filter out irrelevant content (e.g., ESA/school choice news that triggers same keywords but is outside scope since the focus is on public schools, not school choice programs)
- **Iterative Improvement**: Ability to edit gates based on incoming content to refine what gets surfaced
- **Tool Integration**: Leverages existing Slack collaboration infrastructure rather than creating new tools

### Content Engine Structure and Workflows

- **Core Content Pillars**: Podcast, newsletter, and deep dive articles form the foundation of the content engine
- **Social Media Strategy**: Two types of social content - spoke content derived from pillar pieces and standalone social media optimized content
- **Workflow Evolution**: Shifting to a "socials first" approach where social posts are created before newsletter drafts, as social media frameworks often provide good suggestions for packaging core ideas
- **Integration with Telegram**: Using Claude bot assistant in Telegram to add notes to projects in the vault, such as optimizing funnels to point toward email subscriptions

### Skills Refactoring and Optimization

- **Hook and Headline Writer**: Previously combined hooks, headlines, and newsletter subject lines - now broken into separate, more focused skills
- **Newsletter Subject Lines**: Now its own dedicated skill with framework patterns and reference library
- **Article Titles**: Restored with 15 proven formulas in the formula library
- **Issues with Previous Skills**: Earlier versions had lost valuable content and examples, becoming too thin and ineffective (described as "photocopy of a photocopy")

### Philosophy on Skill Design

- **Examples Over Instructions**: Core philosophy that output examples are worth more than extensive instructions
- **Key Principle**: If you can define what good output looks like, you've written a good skill - instructions are almost secondary
- **Best Practice**: Skills should use examples to do the heavy lifting, with instructions bolstering examples to guide the input-to-output translation process
- **Application**: This philosophy applies broadly, including to comic/humor skills - examples of what's funny are more effective than describing humor
- **Implementation Need**: More core substance and examples should be added directly to skills rather than relegated to reference files

### YouTube Clip Extractor Demonstration

- **Tools Required**: YTDLP (scraping tool for downloading from YouTube and other sources) and FFmpeg (video encoding/parsing tool) - may need installation on first run
- **Workflow**: Works in conjunction with YouTube Downloader skill
- **Capabilities**: Automated clip identification based on hook/coda criteria
- **Improved Process**: Now can extract captions and use FFmpeg to download and cut clips automatically, eliminating previous manual workflow of downloading video, importing to Script, and cutting clips
- **Testing**: Demonstrated on a vintage Phil Donahue interview with John Holt about homeschooling (58-minute episode)
- **Content Strategy**: Using vintage/archival content as a way to stand out from AI-generated content - competing with different kinds of visual engagement

### Technical Environment

- Working in Zed editor with agent mode, though preferring multiple terminal windows
- Using Claude in terminal with "dangerously skip permissions" flag for workflow operations
- Experiencing some performance issues requiring closing unused applications

### Action Items

- [ ]  Commit current work to GitHub
- [x]  Add philosophy about examples over instructions to the skill creator (2026-01-23)
- [x]  Audit YouTube Clip Extractor skill and ensure tools are properly hooked up (2026-01-23 - fixed broken references)
- [x]  Consider merging or keeping YouTube Downloader as reference (Decision: Keep separate - youtube-downloader for transcript-only, youtube-clip-extractor for full clip workflow)
- [x]  Add more core substance and examples directly to skills rather than reference files (Philosophy documented in skill-creator)
- [ ]  Complete testing of YouTube Clip Extractor on the Phil Donahue/John Holt video
- [ ]  Edit skill to handle post-clip import cleanup (mentioned as super important but not fully detailed)

### Additional Completed (2026-01-23)
- [x]  Created SKILL_ARCHITECTURE_MAP.md - comprehensive visual map of entire content engine
- [x]  Fixed broken references in video-caption-creation (4 fixes)
- [x]  Fixed youtube-downloader frontmatter name mismatch

Notes

Transcript

I just commented on little bugs that I was noticing and things that I wanted to improve. Then at the end of the call, I just paste the transcript into the chat and say, isolate that part of the conversation and turn it into a spec sheet for the next step of this. Similarly, this call, we will gear towards Giving us a clear to-do list and direction. So I'll share my screen if it lets me. to start, But pretty sweet that you were able to get into GitHub, if you ask me.

And I should probably do a commit sometime soon, although I'm in the middle of like a major refactor of the skills folder, skills repo. Because I realized that, let me see, my FaceTime here is a little bit screwy. I might have to... Oh, you can see my screen. Can't you? You can't? Hold on a second. So let me stop sharing and then start sharing again. Share my screen. Here we go. Share all application windows.

Now do you see meeting here?

All right. So back over in this is Zed just like cursor pretty much I just I like the interface a little better And I've mostly been working in the terminal anyway They also have the agent mode on the side but you can only have one window open at a time and I like to cook with at least two terminals going at once so So here, this has been working on some task for like eight minutes. That's kind of crazy.

I don't know. I feel like it might be getting hung up on something. But I created sort of a... Yeah, I created a temporary project for this. And I think that this will kind of help maybe situate us a little bit. Curation Pipeline, this is a sub project that I want to get going eventually where it will drop suggestions for like the daily or for standalone social posts. It's like scraping other blogs and newsletters and just looking for relevant content.

And once probably once a day, like in the morning before I wake up, it'll just deliver a report in the Slack with each of the articles as like a little post and maybe sort of a little analysis. Like, here's why I thought it would be relevant. So it'll take actually all of our existing feeds, plus some like Google alerts or just general keyword searches and deposit like here's the daily, here's the news of the day.

Here are some things that you might want to vibe with. And it'll also have sort of some gates on that content because there's the stuff that triggers the keyword. But like we don't like to cover ESA news really because that's just out of our wheelhouse. That's a school choice issue. We're not a school choice program. We work with public schools. But oftentimes the same keywords that will trigger things that are relevant will also pull that stuff in.

So it'll kind of filter out some of the stuff that we don't want. And we'll be able to edit the gates as stuff comes in. We'll be like, yeah, that was good. But you know what? Like this one, we want less stuff like this, more stuff like that. And it will just come right into Slack, which is already a tool that I use for collaboration. So we're not like generating new tools. We're just repurposing our existing tools.

Sort of like how this Claude bot assistant uses telegram. I can send it like here today. I said, you know, add a note to the whoops. Add a note to the content engine refactor project in, I said, open at vault in the studio to make a point of optimizing all of the funnels for the social media channels. Research, oh, whoops, that's actually wrong. I meant to say optimizing all of the funnels to point towards email subscriptions.

It kind of figured it out. It kind of figured it out somewhat.

Um, But yeah, so then it should have added this note, phase nine. It found the document. And in this plan here, in this, let's see, checklist, let's see if it added phase nine. Oh, wait a second. There it is, phase nine. By the way, Are you kidding me? I said share all windows, what the heck? Hold on a second Screen sharing. Ask to share. No, no, I don't want to ask to share. share my screen. and share entire screen.

Can you see Zed? Yeah. All right. Cool. And now this is still working. Dang. Okay. I think the problem, I think it's what it's doing. So I... The issue that I was encountering was that, you know, I have my skills largely kind of like siloed and I want them to sort of trigger. I want to come up with a little bit more of a clear Clear flow. And let me see if I can find... sort of the because I thought I had made Pretty good map in ASCII, but now I can't find it.

Instagram workflows. That's not it plan that's not it Dang. Okay, this is finishing up and it's compacting the conversation. So I think I'll be able to get that in a minute. Clear. But like basically, we basically have like some core workflows, the podcast, the newsletter and the deep dive articles. Those constitute like the core of the content engine. And then we have sort of two types, broadly speaking, of social media content.

We have the spoke content that comes from those pillar pieces. And then we have social media that kind of just exists on its own. That's optimized for social media. And we're not optimized. I haven't been thinking so much about how to get the repurposing going in the other direction, but I, I, um, I, I'm starting to install a little bit more of that where when I'm doing the daily stuff, before drafting anything for the newsletter, I actually do the social posts first.

Because the skills that I have for social media, like for writing captions and LinkedIn templates and stuff like that, oftentimes those frameworks give pretty good suggestions for how to package the core packet, like the snippet. an idea that is that that we're going to seize on there um and so then it's like actually maybe the newsletter piece will be better if it at least has this sort of pre-processed social media post and just i think in general thinking kind of socials first will help us um up this up this side of our game um Let's see, where are we here?

I guess we could talk a little bit about those meta ads. Right now, I sent them to you in Notion, right? Okay. Man. I've been going for 14 minutes. It just keeps working. It did the compaction and now it's just still working. Auditing socials. This is... I'm a little worried. I'm getting worried about what it's doing.

When it boogies for this long... Okay. I kind of want to...

and 24,000 tokens. Like I'm not worried about the token usage, but it just, you know, It would be nice if it could get What's it looking for? Okay. Okay, both skills are now restored with their reference files. Let me update the project status. Oh my goodness. Hand off slack. I really wish I could find the original files This one's not bad. This one's still kind of old though. This is like an appendix of skills.

And yeah, this is all old stuff. I really liked the visualizations that we had I wanted to stop so that I can ask it about that. Um, But, oh, actually, you know what? One thing that I want to do is talk through the YouTube video scraper skill. I think it's called... I know it's getting close to the end here because it's just updating context documents and that's usually sort of the last thing. Okay, let's see.

This is the wrong folder. I'm going to get an OpenEd Vault. Skills. YouTube Clip extractor and this will probably be a familiar workflow for you because you you did this a while back and then as soon as you left it kind of fell by the wayside and Okay, so here's what this was just working on right now. I had previously, I had something called a hook and headline writer skill and it was, It was not very good.

It was... Let's see. Hook and headline. This is what it looked like. It was like... Okay. Hooks and headlines that stop the scroll and compel action. Key principles, three sentence rule for social hooks, maximum of three sentences. First sentence must be short. Like what? Where did this come from?

This came from it somehow.

It took a photocopy of a photocopy too many times and like didn't really have, you know, and like 25% ideation, 25% hook and headline. Well, that's not how LLMs think. They don't think in terms of like, I'm going to spend 25% of my time on this. And no, they think in terms of inputs and outputs.

And if you can define what a good output looks like, then you've written a good skill.

The instructions are almost secondary. Some good instructions can bolster an example and give it a better sense of how to navigate the input to output translation process. But almost all of my skills, if I've done my job well and formulated the skill well, it's going to use examples to do the heavy lifting.

And I think that the same also applies with the comic skill. You can describe like, this is what humor is. This is what's funny. But if you can actually give examples, it's going to go a lot farther. So I had, first I was like, it doesn't make sense for us to have hooks and headlines in the same skill.

So I said, let's break that out. And also it had newsletter subject lines in the same one. I said, no, let's break that out.

Let's make the newsletter subject lines its own skill.

So now we have a newsletter subject line. Here's the skill. And then it has the broad frameworks of different, you know, kind of core patterns. And then it has a few other references. This is a really long reference of, subject lines that I think I swiped from I'm not sure where I swiped these from, actually. Or maybe it swiped them. That's kind of interesting. But the references are really kind of demoted in importance because they're not going to get read unless it feels like it doesn't get enough information from the skill itself.

Um, But yeah, for newsletter subject line, Corfo, again, 80% of the performance, I guess that's not, it's not terrible to have it, but, and then saying generate 10 options, that's definitely, you know, that, that is important because with subject lines, it's super easy to just, you know, you might as well get 10. If not, honestly, like if not 50 and then have it pick the best 10 or something like that.

But, you know, it's super cheap in terms of tokens.

You wouldn't do that for like a long form article, but for the short, Thanks. It makes sense. But when I rewrote these sub skills, I was looking at them and I realized that it had stripped away a lot of the examples that I wanted. So this was just a restoration. They were too thin, lost valuable content. And in this case, article titles reference. Let's take a look at the new one now. Where is it? Article titles.

Here we go. Here's the skill. Um... And Let's see. There's 15 proven formulas in the formula library.

Honestly, I probably still want more stuff in the skill itself. Um... But we'll put that on hold. Maybe we'll say, in general with these skills, I want more of the core substance and more examples in the skill itself. And as a general note to add to the skill creator, I want you to put in my philosophy of examples over instructions.

And output examples are worth a thousand words of instructions. Um...

And then I can say, next, let's take a look at the YouTube clip.

What's it called? YouTube clip skill Let's see. YouTube Clip Extractor. I want to do an audit on that one and make sure that all of our tools are hooked up correctly. Um, We might merge YouTube Downloader or perhaps just keep it as a reference.

So basically, these two skills work together, YouTube Clip Extractor and YouTube Downloader.

Um... You're gonna like these. You're gonna like these, I think. Um... So the clip extractor We had previously had in a project in Clawed, Um, Use it when you have a YouTube URL and want to extract the best clips. Automated clip identification based on hook coda criteria. Required tools. YTDLP. So this is one that you might actually need to, the first time you run it, you might need to install YTDLP and FFmpeg.

These are two different tools. YTDLP is a scraping tool that...

downloads files from YouTube and other sources. An FFmpeg is a It's kind of like a whole encoding language for being able to like parse videos and stuff. I actually don't even know exactly what I have, like an intuitive grasp of what FFmpeg does, but it's hard to put that into words.

All right. So from it, from a YouTube video, this will be best if we can actually test it out.

Let's let's find some kind of YouTube video. I'm mostly looking for kind of like. Maybe prominent people, maybe kind of like vintage gems, things that like we're competing against this.

We're competing against Lululemon Pants and Bent Over, a highfalutin apartment. So we can't compete on that per se, but maybe we can compete on the caption with some interesting visual. So let's sort of think about...

I'm going to think of like, like Phil, I don't know, Phil Donahue homeschooling.

Phil Donahue was an old talk show host way back in the day.

Okay, here we go. John Holt and El Programa de Phil Donahue, Sober Homeschooling. And it appears to be in Spanish, but... I don't... Okay, this. Dang.

I'm guessing you can't hear it, right? Oh, but you could hear the audio? For a hot second, it kind of, yeah. But it was in English, right? The video is in English, but the captions are, yeah. So I wonder, I'm gonna see if I can find John Holt.

on Phil Donahue. This could be super interesting if we can find it.

OK, here we go, 58 minutes.

This looks good. Thank you very much. This is going to be great. This is going to be super interesting.

Because you know I was talking about like... One thing we could use to sort of stop the scroll. Everyone's sick of the AI slop. So like instead we kind of go the other direction, right? Um...

Yep. Yep. All right, let me check. Okay, it's doing a lot of work that I don't know that I necessarily... wanted it to do. Well, it's first it had to do the skill creator thing that had the philosophy and now it's going to need to compact context pretty soon again. I'm almost tempted to just start a new chat rather than wait for it to do the whole context thing Broken references, okay, interesting.

Yeah, see, that's the thing is when you start chaining skills together and then you like refactor them, then the references start to get a little bit screwy. So it becomes this whole, it's like refactoring a code base where like you're changing from one language to another andAI can do this now.

It has enough ability or enough wherewithal for that kind of a task. But let's actually start a new terminal here. Let's say Claude. Dangerously skip permissions. That's how I always have to start. when I'm working in the terminal. And... My computer is humming like it's... Gonna catch on fire or something. All right, here we go. So I'm just gonna paste the link in. and say, Hello? Let's run the YouTube Clip Extractor on this episode.

And it should, I think YTDLP, it should first...

Extract the captions.

because it can get the information that it needs without downloading the whole video first. But I think the last time we did this workflow, we were having to manually download the video and put it into script and then cut the clip, right? Now, We don't have to do that anymore. It can use FFmpeg to download the file and cut the clip that it needs.

The one thing that's super important that we should edit the skill to do if we haven't done it already is after we've got the clips imported into, oh, come on, what is this? Okay, it should be YTDLP command line to get information about this. Here we go. YTDLP print title, print description, duration, channel. This should figure it out here. I'm getting, I'm having some performance issues here. I'm going to try Closing out these apps that I'm not using.

Yes. Yes. And, um,
