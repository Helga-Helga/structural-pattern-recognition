from generate_string import generate_string
from draw_letters import create_letters_images
from draw_string import draw_string, get_noised_image
from create_graph import initialize_graph, fill_nodes, fill_edges, compose_labels
from Semiring.SemiringArgminPlusElement import SemiringArgminPlusElement


def dynamic_programming_solver(nodes, edges, semiring=SemiringArgminPlusElement):
    """
    Dynamic programming algorithm for finding the best path (with minimum weight)
    :param nodes: 3d array of node weights
    :param edges: 3d array of edge weights
    :param semiring: semiring class to use
    :return: 3d array of updated node weights
    """
    for obj in reversed(range(1, nodes.shape[0])):
        for label_l in range(nodes.shape[1]):
            min_value = semiring.get_zero()
            next_label = None
            for label_r in range(nodes.shape[2]):
                min_value, next_label = \
                    min_value.add(edges[obj-1, label_l, label_r].mul(nodes[obj, label_r, 0]), next_label, label_r)
            nodes[obj-1, label_l, 0] = nodes[obj-1, label_l, 0].mul(min_value)
            nodes[obj-1, label_l, 1] = next_label
    return nodes


def get_best_path(nodes, labels, semiring=SemiringArgminPlusElement):
    """
    Finds path with minimum weight
    :param nodes: 3d array of updated node weights after dynamic programming
    :param labels: list of tuples like (name_of_character, number_of_column_of_this_character)
    :param semiring: semiring class to use
    :return: best path presented as a list of consecutive labels and its weight
    """
    path = [0] * nodes.shape[0]
    min_value = semiring.get_zero()
    for label in range(nodes.shape[1]):
        if nodes[0, label, 0].value < min_value.value:
            min_value = nodes[0, label, 0]
            path[0] = label
    for obj in range(1, nodes.shape[0]):
        path[obj] = int(nodes[obj-1, path[obj-1], 1])
    return [labels[i] for i in path], nodes[0, path[0], 0]


def get_result_string(path):
    """
    Sequential labels like ('A', 0), ('A', 1), ..., ('A', width(A) - 1) are converted to 'A'
    :param path: list of consecutive labels labels
    :return: string of recognized letters
    """
    result_string = ""
    for node in path:
        if node[1] == 0:
            result_string += node[0]
    return result_string


if __name__ == "__main__":
    N = 10  # Number of symbols in string
    ALPHABET = ['A', 'B', 'C', ' ']  # Alphabet
    SIZE = 20  # Size of font
    MU = 0  # Mean for gaussian distribution
    SIGMA = 255 * 2  # Standard deviation for gaussian distribution

    # Generate string and create image of it
    string = generate_string(ALPHABET, N)
    characters = create_letters_images(ALPHABET, SIZE)
    image = draw_string(string, characters)
    print("Input string: '{}'".format(string))

    # Add noise to image
    image = get_noised_image(image, MU, SIGMA)
    image.show()

    list_characters = [c for c in characters.values()]
    image = image.convert("L")

    # Build graph
    labels = compose_labels(list_characters, ALPHABET)
    nodes, edges = initialize_graph(image.size[0], len(labels))
    nodes = fill_nodes(nodes, image, ALPHABET, list_characters, labels)
    edges = fill_edges(edges, ALPHABET, list_characters, labels)

    # Solve problem
    nodes = dynamic_programming_solver(nodes, edges)
    path, path_weight = get_best_path(nodes, labels)
    print("Result path: ", path)
    print("Path weight: ", path_weight)
    result = get_result_string(path)
    print("Recognized string: '{}'".format(result))
