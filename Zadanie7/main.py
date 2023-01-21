import time
from utils import *
from aco import *


if __name__ == "__main__":
    # read config file
    config_lines = get_file_lines("config.ini")
    input_file = config_lines[1]
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
    optimal_cost = 0
    # check file extension
    if input_file.endswith('.txt'):
        graph, optimal_cost = load_matrix(config_lines[1])
    elif input_file.endswith(('.tsp', '.atsp')):
        graph = load_tsp(config_lines[1])
    # initialize research variables
    times = []
    min_val = 0
    min_path = []
    min_vals = []
    error = 0
    errors = []
    graph = np.array(graph)
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
    for i in range(iter_times):
        start_time = time.time()
        min_val, min_path = aco(alpha, beta, rho, n_ants, n_iterations, graph, update_method, heuristic)
        end_time = time.time()
        times.append(end_time - start_time)
        min_vals.append(min_val)
        error = np.divide(np.subtract(min_val, int(optimal_cost)), int(optimal_cost)) * 100
        errors.append(error)
    print("Average time: ", np.mean(times))
    print("Average error[%]: ", np.mean(errors))
    print("Average cost: ", np.mean(min_vals))
    print("Shortest path: ", min_path)
