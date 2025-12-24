#!/usr/bin/env python3
"""
Publish blog post to GitHub
Usage: python publish.py "Post Title" [--message "Custom commit message"]
"""

import os
import sys
import subprocess
import re
from datetime import datetime

def slugify(title):
    """Convert title to URL-friendly slug"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def run_command(cmd, description):
    """Run a shell command and return output"""
    print(f"[+] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def git_status():
    """Check git status"""
    result = subprocess.run("git status --short", shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def publish_post(title, custom_message=None):
    """Publish a post to GitHub"""

    # Check if we're in a git repo
    if not os.path.exists(".git"):
        print("Error: Not in a git repository")
        return False

    # Get current date
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Create slug
    slug = slugify(title)

    # Expected post filename
    post_file = f"posts/{date_str}-{slug}.md"

    # Check if post exists
    if not os.path.exists(post_file):
        print(f"Warning: Post file not found: {post_file}")
        print("Continuing with all changes...")

    # Show current status
    status = git_status()
    if not status:
        print("No changes to commit")
        return True

    print("\nCurrent changes:")
    print(status)
    print()

    # Stage all changes
    if not run_command("git add .", "Staging all changes"):
        return False

    # Create commit message
    if custom_message:
        commit_msg = custom_message
    else:
        commit_msg = f"Add post: {title}"

    # Commit
    commit_cmd = f'git commit -m "{commit_msg}"'
    if not run_command(commit_cmd, f"Committing: {commit_msg}"):
        return False

    # Push
    if not run_command("git push", "Pushing to GitHub"):
        return False

    print("\n[+] Successfully published!")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python publish.py \"Post Title\" [--message \"Custom commit message\"]")
        print("\nExamples:")
        print('  python publish.py "First Snow"')
        print('  python publish.py "Morning Walk" --message "Update post with new images"')
        sys.exit(1)

    title = sys.argv[1]
    custom_message = None

    # Check for custom message
    if len(sys.argv) > 2 and sys.argv[2] == '--message' and len(sys.argv) > 3:
        custom_message = sys.argv[3]

    if publish_post(title, custom_message):
        print("\nDone! Your post is live on GitHub.")
    else:
        print("\nPublish failed. Check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
