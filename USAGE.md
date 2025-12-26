# Woods Walks - Quick Reference

Simple workflow for creating and publishing blog posts.

## Full Workflow

```bash
# 1. Create new post
python new-post.py "Post Title"

# 2. Add your images to images/YYYY-MM-DD/

# 3. Edit the post file

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
- Creates `posts/YYYY-MM-DD-slug.md`
- Creates `images/YYYY-MM-DD/` folder
- Updates README.md with new post link

---

### optimize_images.py - Optimize Images

**Usage:**
```bash
python optimize_images.py
```

**What it does:**
- Finds all images in `images/` folder
- Resizes to max 1600px width
- Handles EXIF rotation automatically
- Creates `.original` backups
- Generates markdown snippets to copy/paste

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
- Pushes to GitHub

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
├── README.md              # Homepage with recent posts
├── posts/
│   └── YYYY-MM-DD-title.md
├── images/
│   └── YYYY-MM-DD/
│       └── image-name.jpg
└── .claude/
    └── instructions.md    # Full project context
```

---

## Common Scenarios

### Scenario 1: New post with photos
```bash
python new-post.py "Morning Frost"
# Add images to images/2025-12-24/
# Edit posts/2025-12-24-morning-frost.md
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
# Add new images to images/2025-12-24/
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
