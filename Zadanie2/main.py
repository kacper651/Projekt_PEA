from sys import maxsize
from ulits import load_matrix, get_file_lines, save_data, print_matrix
import time
from itertools import combinations as get_combinations
from math import inf

graph1 = [[0, 49, 34, 96, 74],
          [49, 0, 10, 94, 43],
          [34, 10, 0, 21, 6],
          [96, 94, 21, 0, 70],
          [74, 43, 6, 70, 0]]


def held_karp(graph):
    start = time.time()
    size = len(graph)
    archive = dict()

    for i in range(1, size):
        archive[(tuple([i]), i)] = graph[0][i]

    for subset_size in range(2, size):
        subsets = list(get_combinations(range(1, size), subset_size))
        for subset in subsets:
            for vertex in subset:
                min_val = inf
                for key in archive.keys():
                    key_subset, dest = key
                    smaller_subset = list(subset)
                    smaller_subset.remove(vertex)
                    smaller_subset = tuple(smaller_subset)
                    if key_subset == smaller_subset:
                        if archive[(smaller_subset, dest)] + graph[dest][vertex] < min_val:
                            min_val = archive[(smaller_subset, dest)] + graph[dest][vertex]

                archive[(subset, vertex)] = min_val

    end = time.time() - start
    print(archive)
    # return min_path_cost, min_path, end


if __name__ == "__main__":
    # config_lines = get_file_lines("config.ini")
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
    held_karp(graph1, )
