from PIL import Image
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


if __name__ == "__main__":
    letters = ['A', 'B', 'C']
    size = 200
    characters = create_letters_images(letters, size)
    string = "ABCCAABBB"
    image = draw_string(string, characters)
    print("Image size: {}".format(image.size))
    image.show()
