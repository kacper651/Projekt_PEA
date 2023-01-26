import os
import tsplib95


# wczytywanie macierzy
def read_matrix(filepath):
    if filepath.split('.')[-1] == 'txt':
        lines = get_file_lines(filepath)
        lines = [line for line in lines if len(line.strip().split(' ')) > 1]  # usuwanie pustych linii

        matrix = [[] for _ in range(len(lines))]  # inicjalizacja macierzy 2D

        for i, line in enumerate(lines):
            values = " ".join(line.split()).split(' ')  # usuwanie zbednych spacji i rozdzial wartosci

            if len(values) == 1 or len(values) == 0:
                continue

            # wpisywanie do macierzy
            for v in values:
                matrix[i].append(int(v))

        return matrix

    ############## TSPLIB FORMAT ##############

    problem = tsplib95.load(filepath)
    size_range = range(len(list(problem.get_nodes())))

    # inicjalizacja macierzy 2D
    matrix = [[] for _ in size_range]

    # sprawdzanie czy macierz jest w formacie wspolrzednych
    coords = 'node_coords' in problem.as_dict().keys()

    for i in size_range:
        for j in size_range:
            matrix[i].append(problem.get_weight(i+1 if coords else i, j+1 if coords else j))

    return matrix


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


def save_data(data, output_file, input_file):
    if not os.path.exists(output_file):
        with open(output_file, 'w', encoding="utf-8") as f:
            f.write('file;cost;time[s];error[%];method;heuristic;path\n')

    with open(output_file, 'a', encoding="utf-8") as f:
        f.write(f'{input_file[8:]};'
                f'{str(data[1]).replace(".", ",")};'
                f'{str(data[2]).replace(".", ",")};'
                f'{str(data[3]).replace(".", ",")};'
                f'{data[4]};'
                f'{data[5]};'
                f'{data[6]}\n')


def print_matrix(matrix):
    for row in matrix:
        for val in row:
            print(f"{str(val): <4}", end=" ")
        print()
