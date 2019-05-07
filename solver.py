from numpy import inf, zeros
from generate_string import generate_string
from draw_letters import create_letters_images
from draw_string import draw_string, get_noised_image
from create_graph import initialize_graph, fill_nodes


def min_solver(nodes):
    """
    Find labeling taking argminimum value of node weight in each object.
    Edge weights are zero.
    :param nodes: 2d array of node weights
    :return: array of letter indexes
    """
    argmin_nodes = zeros(nodes.shape[0], dtype=int)
    for obj in range(nodes.shape[0]):
        min_value = inf
        for label in range(nodes.shape[1]):
            if nodes[obj, label] < min_value:
                min_value = nodes[obj, label]
                argmin_nodes[obj] = label
    return argmin_nodes


def dynamic_programming_solver(nodes, edges):
    """
    Find labeling using dynamic programming algorithm
    :param nodes: 2d array of node weights
    :param edges: 4d array of edge weights
    :return: array of letter indexes
    """
    argmin_nodes = zeros(nodes.shape[0], dtype=int)
    for obj in range(1, nodes.shape[0]):
        for label in range(nodes.shape[1]):
            min_value = inf
            for nbr_label in range(nodes.shape[1]):
                if edges[obj-1, obj, nbr_label, label] + nodes[obj-1, nbr_label] < min_value:
                    min_value = edges[obj-1, obj, nbr_label, label] + nodes[obj-1, nbr_label]
                    argmin_nodes[obj-1] = nbr_label
            nodes[obj, label] += min_value

    # Find label for the last object (letter)
    min_value = inf
    for label in range(nodes.shape[1]):
        if nodes[nodes.shape[0]-1, label] < min_value:
            min_value = nodes[nodes.shape[0]-1, label]
            argmin_nodes[obj] = label
    return argmin_nodes


def get_result_string(argmin_nodes, labels):
    """
    Get string for found labeling
    :param argmin_nodes: array of letter indexes
    :param labels: array of letters
    :return:
    """
    result_string = ''
    for i in argmin_nodes:
        result_string += labels[i]
    return ''.join(result_string)


if __name__ == "__main__":
    N = 10  # Number of symbols in string
    LABELS = ['A', 'B', 'C', ' ']  # Alphabet
    SIZE = 50  # Size of font
    MU = 0  # Mean for gaussian distribution
    SIGMA = 255 * 2  # Standard deviation for gaussian distribution

    # Generate string and create image of it
    string = generate_string(LABELS, N)
    characters = create_letters_images(LABELS, SIZE)
    image = draw_string(string, characters)
    print("Input string:           {}".format(string))

    # Add noise to image
    image = get_noised_image(image, MU, SIGMA)
    image.show()

    # Build graph
    nodes, edges = initialize_graph(N, LABELS)
    list_characters = [c for c in characters.values()]
    image = image.convert("L")
    nodes = fill_nodes(nodes, image, list_characters)

    # Solve problem
    result_min = min_solver(nodes)
    print("Recognized taking min:  {}".format(get_result_string(result_min, LABELS)))

    result_dynamic = dynamic_programming_solver(nodes, edges)
    print("Recognized dynamically: {}".format(get_result_string(result_dynamic, LABELS)))
