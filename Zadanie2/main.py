from sys import maxsize
from ulits import load_matrix, get_file_lines, save_data, print_matrix
import time


def held_karp(graph, size):
    start = time.time()
    min_path_cost = maxsize
    min_path = []

    end = time.time() - start

    return min_path_cost, min_path, end


if __name__ == "__main__":
    config_lines = get_file_lines("config.ini")

    adj_matrix, size = load_matrix(config_lines[1])
    times = []

    for _ in range(int(config_lines[5])):
        min_path_cost, min_path, tsp_time = held_karp(adj_matrix, size)
        times.append(tsp_time)

    for tsp_time in times:
        save_data(min_path, tsp_time)

    print_matrix(adj_matrix)
    print(min_path_cost)
    print(min_path)
    print(tsp_time)
