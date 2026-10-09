#!/usr/bin/env python3
"""
Create a new blog post with template and folder structure
Usage: python new-post.py "Post Title" [--style image-first|observation-first|reflection]
"""

import os
import sys
import re
from datetime import datetime

# MkDocs builds the site from docs/; paths are relative to the repo root
DOCS_DIR = "docs"
POSTS_DIR = f"{DOCS_DIR}/posts"
IMAGES_DIR = f"{DOCS_DIR}/images"
SITE_INDEX = f"{DOCS_DIR}/index.md"

def slugify(title):
    """Convert title to URL-friendly slug"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def get_post_template(style, title, date_display, date_slug):
    """Get the template based on style"""

    templates = {
        'image-first': f"""# {title}

## {date_display}

Brief introduction or context (2-3 sentences).

![Alt text describing the image](../images/{date_slug}/filename.jpg)

Your reflection or observation here (1-3 paragraphs).

---
[← Back to all posts](../index.md)
""",
        'observation-first': f"""# {title}

## {date_display}

Your observation or what you found (2-3 sentences).

![Alt text describing the image](../images/{date_slug}/filename.jpg)

Connection or meaning (1-2 sentences).

---
[← Back to all posts](../index.md)
""",
        'reflection': f"""# {title}

## {date_display}

Your thoughts or reflection here.

Continue the reflection (keep it focused and concise).

---
[← Back to all posts](../index.md)
"""
    }

    return templates.get(style, templates['image-first'])

def update_post_list(list_path, post_link, title, date_obj):
    """Add a post link under '## Recent Posts' in a markdown file"""
    if not os.path.exists(list_path):
        print(f"Warning: {list_path} not found, skipping")
        return

    with open(list_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Format: - [Title](posts/YYYY-MM-DD-slug.md) - Month Day, Year
    date_display = date_obj.strftime("%B %d, %Y")
    new_entry = f"- [{title}]({post_link}) - {date_display}"

    # Find the "## Recent Posts" section
    if "## Recent Posts" in content:
        # Insert after the "## Recent Posts" line
        lines = content.split('\n')
        insert_index = None

        for i, line in enumerate(lines):
            if line.strip() == "## Recent Posts":
                # Insert after the next blank line
                insert_index = i + 2
                break

        if insert_index is not None:
            lines.insert(insert_index, new_entry)
            content = '\n'.join(lines)

            with open(list_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[+] Updated {list_path}")
    else:
        print(f"Warning: Could not find '## Recent Posts' section in {list_path}")

def yaml_quote(text):
    """Quote a nav title when plain YAML would misread it"""
    if re.search(r'[:#\[\]{},&*!|>\'"%@`]', text) or text[:1] in '-?' or text != text.strip():
        return '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return text

def update_nav(post_link, title, config_path="mkdocs.yml"):
    """Add the post at the top of the Walks section of the MkDocs nav"""
    if not os.path.exists(config_path):
        print(f"Warning: {config_path} not found, skipping nav update")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    for i, line in enumerate(lines):
        if line.strip() == "- Walks:":
            # Match the indentation of the existing entries
            indent = "      "
            if i + 1 < len(lines) and lines[i + 1].lstrip().startswith("- "):
                next_line = lines[i + 1]
                indent = next_line[:len(next_line) - len(next_line.lstrip())]
            lines.insert(i + 1, f"{indent}- {yaml_quote(title)}: {post_link}")

            with open(config_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            print(f"[+] Updated {config_path} nav")
            return

    print(f"Warning: Could not find '- Walks:' in {config_path} nav")

def create_post(title, style='image-first'):
    """Create a new post with all necessary files and folders"""

    # Get current date
    date_obj = datetime.now()
    date_str = date_obj.strftime("%Y-%m-%d")
    date_display = date_obj.strftime("%B %d, %Y")

    # Create slug
    slug = slugify(title)

    # Create file paths
    post_name = f"{date_str}-{slug}.md"
    post_filename = f"{POSTS_DIR}/{post_name}"
    images_folder = f"{IMAGES_DIR}/{date_str}"

    # Check if post already exists
    if os.path.exists(post_filename):
        print(f"Error: Post already exists: {post_filename}")
        return None

    # Create posts folder if it doesn't exist
    os.makedirs(POSTS_DIR, exist_ok=True)

    # Create images folder
    os.makedirs(images_folder, exist_ok=True)
    print(f"[+] Created folder: {images_folder}")

    # Get template content
    template = get_post_template(style, title, date_display, date_str)

    # Write post file
    with open(post_filename, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"[+] Created post: {post_filename}")

    # List the post on the site home page, the repo README and the site nav
    update_post_list(SITE_INDEX, f"posts/{post_name}", title, date_obj)
    update_post_list("README.md", post_filename, title, date_obj)
    update_nav(f"posts/{post_name}", title)

    return post_filename

def main():
    if len(sys.argv) < 2:
        print("Usage: python new-post.py \"Post Title\" [--style image-first|observation-first|reflection]")
        print("\nExamples:")
        print('  python new-post.py "First Snow"')
        print('  python new-post.py "Morning Light" --style observation-first')
        sys.exit(1)

    title = sys.argv[1]
    style = 'image-first'

    # Check for style argument
    if len(sys.argv) > 2 and sys.argv[2] == '--style' and len(sys.argv) > 3:
        style = sys.argv[3]
        if style not in ['image-first', 'observation-first', 'reflection']:
            print(f"Error: Invalid style '{style}'")
            print("Valid styles: image-first, observation-first, reflection")
            sys.exit(1)

    post_file = create_post(title, style)

    if post_file:
        print(f"\n[+] Post created successfully!")
        print(f"\nNext steps:")
        print(f"1. Add your images to: {IMAGES_DIR}/{datetime.now().strftime('%Y-%m-%d')}/")
        print(f"2. Edit your post: {post_file}")
        print(f"3. Run: python optimize_images.py")
        print(f"4. Preview with: mkdocs serve")
        print(f"5. Run: python publish.py \"{title}\"")

if __name__ == "__main__":
    main()
