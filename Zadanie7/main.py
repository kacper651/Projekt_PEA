import numpy as np
import time
from utils import *


# ant colony optimization algorithm with parameters: alpha, beta, rho, Q, n_ants, n_iterations
def aco(alpha, beta, rho, Q, n_ants, n_iterations, graph):
    # initialize pheromone trails
    pheromone = np.ones((graph.shape[0], graph.shape[0]))
    pheromone /= graph.shape[0]

    # initialize best length (for now big number)
    best_length = np.inf
    # initialize best path (for now empty)
    best_path = []

    # for each iteration
    for i in range(n_iterations):
        # initialize length of paths for all ants (for now big number)
        length = np.ones(n_ants) * np.inf
        # initialize paths for all ants (for now empty)
        paths = []

        # for each ant
        for j in range(n_ants):
            # initialize path with starting node
            path = [0]
            # initialize tabu list with starting node
            tabu = [0]
            # initialize current node
            current = 0

            # while not all nodes visited
            while len(tabu) < graph.shape[0]:
                # select next node with roulette wheel selection
                next_node = roulette_wheel_selection(current, alpha, beta, tabu, pheromone, graph)
                # add node to tabu list
                tabu.append(next_node)
                # add node to path
                path.append(next_node)
                # update current node
                current = next_node

            # add return to depot to path
            path.append(0)
            # calculate length of path
            length[j] = calculate_length(path, graph)
            # add path to paths
            paths.append(path)

        # update pheromone trails
        pheromone = update_pheromone(pheromone, paths, length, Q, rho)

        # update best length and path
        min_index = np.argmin(length)
        if length[min_index] < best_length:
            best_length = length[min_index]
            best_path = paths[min_index]

        # print progress
        # print('Iteration: {}, best length: {}'.format(i, best_length))

    return best_length, best_path


# roulette wheel selection
def roulette_wheel_selection(current, alpha, beta, tabu, pheromone, distance):
    # initialize numerator
    numerator = np.zeros(distance.shape[0])
    # for each node
    for i in range(distance.shape[0]):
        # if node not in tabu list
        if i not in tabu:
            # calculate numerator
            numerator[i] = (pheromone[current][i] ** alpha) * ((1.0 / distance[current][i]) ** beta)

    # calculate denominator
    denominator = np.sum(numerator)
    # calculate probabilities
    probabilities = numerator / denominator
    # calculate cumsum of probabilities
    probabilities = np.cumsum(probabilities)
    # generate random number
    r = np.random.random()
    # select next node with roulette wheel selection
    for i, probability in enumerate(probabilities):
        if r < probability:
            return i


# update pheromone trails
def update_pheromone(pheromone, paths, length, Q, rho):
    # for each path
    for i in range(len(paths)):
        # for each arc in path
        for j in range(len(paths[i]) - 1):
            # update pheromone trail
            pheromone[paths[i][j]][paths[i][j + 1]] = (1 - rho) * pheromone[paths[i][j]][paths[i][j + 1]] + (
                        Q / length[i])
            pheromone[paths[i][j + 1]][paths[i][j]] = pheromone[paths[i][j]][paths[i][j + 1]]

    return pheromone


# calculate length of path
def calculate_length(path, distance):
    length = 0
    # for each arc in path
    for i in range(len(path) - 1):
        # add length of arc to path length
        length += distance[path[i]][path[i + 1]]

    return length


if __name__ == "__main__":
    config_lines = get_file_lines("config.ini")
    input_file = config_lines[1]
    output_file = config_lines[3]
    iter_times = int(config_lines[5])
    alpha = float(config_lines[7])
    beta = float(config_lines[9])
    rho = float(config_lines[11])
    Q = float(config_lines[13])
    n_ants = int(config_lines[15])
    n_iterations = int(config_lines[17])

    graph = []
    optimal_cost = 0

    if input_file.endswith('.txt'):
        graph, optimal_cost = load_matrix(config_lines[1])
    elif input_file.endswith(('.tsp', '.atsp')):
        graph = load_tsp(config_lines[1])

    times = []
    min_val = 0
    min_path = []
    min_vals = []
    error = 0
    errors = []
    graph = np.array(graph)

    print("Running ACO...")
    print("Input file: " + input_file[8:])
    print("Parameters: alpha = " + str(alpha) +
          ", beta = " + str(beta) + ", rho = " +
          str(rho) + ", Q = " + str(Q) + ", no. ants = " +
          str(n_ants) + ", no. iterations = " + str(n_iterations))
    if len(graph) < 30:
        print("Graph:")
        print_matrix(graph)

    for i in range(iter_times):
        start_time = time.time()
        min_val, min_path = aco(alpha, beta, rho, Q, n_ants, n_iterations, graph)
        end_time = time.time()
        times.append(end_time - start_time)
        min_vals.append(min_val)
        error = np.divide(np.subtract(min_val, int(optimal_cost)), int(optimal_cost)) * 100
        errors.append(error)

    print("Average time: ", np.mean(times))
    print("Average error[%]: ", np.mean(errors))
    print("Average cost: ", np.mean(min_vals))
    print("Shortest path: ", min_path)
