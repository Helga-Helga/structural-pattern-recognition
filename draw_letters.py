from PIL import Image, ImageDraw, ImageFont


def create_letters_images(characters, size):
    """
    Create images of characters (letters)
    :param characters: a list of letters that should be presented as images
    :param size: size of characters
    :return: generated images of given characters
    """
    font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf', size)
    images = {}
    for c in characters:
        width, height = font.getsize(c)
        c_width, c_height = font.getoffset(c)
        image = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.text((-c_width, -c_height), text=c, fill='black', font=font)

        # Crop image (remove areas with transparent background)
        bbox = image.convert("RGBa").getbbox()
        images[c] = image.crop(bbox)
        images[c] = images[c].convert("L")

    images = align_image_sizes(characters, images)
    return images


def align_image_sizes(characters, images):
    """
    Resize images so that they have the same sizes
    :param characters: a list of letters
    :param images: generated images with different sizes
    :return: resized images
    """
    width = max(images[c].size[0] for c in characters)
    height = max(images[c].size[1] for c in characters)
    for c in characters:
        image = images[c]
        images[c] = image.resize((width, height), Image.ANTIALIAS)

    return images


if __name__ == "__main__":
    characters = ['A', 'B', 'C']
    size = 200
    images = create_letters_images(characters, size)
    for c in characters:
        images[c].show()
