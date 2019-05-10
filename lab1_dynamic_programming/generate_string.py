from numpy.random import choice


def generate_string(characters, length):
    """
    Generates a random string of given characters of given length
    :param characters: a list of possible letters that can be present in string
    :param length: number of characters in string
    :return: generated random string
    """
    return ''.join(choice(characters, length))


if __name__ == "__main__":
    characters = ['A', 'B', 'C']
    length = 10
    print(generate_string(characters, length))
