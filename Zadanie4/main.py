import random
import math
import time

from ulits import save_data, load_tsp, load_matrix, get_file_lines, print_matrix


def simulated_annealing(cities, T, alpha, stopping_T, stopping_iter):

    start = time.time()
    n = len(cities)
    current_solution = random.sample(range(n), n)

    best_solution = current_solution.copy()
    best_distance = distance(current_solution, cities)

    iter = 0

    while T > stopping_T:
        while iter < stopping_iter:
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)

            if i != j:
                new_solution = current_solution.copy()
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                current_distance = distance(current_solution, cities)
                new_distance = distance(new_solution, cities)
                ap = acceptance_probability(current_distance, new_distance, T)
                if ap > random.random():
                    current_solution = new_solution
                    if current_distance < best_distance:
                        best_solution = current_solution
                        best_distance = current_distance
            iter += 1
        iter = 0
        T = T*alpha
    duration = time.time() - start

    return best_solution, best_distance, duration


def distance(solution, cities):
    current_distance = 0
    for i in range(len(solution)):
        j = (i+1) % len(solution)
        city_i = solution[i]
        city_j = solution[j]
        current_distance += cities[city_i][city_j]
    return current_distance


def acceptance_probability(old_cost, new_cost, T):
    if new_cost < old_cost:
        return 1
    return math.exp((old_cost - new_cost) / T)


if __name__ == "__main__":
    config_lines = get_file_lines("config.ini")
    graph = []

    if config_lines[1].endswith('.txt'):
        graph = load_matrix(config_lines[1])
    elif config_lines[1].endswith(('.tsp', '.atsp')):
        graph = load_tsp(config_lines[1])

    times = []
    min_val = None
    min_path = []
    min_vals = []

    # for _ in range(int(config_lines[5])):
    #     min_path, min_val, tsp_time = simulated_annealing(graph, 3000, 0.999, 1, 100)
    #     min_vals.append(min_val)
    #     times.append(tsp_time)
    #
    # # for tsp_time in times:
    # #     save_data([min_path, min_val, tsp_time])
    #
    print_matrix(graph)
    # print(int(sum(min_vals)/int(config_lines[5])))
    # print(min_path)
    # print(sum(times)/int(config_lines[5]))
