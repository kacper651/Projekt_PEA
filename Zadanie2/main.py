from ulits import load_matrix, get_file_lines, save_data, print_matrix
import time
from itertools import combinations as get_combinations
from math import inf
import tsplib95

graph1 = [[-1, 81, 50, 18, 75, 39, 107, 77, 87, 43],  # testowy graf, żeby zobaczyć czy metody działają innit bruv
          [81, -1, 76, 21, 37, 26, 34, 58, 66, 15],
          [50, 76, -1, 24, 14, 58, 100, 68, 33, 30],
          [18, 21, 24, -1, 19, 58, 68, 62, 84, 81],
          [75, 37, 14, 19, -1, 31, 60, 65, 29, 91],
          [39, 26, 58, 58, 31, -1, 64, 21, 42, 46],
          [107, 34, 100, 68, 60, 64, -1, 15, 55, 16],
          [77, 58, 68, 62, 65, 21, 15, -1, 17, 34],
          [87, 66, 33, 84, 29, 42, 55, 17, -1, 68],
          [43, 15, 30, 81, 91, 46, 16, 34, 68, -1]]


def load_tsp(path):
    problem = tsplib95.load(path)
    size = range(len(list(problem.get_nodes())))
    matrix = [[] for _ in size]
    for i in size:
        for j in size:
            matrix[i].append(problem.get_weight(i, j))

    return matrix


def held_karp(graph):
    start = time.time()
    size = len(graph)
    archive = [None]
    for subset_size in range(1, size):
        archive.append(dict())

    for i in range(1, size):
        archive[1][(tuple([i]), i)] = graph[0][i]

    for subset_size in range(2, size):
        subsets = list(get_combinations(range(1, size), subset_size))
        for subset in subsets:
            for vertex in subset:
                min_val = inf
                for key in archive[subset_size - 1].keys():
                    key_subset, dest = key
                    smaller_subset = list(subset)
                    smaller_subset.remove(vertex)
                    smaller_subset = tuple(smaller_subset)
                    if key_subset == smaller_subset:
                        current_val = archive[subset_size - 1][(smaller_subset, dest)] + graph[dest][vertex]
                        if current_val < min_val:
                            min_val = current_val

                archive[subset_size][(subset, vertex)] = min_val

    end = time.time() - start
    # for subset_size in archive:
    #     print(subset_size)

    min_val = inf
    for key in archive[size - 1].keys():
        key_subset, dest = key
        current_val = archive[size - 1][key] + graph[dest][0]
        if current_val < min_val:
            min_val = current_val

    print(min_val)

    return min_val, end


if __name__ == "__main__":
    config_lines = get_file_lines("config.ini")
    #
    # adj_matrix, size = load_matrix(config_lines[1])
    # times = []
    #
    # for _ in range(int(config_lines[5])):
    #     min_path_cost, min_path, tsp_time = held_karp(adj_matrix, size)
    #     times.append(tsp_time)
    #
    # for tsp_time in times:
    #     save_data(min_path, tsp_time)
    #
    # print_matrix(adj_matrix)
    # print(min_path_cost)
    # print(min_path)
    # print(tsp_time)
    print(held_karp(load_tsp(config_lines[1])))
    print(load_tsp(config_lines[1]))
