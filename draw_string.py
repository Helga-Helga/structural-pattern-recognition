from PIL import Image
from numpy import array, random
from draw_letters import create_letters_images


def draw_string(string, characters):
    """
    Creates an image of given string
    :param string: string to be drawn
    :param characters: images of letters that are presented in string
    :return: image of string
    """
    images = [characters[c] for c in string]

    width = sum(character.size[0] for character in images)
    height = max(character.size[1] for character in images)

    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    horizontal_offset = 0
    for character in images:
        image.paste(character, (horizontal_offset, 0))
        horizontal_offset += character.size[0]
    return image


def get_noised_image(image, mu=0, sigma=0):
    """
    Adds gaussian noise to the image
    :param image: image of character sequence
    :param mu: mean of the distribution
    :param sigma: standard deviation of the distribution
    :return: noised image
    """
    noise = random.normal(mu, sigma, size=(image.size[1], image.size[0]))
    image_array = array(image.convert("L"), dtype="float64")
    image_array += noise
    return Image.fromarray(image_array.clip(0, 255).astype("uint8"), mode="L")


if __name__ == "__main__":
    letters = ['A', 'B', 'C']
    size = 200
    characters = create_letters_images(letters, size)
    string = "ABCCAABBB"
    image = draw_string(string, characters)
    print("Image size: {}".format(image.size))
    image.show()

    image = get_noised_image(image, 0, 255 * 2)
    image.show()
