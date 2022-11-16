from ulits import load_matrix, load_tsp, get_file_lines, save_data, print_matrix
import time
from itertools import combinations as get_combinations
from math import inf


def held_karp(graph):
    size = len(graph)
    archive = [None]
    prev = [None]
    start = time.time()
    for subset_size in range(1, size):
        archive.append(dict())
        prev.append(dict())

    for i in range(1, size):
        archive[1][(tuple([i]), i)] = graph[0][i]
        prev[1][tuple([i]), i] = i

    for subset_size in range(2, size):
        subsets = list(get_combinations(range(1, size), subset_size))
        for subset in subsets:
            for vertex in subset:
                min_val = inf
                min_prev = None
                for key in archive[subset_size - 1].keys():
                    key_subset, dest = key
                    smaller_subset = list(subset)
                    smaller_subset.remove(vertex)
                    smaller_subset = tuple(smaller_subset)
                    if key_subset == smaller_subset:
                        current_val = archive[subset_size - 1][(smaller_subset, dest)] + graph[dest][vertex]
                        if current_val < min_val:
                            min_val = current_val
                            min_prev = dest

                archive[subset_size][(subset, vertex)] = min_val
                prev[subset_size][subset, vertex] = min_prev

    min_val = inf
    pre = None
    min_path = []
    for key in archive[size - 1].keys():
        key_subset, dest = key
        current_val = archive[size - 1][key] + graph[dest][0]
        if current_val < min_val:
            min_val = current_val
            pre = key

    for key in prev[size - 1].keys():
        key_subset, dest = key
        current_prev = prev[size - 1][pre]

    end = time.time() - start

    return min_path, min_val, end


if __name__ == "__main__":
    config_lines = get_file_lines("config.ini")
    graph = []
    if config_lines[1].endswith('.txt'):
        graph = load_matrix(config_lines[1])
    elif config_lines[1].endswith(('.tsp', '.atsp')):
        graph = load_tsp(config_lines[1])

    times = []

    # for _ in range(int(config_lines[5])):
    #     min_path_cost, min_path, tsp_time = held_karp(graph)
    #     times.append(tsp_time)
    #

    print_matrix(graph)
    min_path, min_val, time = held_karp(graph)
    # for tsp_time in times:
    #     save_data([min_path, min_val, tsp_time])
    print(min_path)
    print(min_val)
