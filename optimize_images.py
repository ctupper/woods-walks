#!/usr/bin/env python3
"""
Image optimization script for woods-walks blog
Resizes images to web-friendly dimensions and optimizes quality
"""

from PIL import Image, ImageOps
import os
import sys

def optimize_image(image_path, max_width=800, quality=85):
    """
    Optimize an image for web use

    Args:
        image_path: Path to the image file
        max_width: Maximum width in pixels (default: 800)
        quality: JPEG quality 1-100 (default: 85)
    """
    # Open the image
    img = Image.open(image_path)

    # Apply EXIF orientation if present
    img = ImageOps.exif_transpose(img)

    # Get original dimensions
    original_size = os.path.getsize(image_path)
    width, height = img.size

    print(f"\nOriginal image: {image_path}")
    print(f"  Dimensions: {width}x{height}px")
    print(f"  File size: {original_size / (1024*1024):.2f}MB")

    # Calculate new dimensions if width exceeds max_width
    if width > max_width:
        ratio = max_width / width
        new_width = max_width
        new_height = int(height * ratio)

        print(f"\nResizing to: {new_width}x{new_height}px")
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    else:
        print(f"\nImage width ({width}px) is already <= {max_width}px, no resize needed")

    # Create backup of original
    backup_path = image_path + '.original'
    if not os.path.exists(backup_path):
        os.rename(image_path, backup_path)
        print(f"Original backed up to: {backup_path}")

    # Save optimized version
    img.save(image_path, 'JPEG', quality=quality, optimize=True)

    new_size = os.path.getsize(image_path)
    reduction = ((original_size - new_size) / original_size) * 100

    print(f"\nOptimized image saved!")
    print(f"  New file size: {new_size / (1024*1024):.2f}MB")
    print(f"  Reduction: {reduction:.1f}%")

    return image_path

if __name__ == "__main__":
    # Find all images in the images directory
    images_dir = "images"

    if not os.path.exists(images_dir):
        print(f"Error: {images_dir} directory not found")
        sys.exit(1)

    # Find all JPG/JPEG/PNG files
    image_files = []
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')) and not file.endswith('.original'):
                image_files.append(os.path.join(root, file))

    if not image_files:
        print("No images found to optimize")
        sys.exit(0)

    print(f"Found {len(image_files)} image(s) to optimize:")
    for img in image_files:
        print(f"  - {img}")

    print("\n" + "="*60)

    # Optimize each image and collect results
    optimized_images = []
    for image_path in image_files:
        try:
            result = optimize_image(image_path)
            if result:
                optimized_images.append(result)
            print("="*60)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    print("\nAll images optimized!")

    # Generate markdown snippets
    if optimized_images:
        print("\n" + "="*60)
        print("MARKDOWN SNIPPETS")
        print("="*60)
        print("\nCopy and paste these into your blog post:\n")

        for img_path in optimized_images:
            # Convert Windows path to forward slashes for markdown
            img_path = img_path.replace('\\', '/')
            # Get filename without extension for alt text suggestion
            filename = os.path.basename(img_path)
            name_without_ext = os.path.splitext(filename)[0]
            # Convert hyphens to spaces for better alt text
            alt_suggestion = name_without_ext.replace('-', ' ').title()

            # Generate relative path from posts/ directory
            relative_path = f"../{img_path}"

            print(f"![{alt_suggestion}]({relative_path})")
            print()
