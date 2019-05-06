from numpy import zeros, array
from generate_string import generate_string
from draw_string import draw_string
from draw_string import create_letters_images


def initialize_graph(n, labels):
    """
    Creates an empty array of nodes and edges.
    To get a node (t, k) weight use nodes[t, k], where t is a character number and k is a label (character name).
    To get an edge (t, k, t_, k_) weight use edges[t, t_, k, k_], where (t, k) and (t_, k_) are nodes.
    :param n: number of characters (letters) in string
    :param k: number of possible characters (alphabet size)
    :return: zero weights of nodes and edges
    """
    k = len(labels)
    nodes = zeros((n, k))
    edges = zeros((n, n, k, k))
    return nodes, edges


def find_subimage_start_index(character_number, character_width):
    """
    Returns start index of subimage (image of some character).
    First image column has index 0.
    :param character_number: letter number in image
    :param character_width: letter width (all letters has the same width)
    :return: start position in string image of character of given number
    """
    if character_number == 0:
        return 0
    return character_number * character_width


def node_weight(string_image, character_image, character_number):
    """
    Calculates weight of one node.
    There is one node for one letter in image.
    Node weight is a sum over all pixels of squared difference between letter in string image and reference letter image
    :param string_image: image of string (sequence of letters, may be noised)
    :param character_image: image of one character without noise
    :param character_number: number of pending character in string image
    :return: weight of node
    """
    string_image = array(string_image, dtype=float)
    character_image = array(character_image, dtype=float)
    x_start = find_subimage_start_index(character_number, character_image.shape[1])
    weight = 0.
    for row in range(character_image.shape[0]):
        for column in range(character_image.shape[1]):
            weight += (string_image[row, column + x_start] - character_image[row, column]) ** 2
    return weight


def fill_nodes(nodes, string_image, characters):
    """
    Calculates weights of nodes.
    :param nodes: array of array of all possible labels for each object
    :param string_image: image of string (sequence of letters, may be noised)
    :param characters: list of letter images
    :return: calculated weights of all nodes
    """
    for i in range(nodes.shape[0]):
        for k in range(nodes.shape[1]):
            nodes[i, k] = node_weight(string_image, characters[k], i)
    return nodes


if __name__ == "__main__":
    n = 10
    labels = ['A', 'B', 'C']
    string = generate_string(labels, n)
    characters = create_letters_images(labels, 200)
    image = draw_string(string, characters)
    print(string)

    nodes, edges = initialize_graph(n, labels)
    list_characters = [c for c in characters.values()]

    image = image.convert("L")

    nodes = fill_nodes(nodes, image, list_characters)
    print(nodes)
