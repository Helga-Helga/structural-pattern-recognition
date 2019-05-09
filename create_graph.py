from numpy import array, full, inf
from generate_string import generate_string
from draw_string import draw_string
from draw_string import create_letters_images


def initialize_graph(n, k):
    """
    Initialize nodes and weights of graph with infinite values
    Node: nodes[obj, obj_label, next_best_label]
    next_best_label is filled during dynamic programming
    Edge: edges[obj_l, obj_r, label_l, label_r], where obj_r - obj_l = 1
    :param n: number of objects
    :param k: number of labels in each object
    :return: 3d array of nodes and 4d array of edges with infinite weights
    """
    nodes = full((n, k, k), inf)
    edges = full((n, n, k, k), inf)
    return nodes, edges


def compose_labels(character_images, alphabet):
    """
    Each column of each letter image has its own label
    Example of label: ('A', 0) -- first column of image of letter 'A'
    :param character_images: list of images of characters (letters)
    :param alphabet: names of characters
    :return: list of tuples (name_of_character, number_of_column_of_this_character)
    """
    labels = []
    for letter_index in range(len(character_images)):
        for column in range(character_images[letter_index].size[0]):
            labels.append((alphabet[letter_index], column))
    return labels


def fill_edges(edges, alphabet, character_images, labels):
    """
    Defines allowable edges with zero weights
    :param edges: 4d array of edge weights
    :param alphabet: list of character names
    :param character_images: list of images of characters
    :param labels: list of tuples like (name_of_character, number_of_column_of_this_character)
    :return: 4d array of edge weights with zero weights for allowable ones
    """
    for obj in range(edges.shape[0] - 1):
        for label_l in range(edges.shape[2]):
            for label_r in range(edges.shape[3]):
                letter_index = alphabet.index(labels[label_l][0])
                width = character_images[letter_index].size[0]
                # ('A', 1) -> ('A', 2)
                if labels[label_r][1] - labels[label_l][1] == 1 and labels[label_l][0] == labels[label_r][0]:
                    edges[obj, obj + 1, label_l, label_r] = 0
                # ('A', width('A') - 1) -> ('B', 0)
                if labels[label_l][1] == width - 1 and labels[label_r][1] == 0:
                    edges[obj, obj + 1, label_l, label_r] = 0
    return edges


def fill_nodes(nodes, image, alphabet, character_images, labels):
    """
    Defines allowable nodes and computes their weights
    Weight of node ('A', 0) in first object is sum over pixels in image column of square differences
    between pixel in first column of image and firt column of image of letter 'A"
    :param nodes: 3d array of node weights
    :param image: noised image of string of characters
    :param alphabet: list of character names
    :param character_images: list of images of characters
    :param labels: list of tuples like (name_of_character, number_of_column_of_this_character)
    :return: 3d array of node weights
    """
    image = array(image, dtype=float)
    list_character_images = convert_images_to_arrays(character_images)
    for obj in range(nodes.shape[0]):
        for label in range(nodes.shape[1]):
            # First (zero) object can't have non-first label of any letter
            if obj == 0 and labels[label][1] != 0:
                continue
            letter_index = alphabet.index(labels[label][0])
            character_image = list_character_images[letter_index]
            # Last object can't have non-last label of any letter
            if obj == nodes.shape[0] - 1 and labels[label][1] != character_image.shape[1] - 1:
                continue
            weight = 0.
            for h_pixel in range(character_image.shape[0]):
                weight += (image[h_pixel, obj] - character_image[h_pixel, labels[label][1]]) ** 2
            nodes[obj, label, 0] = weight
            nodes[obj, label, 1] = None
    return nodes


def convert_images_to_arrays(character_images):
    """
    Convert images in list into 2d arrays
    :param character_images: list of images of characters
    :return: list of 2d arrays
    """
    list_array = []
    for image in character_images:
        list_array.append(array(image, dtype=float))
    return list_array


if __name__ == "__main__":
    n = 10
    alphabet = ['A', 'B', 'C']
    string = generate_string(alphabet, n)
    characters = create_letters_images(alphabet, 20)
    image = draw_string(string, characters)
    print(string)

    list_characters = [c for c in characters.values()]
    image = image.convert("L")

    print(image.size)
    labels = compose_labels(list_characters, alphabet)
    nodes, edges = initialize_graph(image.size[0], len(labels))
    nodes = fill_nodes(nodes, image, alphabet, list_characters, labels)
    edges = fill_edges(edges, alphabet, list_characters, labels)

    print(nodes[0, 0, 0])  # should be not inf
    print(nodes[0, 1, 0])  # should be inf
    print(edges[0, 1, 0, 1])  # should be zero
    print(edges[0, 1, 0, 0])  # should be inf
