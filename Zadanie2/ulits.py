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
    output_file = get_file_lines("config.ini")[5]

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
