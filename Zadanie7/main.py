import time
from utils import *
from aco import *


def get_optimal_cost():
    tsp_dict = {}
    with open("./input/TSPs.txt") as f:
        for line in f:
            (key, val) = line.split(":")
            tsp_dict[key] = val[:-1]
    return tsp_dict


def run_single_solver(input_file):
    # read config file
    config_lines = get_file_lines("config.ini")
    # input_file = config_lines[1]
    output_file = config_lines[3]
    iter_times = int(config_lines[5])
    alpha = float(config_lines[7])
    beta = float(config_lines[9])
    rho = float(config_lines[11])
    n_ants = int(config_lines[13])
    n_iterations = int(config_lines[15])
    update_method = config_lines[17].upper()
    heuristic = config_lines[19].lower()
    # initialize graph
    graph = []
    # initialize optimal cost
    optimal_cost = 0
    # check file extension
    if input_file.endswith('.txt'):
        graph = read_matrix(input_file)
    elif input_file.endswith('.tsp'):
        graph = read_matrix(input_file)
        optimal_cost = get_optimal_cost()[input_file[8:-4]]
    elif input_file.endswith('.atsp'):
        graph = read_matrix(input_file)
        optimal_cost = get_optimal_cost()[input_file[8:-5]]
    # initialize research variables
    times = []
    min_path = []
    min_vals = []
    errors = []
    graph = np.array(graph)
    # n_ants == n_cities
    if n_ants == 0:
        n_ants = len(graph)
    # run algorithm
    print("Running ACO...")
    print("Input file: " + input_file[8:])
    print("Parameters: alpha = " +
          str(alpha) + ", beta = " +
          str(beta) + ", rho = " +
          str(rho) + ", no. ants = " +
          str(n_ants) + ", no. iterations = " +
          str(n_iterations))
    if update_method != 'QAS' and update_method != 'DAS' and update_method != 'CAS':
        print(f'Invalid pheromone update method "{update_method}", using default QAS')
        update_method = 'QAS'
    print("Pheromone update method: " + update_method)
    if heuristic != 'frequency factor' and heuristic != 'visibility':
        print(f'Invalid heuristic "{heuristic}", using default visibility')
        heuristic = 'visibility'
    print("Heuristic: " + heuristic)
    print("Running " + str(iter_times) + " iteration(s)...")
    for i in range(iter_times):
        start_time = time.time()
        min_val, min_path = aco(alpha, beta, rho, n_ants, n_iterations, graph, update_method, heuristic)
        end_time = time.time()
        times.append(end_time - start_time)
        min_vals.append(min_val)
        error = np.divide(np.subtract(min_val, int(optimal_cost)), int(optimal_cost)) * 100
        errors.append(error)
    save_data([input_file[8:], np.mean(min_vals), np.mean(times).round(3), np.mean(errors).round(3), update_method,
               heuristic, min_path], output_file, input_file)
    print("Average time: ", np.mean(times).round(3))
    print("Average error[%]: ", np.mean(errors).round(3))
    print("Average cost: ", np.mean(min_vals))
    print("Shortest path: ", min_path)
    print()


if __name__ == "__main__":
    # TESTOWAĆ OSOBNO DLA ./input/rbg323.tsp i "./input/Rbg443.atsp"

    config_lines = get_file_lines("config.ini")
    instances = ["./input/Burma14.tsp", "./input/Gr17.tsp", "./input/Gr21.tsp", "./input/Gr24.tsp",
                 "./input/Bays29.tsp", "./input/Ftv33.atsp", "./input/Ftv44.atsp", "./input/Ft53.atsp",
                 "./input/Ch150.tsp", "./input/Ftv170.atsp", "./input/Gr202.tsp", "./input/Pcb442.tsp",
                 "./input/Gr666.tsp", "./input/Pr1002.tsp", "./input/Pr2392.tsp"]
    # for input_file in instances:
    #     run_single_solver(input_file.lower())

    run_single_solver(config_lines[1].lower())
    k = input("Press any key to exit...")
