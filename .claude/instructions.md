# Woods Walk Blog - Claude Code Instructions

## Project Overview

**Purpose:** Personal blog documenting morning walks in Maine woods through photography and brief reflections.

**Philosophy:** "Just enough" - finding what matters in simple moments. One day at a time.

**Audience:** Primarily for myself. If others find it and connect with it, great. Not optimizing for traffic or engagement metrics.

**Brand Identity:** 🌲💙
- 🌲 = Woods, connection to nature, Maine heritage, finding peace
- 💙 = Connection, showing up, steady presence

---

## Core Values & Principles

### Content Philosophy
- **Word efficiency:** Say what needs saying, no more. Cut through BS.
- **Simplicity over perfection:** Better to post something simple than wait for perfect
- **Authentic voice:** Direct, honest, conversational. No corporate speak.
- **Pattern recognition:** Connecting dots between observations, finding meaning in small details
- **Process over outcome:** The walk matters more than the photos. The journey over the destination.

### Technical Philosophy
- **Simple and maintainable:** I'm a programmer but this isn't a tech showcase
- **Hard to break:** Prefer boring, stable tech over cutting-edge
- **No analysis paralysis:** Make decisions, move forward, iterate
- **Version controlled:** Everything in git, clear history
- **Minimal dependencies:** Fewer things to break or maintain

---

## My Background (For Voice/Context)

- 57 years old, computer programmer in Maine
- Grew up in northern Maine (Perham), lumber jack family heritage
- Pattern recognition and systems thinking are core strengths
- Value autonomy, intellectual challenge, efficiency
- Introverted - the woods are restoration time
- Recovery mindset: one day at a time, forward-looking
- Direct communicator, no time for unnecessary complexity

### Why I Walk
- Connection to late father (woods = where I feel him around)
- Mental health and physical movement
- Finding "special moments" at macro and micro levels
- Escape from work chaos and life demands
- Just being myself without roles/responsibilities

---

## Content Structure

### Post Format
```markdown
# Post Title

*Date*

Brief introduction/context (2-3 sentences max)

![Alt text](../images/YYYY-MM-DD/filename.jpg)

Reflection or observation (1-3 paragraphs, keep it concise)

Optional second image if it adds to story

Closing thought (1-2 sentences)

---
[← Back](../README.md)
```

### File Organization
```
woods-walks/
├── README.md (homepage, recent posts list)
├── posts/
│   └── YYYY-MM-DD-title.md
├── images/
│   └── YYYY-MM-DD/
│       └── descriptive-name.jpg
└── .claude/
    └── instructions.md (this file)
```

### Naming Conventions
- **Posts:** `YYYY-MM-DD-short-descriptive-title.md`
- **Images:** `descriptive-name.jpg` (lowercase, hyphens, descriptive)
- **Image folders:** `YYYY-MM-DD/` (matches post date)

---

## Writing Style Guide

### Voice Characteristics
- **Conversational but not chatty:** Like talking to a friend over coffee
- **Observations over explanations:** Show, don't tell when possible
- **Concise:** Respect reader's time (and my own)
- **Honest:** Don't sugarcoat or perform positivity
- **Grounded:** Maine practical, not California mystical

### What to Avoid
- ❌ Bullet points (unless truly necessary for clarity)
- ❌ Excessive formatting (bold, italics, headers)
- ❌ Corporate speak or buzzwords
- ❌ Forced optimism or inspiration
- ❌ Over-explaining obvious things
- ❌ Apologizing for posting or not posting

### Themes That Resonate
- "Just enough" philosophy
- "One day at a time" approach  
- "Special moments don't come if you sit around and wait"
- "Sometimes you need to be in the moment and take it in"
- Pattern recognition, connecting dots
- Finding beauty in ordinary things (shadow in snow, ferns in winter)
- The hunt being as rewarding as the capture

---

## Photography Approach

### Style
- Phone camera (Samsung Galaxy S24FE) - "the phone makes things look really good"
- Not professional photographer, just capturing what catches my eye
- Mix of macro (landscapes, vistas) and micro (details, patterns)
- Intentional composition but not overthought
- Sometimes the best shot is the one people miss (like my shadow in the snow)

### Technical Requirements
- **Resize for web:** Max 1920px width, quality 80-85%
- **File size target:** 200KB-1MB per image
- **Format:** JPG for photos
- **Alt text:** Descriptive but brief

### When to Include Photos
- When image tells the story better than words
- When it captures a "special moment" worth sharing
- Not every post needs multiple images
- Quality over quantity

---

## Technical Stack

### Current Setup
- **Hosting:** GitHub (public repo)
- **Format:** Markdown files
- **Images:** Stored in repo (for now)
- **Version control:** Git + GitHub

### Future Consideration (Not Yet)
- **GitHub Pages + Jekyll:** When ready for proper blog look
- **Custom domain:** Maybe someday, not priority
- **Comments:** Probably never - not trying to build community
- **Analytics:** Don't care about metrics

### What I Need Help With
1. **Post creation workflow:** Scripts/templates to make new posts easy
2. **Image management:** Batch resizing, organizing, optimizing
3. **Markdown consistency:** Keeping format clean and consistent
4. **Jekyll setup:** When ready to upgrade from plain markdown
5. **Automation:** Anything that removes friction from posting

### What I Don't Need
- SEO optimization
- Social media integration  
- Complex features or plugins
- Performance optimization (unless actually slow)
- "Growth hacking" or engagement tricks

---

## Common Tasks & Workflows

### Creating New Post
```bash
# Ideal workflow (help me build this):
./new-post.sh "First Snow"
# Creates:
# - posts/2025-12-24-first-snow.md (from template)
# - images/2025-12-24/ (empty folder)
# - Opens editor with template filled in
```

### Adding Images
```bash
# Current: Manual upload to GitHub
# Desired: Script to resize and organize
./add-images.sh posts/2025-12-24-first-snow.md image1.jpg image2.jpg
# Resizes images, moves to correct folder, updates post with image markdown
```

### Publishing
```bash
# Current: git add, commit, push
# Keep it simple - this workflow is fine
git add .
git commit -m "Add post: First Snow"
git push
```

---

## Constraints & Preferences

### Time Constraints
- **Morning walks:** 1 hour, most days
- **Writing/posting:** Want this to take 10-15 minutes max
- **Maintenance:** Minimal time investment

### Technical Preferences
- **Languages I know:** Python, VBA, SQL, basic bash scripting
- **What I'm learning:** AI-assisted coding (Claude Code, Copilot)
- **Comfort zone:** Command line comfortable, prefer scripts to GUIs
- **Platform:** Windows primarily, some familiarity with git bash

### Decision-Making Style
- Present options clearly with pros/cons
- Prefer "good enough now" over "perfect later"
- Will try things and iterate
- Trust my gut, don't need excessive validation
- Appreciate directness over hand-holding

---

## Success Criteria

**This project succeeds if:**
- ✅ I actually post regularly (not letting friction stop me)
- ✅ Captures moments/thoughts that matter to me
- ✅ Easy to maintain (doesn't become a burden)
- ✅ Feels authentic (my voice, not performing for audience)
- ✅ Simple enough that I can manage it long-term

**This project fails if:**
- ❌ Becomes too complicated to maintain
- ❌ Feels like obligation rather than expression
- ❌ I start worrying about "audience" or "engagement"
- ❌ Technology gets in the way of content

---

## Important Context Notes

### Current Life Situation
- Work: Busy, sometimes chaotic, year-end crunch
- Family: Wife (Jo-Ann) dealing with health issues, adult kids nearby
- Financial: Working toward debt freedom, ~3-4 years out
- Mindset: One day at a time, managing what I can control

### Why This Matters
The walks are essential mental health time. The blog is:
- Documentation of the journey
- Practice in noticing/appreciating
- Something that's mine (not work, not family obligations)
- Low-stakes creative outlet

**Don't suggest things that add stress or complexity.** This should be restorative, not another thing to manage.

---

## Working With Me

### Communication Style
- **Direct and efficient:** Get to the point
- **Questions welcome:** I'll ask if I don't understand
- **Iteration friendly:** Try things, see what works, adjust
- **Context matters:** More context = better solutions

### When I Say "Simple"
I mean:
- Fewer moving parts
- Easy to understand/maintain
- Resistant to breaking
- Not impressive, just functional

### Red Flags to Avoid
- "This is the best practice..." (question: for whom?)
- "Everyone does it this way..." (don't care about everyone)
- "You should really..." (respect my choices)
- Over-engineering simple problems

---

## Example Post Styles

### Style 1: Image-First
```markdown
# Shadow in the Snow

*December 9, 2025*

First snow this week. Cold and frosty at sunrise.

![My shadow in the footprints](../images/2025-12-09/shadow-in-snow.jpg)

Most people miss their own shadow in the path. Sometimes you need to be in the moment and take it in.

---
[← Back](../README.md)
```

### Style 2: Observation-First
```markdown
# Green in Winter

*December 10, 2025*

Found ferns still bright green, tucked in a broken log. Everything else dormant, but these persist.

![Ferns in snow](../images/2025-12-10/ferns-winter.jpg)

Life finds a way even in the cold. Just enough.

---
[← Back](../README.md)
```

### Style 3: Reflection
```markdown
# The Hunt

*December 15, 2025*

The hunt is just as rewarding as capturing a special moment. Sometimes you see them, sometimes you need to find them.

Been thinking about that on these morning walks. The looking matters as much as the finding.

---
[← Back](../README.md)
```

---

## Version History & Evolution

### Current Phase: Getting Started
- Setting up basic repo structure
- Learning what works for posting rhythm
- Experimenting with style/voice
- Keeping it dead simple

### Future Possibilities
- Upgrade to Jekyll for better presentation
- Custom domain (maybe)
- More sophisticated image handling
- Hiking adventure posts (not just daily walks)

**Key:** Don't jump ahead. Let this evolve naturally. Simple first, expand only when actually needed.

---

## Final Notes

**Remember:** This is documentation of my journey, not a product launch. Success is showing up and capturing what matters, not building the perfect blog platform.

**Help me:**
- Remove friction from posting
- Maintain consistency without rigidity  
- Keep it simple and sustainable
- Honor my voice and values

**The goal isn't perfection. It's "just enough" to document the walk and the thoughts. That's it.**

🌲💙