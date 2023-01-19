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

    iterations = 0

    while T > stopping_T:
        while iterations < stopping_iter:
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
            iterations += 1
        iterations = 0
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
    input_file = config_lines[1]
    output_file = config_lines[3]
    iter_times = int(config_lines[5])
    start_T = int(config_lines[7])
    alpha = float(config_lines[9])
    end_T = float(config_lines[11])
    epoque_n = int(config_lines[13])

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

    # print_matrix(graph)

    for _ in range(iter_times):
        min_path, min_val, tsp_time = simulated_annealing(graph, start_T, alpha, end_T, epoque_n)
        min_vals.append(min_val)
        times.append(tsp_time)
        error = (min_val - int(optimal_cost)) * 100 / int(optimal_cost)
        errors.append(error)
        #save_data([min_path, min_val, tsp_time, error, input_file, epoque_n], output_file)
        epoque_n += 100

    print(f'Średni błąd: {sum(errors)/len(errors)}[%]')
    print(f'Średni czas: {sum(times)/len(times)}[s]')
    print(f'Średni koszt: {sum(min_vals)/len(min_vals)}')
