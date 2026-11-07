# Woods Walks - Quick Reference

Simple workflow for creating and publishing blog posts.

## One-time Setup

```bash
pip install -r requirements.txt pillow
```

`requirements.txt` pins the MkDocs Material version the site is built with; Pillow is only needed locally for `optimize_images.py`.

## Full Workflow

```bash
# 1. Create new post
python new-post.py "Post Title"

# 2. Add your images to docs/images/YYYY-MM-DD/

# 3. Edit the post file (preview with: mkdocs serve)

# 4. Optimize images and get markdown snippets
python optimize_images.py

# 5. Copy/paste markdown snippets into your post

# 6. Publish
python publish.py "Post Title"
```

---

## Script Reference

### new-post.py - Create New Post

**Basic usage:**
```bash
python new-post.py "Post Title"
```

**With style template:**
```bash
python new-post.py "Morning Walk" --style observation-first
```

**Available styles:**
- `image-first` (default) - Photo then reflection
- `observation-first` - What you found, then photo
- `reflection` - Text-only thoughts

**What it does:**
- Creates `docs/posts/YYYY-MM-DD-slug.md`
- Creates `docs/images/YYYY-MM-DD/` folder
- Adds the post to "Recent Posts" in `docs/index.md` (site home page) and `README.md`
- Adds the post to the `mkdocs.yml` nav under Walks, at the top of its year's section (creating the year if needed)

---

### optimize_images.py - Optimize Images

**Usage:**
```bash
python optimize_images.py
```

**What it does:**
- Finds new images in `docs/images/` (JPG, JPEG, PNG). Images that already have a `.original` backup are skipped, so re-running never re-compresses a photo
- Resizes to max 800px width (JPEG quality 85; PNGs stay PNG and keep transparency)
- Handles EXIF rotation automatically
- Strips EXIF metadata, including GPS location
- Keeps the untouched original as `<name>.original` (not committed to git)
- Prints markdown snippets for the images it just optimized

**Output example:**
```
![Shadow In Snow](../images/2025-12-07/shadow-in-snow.jpg)
```

---

### publish.py - Git Publish

**Basic usage:**
```bash
python publish.py "Post Title"
```

**With custom commit message:**
```bash
python publish.py "Morning Walk" --message "Update post with new images"
```

**What it does:**
- Shows git status
- Stages all changes (`git add .`)
- Commits with message: `Add post: {title}`
- Pushes to GitHub; on `main`, the publish-docs workflow rebuilds the site with `mkdocs gh-deploy`
- Titles and messages can contain quotes or any other characters

**Site check:** the "Check site" workflow runs `mkdocs build --strict` on every push to `main` and every pull request. It fails on broken internal links, links to headings that don't exist, and nav entries pointing at missing files. It doesn't block the publish, so a red X means fix the link, not that the post is missing. Run the same check locally with `mkdocs build --strict`.

---

## Quick Tips

**Create post with specific style:**
```bash
python new-post.py "Frozen Brook" --style reflection
```

**Publish with custom message:**
```bash
python publish.py "Update" --message "Fix typo in First Snow post"
```

**Just optimize without creating new post:**
```bash
# Drop images in existing YYYY-MM-DD folder
python optimize_images.py
# Copy markdown snippets into post
```

---

## File Structure

```
woods-walks/
├── README.md              # GitHub landing page with recent posts
├── mkdocs.yml             # Site config and nav (Walks lists posts by year)
├── requirements.txt       # Pinned MkDocs Material version (used by both workflows)
├── hooks/lists.py         # Build-time fix: lists right under a line of text render as lists
├── docs/                  # Everything MkDocs publishes
│   ├── index.md           # Site home page with recent posts
│   ├── posts/
│   │   └── YYYY-MM-DD-title.md
│   └── images/
│       └── YYYY-MM-DD/
│           └── image-name.jpg
├── CLAUDE.md              # Project context Claude Code loads automatically
└── CLAUDE.local.md        # Private personal context (gitignored, you create it)
```

---

## Common Scenarios

### Scenario 1: New post with photos
```bash
python new-post.py "Morning Frost"
# Add images to docs/images/2025-12-24/
# Edit docs/posts/2025-12-24-morning-frost.md
python optimize_images.py
# Copy markdown snippets into post
python publish.py "Morning Frost"
```

### Scenario 2: Update existing post
```bash
# Edit the post file
python publish.py "Update" --message "Fix typo in Morning Frost"
```

### Scenario 3: Add more images to existing post
```bash
# Add new images to docs/images/2025-12-24/
python optimize_images.py
# Copy new markdown snippets into post
python publish.py "Morning Frost" --message "Add more photos"
```

---

## Troubleshooting

**Post already exists:**
- Script won't overwrite. Delete the post file first or use a different title.

**Image orientation wrong:**
- Script handles EXIF rotation automatically. If still wrong, report as bug.

**Git push fails:**
- Check you're connected to internet
- Verify git credentials are set up

**Markdown snippets not showing:**
- Script only generates snippets for newly optimized images
- Images with `.original` backup are skipped

**Re-optimize an image (e.g. after changing the size):**
- Delete the optimized image, rename `name.jpg.original` back to `name.jpg`, run the script again

**Image disappeared after an error:**
- It shouldn't: if saving fails, the script puts the original back. Check for a leftover `.original` file and rename it back

**"Check site" workflow failed:**
- Run `mkdocs build --strict` locally; the WARNING line names the file and the broken link
