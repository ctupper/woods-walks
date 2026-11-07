#!/usr/bin/env python3
"""
Image optimization script for woods-walks blog
Resizes new images to web-friendly dimensions and prints markdown snippets.

An image is optimized once: the untouched original is kept beside it as
`<name>.original` (gitignored), and any image that already has one is
skipped, so re-running never re-compresses a photo that's already been done.
"""

from PIL import Image, ImageOps
import os
import sys

IMAGES_DIR = "docs/images"
POSTS_DIR = "docs/posts"
MAX_WIDTH = 800
JPEG_QUALITY = 85

JPEG_EXTS = ('.jpg', '.jpeg')
PNG_EXTS = ('.png',)


def backup_path(image_path):
    return image_path + '.original'


def optimize_image(image_path, max_width=MAX_WIDTH, quality=JPEG_QUALITY):
    """
    Optimize an image for web use, keeping its format (JPEG stays JPEG,
    PNG stays PNG). Metadata such as EXIF/GPS is not carried over.

    Args:
        image_path: Path to the image file
        max_width: Maximum width in pixels
        quality: JPEG quality 1-100 (ignored for PNG)
    """
    is_png = image_path.lower().endswith(PNG_EXTS)
    original_size = os.path.getsize(image_path)

    # Read the whole image into memory and close the file, so the original
    # can be renamed to its backup (Windows won't rename an open file)
    with Image.open(image_path) as src:
        img = ImageOps.exif_transpose(src)  # apply phone rotation
        img.load()

    width, height = img.size
    print(f"\nOriginal image: {image_path}")
    print(f"  Dimensions: {width}x{height}px")
    print(f"  File size: {original_size / (1024*1024):.2f}MB")

    if width > max_width:
        new_height = int(height * max_width / width)
        print(f"\nResizing to: {max_width}x{new_height}px")
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    else:
        print(f"\nImage width ({width}px) is already <= {max_width}px, no resize needed")

    os.rename(image_path, backup_path(image_path))
    print(f"Original backed up to: {backup_path(image_path)}")

    try:
        if is_png:
            img.save(image_path, 'PNG', optimize=True)
        else:
            # JPEG has no transparency or palette; flatten anything else to RGB
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
    except Exception:
        # Put the original back so a failed run leaves the image as it was
        if os.path.exists(image_path):
            os.remove(image_path)
        os.rename(backup_path(image_path), image_path)
        raise

    new_size = os.path.getsize(image_path)
    reduction = ((original_size - new_size) / original_size) * 100

    print(f"\nOptimized image saved!")
    print(f"  New file size: {new_size / (1024*1024):.2f}MB")
    print(f"  Reduction: {reduction:.1f}%")

    return image_path


def find_new_images(images_dir):
    """Images that haven't been optimized yet (no .original backup)"""
    new_images, skipped = [], 0
    for root, dirs, files in os.walk(images_dir):
        for file in sorted(files):
            if not file.lower().endswith(JPEG_EXTS + PNG_EXTS):
                continue
            path = os.path.join(root, file)
            if os.path.exists(backup_path(path)):
                skipped += 1
            else:
                new_images.append(path)
    return new_images, skipped


def print_snippets(image_paths):
    print("\n" + "="*60)
    print("MARKDOWN SNIPPETS")
    print("="*60)
    print("\nCopy and paste these into your blog post:\n")

    for img_path in image_paths:
        # Alt text suggestion from the filename: shadow-in-snow -> Shadow In Snow
        name_without_ext = os.path.splitext(os.path.basename(img_path))[0]
        alt_suggestion = name_without_ext.replace('-', ' ').title()

        # Path relative to docs/posts/, with forward slashes even on Windows
        relative_path = os.path.relpath(img_path, POSTS_DIR).replace('\\', '/')

        print(f"![{alt_suggestion}]({relative_path})")
        print()


def main():
    if not os.path.exists(IMAGES_DIR):
        print(f"Error: {IMAGES_DIR} directory not found")
        sys.exit(1)

    image_files, skipped = find_new_images(IMAGES_DIR)

    if skipped:
        print(f"Skipping {skipped} image(s) already optimized (have a .original backup)")

    if not image_files:
        print("No new images to optimize")
        sys.exit(0)

    print(f"Found {len(image_files)} new image(s) to optimize:")
    for img in image_files:
        print(f"  - {img}")

    print("\n" + "="*60)

    optimized_images = []
    for image_path in image_files:
        try:
            optimized_images.append(optimize_image(image_path))
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
        print("="*60)

    print(f"\nOptimized {len(optimized_images)} of {len(image_files)} image(s).")

    if optimized_images:
        print_snippets(optimized_images)


if __name__ == "__main__":
    main()
