from sys import maxsize
from itertools import permutations as get_permutations
import time
import os


def load_matrix(file_name):
    lines = get_file_lines(file_name)
    lines.pop(0)
    adj_matrix = []
    for line in lines:
        adj_matrix.append([int(i) for i in line.split()])

    size = len(adj_matrix)
    return adj_matrix, size


def get_file_lines(filepath):
    if not os.path.exists(filepath):
        raise Exception(f"Pliku nie ma: '{filepath}'")

    with open(filepath, 'r') as f:
        return f.read().splitlines()


def save_data(data):
    output_file = config_lines[5]

    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write('droga;czas[s]\n')

    with open(output_file, 'a') as f:
        f.write(f'{data[0]};{str(data[1]).replace(".", ",")}\n')


def print_matrix(matrix):
    for row in matrix:
        for val in row:
            print(val, end=" ")
        print()


# funkcja TSP brute force
def tsp(graph, size):
    start = time.time()  # start pomiaru czasu
    min_path_cost = maxsize
    min_path = []
    permutations = get_permutations(range(size))  # wytworzenie listy permutacji
    for permutation in permutations:
        current_path_weight = 0  # inicjalizacja zmiennych
        current_vertex = 0
        for cost in permutation:
            current_path_weight += graph[current_vertex][cost]  # aktualizacja aktualnie rozpatrywanej ścieżki, czyli zwiekszenie kosztu itd
            current_vertex = cost
        current_path_weight += graph[current_vertex][0]

        if current_path_weight < min_path_cost:  # sprawdzenie czy rozwiazanie jest lepsze
            min_path_cost = current_path_weight
            min_path = permutation
    min_path = list(min_path)
    end = time.time() - start  # koniec pomiaru

    return min_path_cost, min_path, end


if __name__ == "__main__":
    config_lines = get_file_lines("config.ini")

    adj_matrix, size = load_matrix("./input/" + config_lines[1])
    times = []

    for _ in range(int(config_lines[3])):
        min_path_cost, min_path, tsp_time = tsp(adj_matrix, size)
        times.append(tsp_time)

    print_matrix(adj_matrix)
    print(min_path_cost)
    print(min_path)
    print(tsp_time)
    # for tsp_time in times:
    # save_data([min_path, tsp_time])
    # print("koniec")
