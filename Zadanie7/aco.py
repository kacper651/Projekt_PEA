import numpy as np


# main algorithm
def aco(alpha, beta, rho, ants, iterations, graph, pheromone_update_method, choice_heuristic):
    # initialize pheromone trails
    pheromone = np.ones((graph.shape[0], graph.shape[0]))
    pheromone /= graph.shape[0]
    # initialize const Q
    Q = 1.0
    # initialize the best length (for now big infinity)
    best_length = np.inf
    # initialize the best path (for now empty)
    best_path = []
    # for each iteration
    for i in range(iterations):
        # initialize length of paths for all ants (for now big number)
        length = np.ones(ants) * np.inf
        # initialize paths for all ants (for now empty)
        paths = []
        # initialize frequency factor
        frequency_factor = np.ones(graph.shape[0])
        # for each ant
        for j in range(ants):
            # initialize path with starting node
            path = [0]
            # initialize tabu list with starting node
            tabu = [0]
            # initialize current node
            current = 0
            # while not all nodes visited
            while len(tabu) < graph.shape[0]:
                # select next node with roulette wheel selection
                next_node = route_selector(current, alpha, beta, tabu, pheromone, graph, choice_heuristic, frequency_factor)
                # add node to tabu list
                tabu.append(next_node)
                # add node to path
                path.append(next_node)
                # update current node
                current = next_node
            # add return to starting node to path
            path.append(0)
            # calculate length of path
            length[j] = calculate_length(path, graph)
            # add path to paths
            paths.append(path)
            # update frequency factor
            frequency_factor = calculate_frequency_factor(paths, graph)
        # update pheromone trails
        pheromone = update_pheromone(pheromone, paths, length, Q, rho, pheromone_update_method, graph)
        # update the best length and path
        min_index = np.argmin(length)
        if length[min_index] < best_length:
            best_length = length[min_index]
            best_path = paths[min_index]
    return best_length, best_path


# calculate frequency factor
def calculate_frequency_factor(paths, graph):
    frequency_factor = np.zeros(graph.shape[0])
    # for each path
    for i in range(len(paths)):
        # for each node in path
        for j in range(len(paths[i])):
            # update frequency factor
            frequency_factor[paths[i][j]] += 1
    return frequency_factor


# select next node with probability according to chosen heuristic
def route_selector(current, alpha, beta, tabu, pheromone, graph, heuristic_method, frequency_factor):
    # initialize numerator
    numerator = np.zeros(graph.shape[0])
    if heuristic_method == 'visibility':
        # for each node
        for i in range(graph.shape[0]):
            # if node not in tabu list
            if i not in tabu:
                # calculate numerator
                numerator[i] = (pheromone[current][i] ** alpha) * ((1.0 / graph[current][i]) ** beta)
    elif heuristic_method == 'frequency factor':
        # for each node
        for i in range(graph.shape[0]):
            # if node not in tabu list
            if i not in tabu:
                # calculate numerator
                numerator[i] = ((pheromone[current][i] ** alpha) * (frequency_factor[current]) / graph[current][i]) ** beta  # ((1.0 / graph[current][i]) ** beta) * (1.0 / graph[current][i])
    # calculate denominator
    denominator = np.sum(numerator)
    # calculate probabilities
    probabilities = numerator / denominator
    # calculate cumulative sum of probabilities
    probabilities = np.cumsum(probabilities)
    # generate random number
    r = np.random.random()
    # select next node with roulette wheel selection
    for i, probability in enumerate(probabilities):
        if r < probability:
            return i


# update pheromone trails according to chosen method
def update_pheromone(pheromone, paths, length, Q, rho, method, graph):
    # for each path
    for i in range(len(paths)):
        # for each arc in path
        for j in range(len(paths[i]) - 1):
            # update pheromone trail
            if method == 'QAS':
                pheromone[paths[i][j]][paths[i][j + 1]] = (1 - rho) * pheromone[paths[i][j]][paths[i][j + 1]] + (Q / graph[i][j])
                pheromone[paths[i][j + 1]][paths[i][j]] = pheromone[paths[i][j]][paths[i][j + 1]]
            elif method == 'DAS':
                pheromone[paths[i][j]][paths[i][j + 1]] = (1 - rho) * pheromone[paths[i][j]][paths[i][j + 1]] + Q
                pheromone[paths[i][j + 1]][paths[i][j]] = pheromone[paths[i][j]][paths[i][j + 1]]
            elif method == 'CAS':
                pheromone[paths[i][j]][paths[i][j + 1]] = (1 - rho) * pheromone[paths[i][j]][paths[i][j + 1]] + Q / (length[i] ** i)
                pheromone[paths[i][j + 1]][paths[i][j]] = pheromone[paths[i][j]][paths[i][j + 1]]
    return pheromone


# calculate length of path
def calculate_length(path, graph):
    length = 0
    # for each arc in path
    for i in range(len(path) - 1):
        # add length of arc to path length
        length += graph[path[i]][path[i + 1]]
    return length
