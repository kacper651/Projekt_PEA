import os
import tsplib95


def load_matrix(file_name):
    lines = get_file_lines(file_name)
    lines.pop(0)
    adj_matrix = []
    for line in lines:
        adj_matrix.append([int(i) for i in line.split()])

    return adj_matrix


def load_tsp(path):
    problem = tsplib95.load(path)
    size = range(len(list(problem.get_nodes())))
    matrix = [[] for _ in size]
    for i in size:
        for j in size:
            matrix[i].append(problem.get_weight(i, j))

    return matrix


def get_file_lines(filepath):
    if not os.path.exists(filepath):
        raise Exception(f"Pliku nie ma: '{filepath}'")

    with open(filepath, 'r') as f:
        return f.read().splitlines()


def save_data(data):
    config_lines = get_file_lines("config.ini")
    output_file = config_lines[5]

    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write('droga;koszt;czas[s]\n')

    with open(output_file, 'a') as f:
        f.write(f'{data[0]};{data[1]};{str(data[2]).replace(".", ",")}\n')


def print_matrix(matrix):
    for row in matrix:
        for val in row:
            print(val, end=" ")
        print()
