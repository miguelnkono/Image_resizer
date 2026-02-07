import math
import os
import sys
import argparse
from pathlib import Path
from PIL import Image


def img_resizer(path: str) -> Image.Image:
    """
    Resize an image based on its aspect ratio.

    Args:
        path: Path to the image file

    Returns:
        Resized PIL Image object
    """
    try:
        image = Image.open(path)
        width, height = image.size

        new_width = 300
        new_height = int(height * (new_width / width))

        # Use LANCZOS for high-quality downsampling
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return resized_image
    except Exception as e:
        print(f"❌ Error processing {path}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Small utility to help resize images in a specific folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--folder",
        "-f",
        required=True,
        help="Specify the folder containing the images to resize",
    )
    parser.add_argument(
        "--resized_imgs",
        "-r",
        required=True,
        help="Specify the folder to store the resized images",
    )

    args = parser.parse_args()

    # Validate input folder
    img_dir = Path(args.folder)
    if not img_dir.exists():
        print(f"❌ Error: Input folder '{args.folder}' does not exist!")
        sys.exit(1)

    if not img_dir.is_dir():
        print(f"❌ Error: '{args.folder}' is not a directory!")
        sys.exit(1)

    # Create output folder if it doesn't exist
    resized_path = Path(args.resized_imgs)
    resized_path.mkdir(parents=True, exist_ok=True)

    # Supported image extensions
    supported_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}

    # Get all image files
    image_paths = [
        f
        for f in img_dir.iterdir()
        if f.is_file() and f.suffix.lower() in supported_extensions
    ]

    if not image_paths:
        print(f"⚠️  Warning: No supported image files found in '{args.folder}'")
        print(f"   Supported formats: {', '.join(supported_extensions)}")
        sys.exit(0)

    print(f"📁 Found {len(image_paths)} image(s) to process...")

    # Process each image
    processed = 0
    skipped = 0

    for img_path in image_paths:
        # Generate output filename
        output_name = f"{img_path.stem}_resized{img_path.suffix}"
        output_path = resized_path / output_name

        # Skip if already exists
        if output_path.exists():
            print(f"⏭️  Skipping {img_path.name} (already exists)")
            skipped += 1
            continue

        # Resize image
        print(f"🔄 Processing {img_path.name}...", end=" ")
        resized_image = img_resizer(str(img_path))

        if resized_image:
            # Save with original format or PNG
            try:
                resized_image.save(output_path)
                print(f"✅ Saved to {output_name}")
                processed += 1
            except Exception as e:
                print(f"❌ Failed to save: {e}")
        else:
            print("❌ Failed")

    # Summary
    print("\n" + "=" * 50)
    print(f"✨ Processing complete!")
    print(f"   Processed: {processed}")
    print(f"   Skipped: {skipped}")
    print(f"   Output folder: {resized_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
