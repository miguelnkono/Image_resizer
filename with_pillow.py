from PIL import Image
import argparse
import os
import sys


def img_resizer(path: str) -> Image.Image:

    image = Image.open(path)
    width, height = image.size

    new_width = 300
    new_height = int(height * (new_width / width))

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    return resized_image


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="small utility to help resize images in a specific folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--folder", "-f", help="specify the folder containing the images to resize"
    )
    parser.add_argument(
        "--resized_imgs", "-r", help="specify the folder to store the resized images"
    )
    args = parser.parse_args()

    if not args.folder and not args.resized_imgs:
        print("❌ Error: Folder containing the images is required!")
        print("❌ Error: Folder to store the resized images is required!")
        print("   Use --folder /path/to/images or --interactive mode")
        print("   Use --name base_name or --interactive mode")
        sys.exit(-1)

    # img_dir = os.path.join(os.path.abspath(os.path.curdir), "imgs")
    img_dir = args.folder
    image_paths = [os.path.join(img_dir, img) for img in os.listdir(img_dir)]

    # resized_path = os.path.join(img_dir, "resized_imgs")
    resized_path = args.resized_imgs
    if os.path.exists(resized_path) == False:
        os.mkdir(resized_path)

    for path in image_paths:
        if os.path.isdir(path) is not True:
            resized_image = img_resizer(path=path)

            img_new_name = (
                resized_path + "/" + path.split("/")[-1].split(".")[0] + "_resized.png"
            )

            if os.path.exists(img_new_name) is not True:
                resized_image.save(img_new_name)
