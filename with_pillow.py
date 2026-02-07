from PIL import Image

if __name__ == "__main__":
    image = Image.open("bear.png")
    width, height = image.size
    
    new_width = 300
    new_height = int(height * (new_width / width))

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    resized_image.show(title="resized image")

