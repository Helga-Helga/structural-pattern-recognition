from numpy import inf, zeros
from generate_string import generate_string
from draw_letters import create_letters_images
from draw_string import draw_string
from create_graph import initialize_graph, fill_nodes


def min_solver(nodes):
    """
    Find labeling taking argminimum value of node weight in each object.
    Edge weights are zero.
    :param nodes: 2d array of node weights
    :return: array of letter indexes
    """
    argmin_nodes = zeros(nodes.shape[0], dtype=int)
    for i in range(nodes.shape[0]):
        min_value = inf
        for k in range(nodes.shape[1]):
            if nodes[i, k] < min_value:
                min_value = nodes[i, k]
                argmin_nodes[i] = k
    return argmin_nodes


def dynamic_programming_solver(nodes, edges):
    """
    Find labeling using dynamic programming algorithm
    :param nodes: 2d array of node weights
    :param edges: 4d array of edge weights
    :return: array of letter indexes
    """
    argmin_nodes = zeros(nodes.shape[0], dtype=int)
    for i in range(nodes.shape[0]):
        for k in range(nodes.shape[1]):
            min_value = inf
            for k_ in range(nodes.shape[1]):
                if i == nodes.shape[0] - 1:
                    if nodes[i, k_] < min_value:
                        min_value = nodes[i, k_]
                        argmin_nodes[i] = k_
                    continue
                if edges[i, i+1, k_, k] + nodes[i, k_] < min_value:
                    min_value = edges[i, i+1, k_, k] + nodes[i, k_]
                    argmin_nodes[i] = k_
            nodes[i, k] += min_value
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
    n = 20
    labels = ['A', 'B', 'C', ' ']
    string = generate_string(labels, n)
    characters = create_letters_images(labels, 200)
    image = draw_string(string, characters)
    print("Input string:           {}".format(string))

    nodes, edges = initialize_graph(n, labels)
    list_characters = [c for c in characters.values()]
    image = image.convert("L")
    nodes = fill_nodes(nodes, image, list_characters)
    print("Recognized taking min:  {}".format(get_result_string(min_solver(nodes), labels)))

    print("Recognized dynamically: {}".format(get_result_string(dynamic_programming_solver(nodes, edges), labels)))
