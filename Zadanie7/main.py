# import the necessary packages
import numpy as np
from utils import *


# Define the ant colony optimization algorithm
def ant_colony_optimization(graph, n_ants, n_iterations, alpha=1, beta=1, rho=0.5, q=1):
    # Initialize the pheromone matrix
    pheromone = np.ones((graph.shape[0], graph.shape[1])) / graph.shape[0]

    # Perform the ant colony optimization
    for i in range(n_iterations):
        # Create the ants
        ants = [_create_ant(graph, pheromone, alpha, beta) for j in range(n_ants)]

        # Calculate the tour length of each ant
        ant_scores = [_tour_length(graph, ant) for ant in ants]

        # Get the best ant
        best_ant = ants[np.argmin(ant_scores)]

        # Update the pheromone matrix
        pheromone = _update_pheromone(graph, pheromone, best_ant, rho, q)

    return best_ant


# Define the function to create an ant
def _create_ant(graph, pheromone, alpha, beta):
    # Set the initial node
    ant = [np.random.choice(graph.shape[0])]

    # Select the next node
    for i in range(graph.shape[0] - 1):
        # Get the current node
        current_node = ant[-1]

        # Calculate the transition probabilities
        transition_probabilities = _transition_probabilities(graph, pheromone, current_node, alpha, beta)

        # Select the next node
        next_node = np.random.choice(graph.shape[0], p=transition_probabilities)

        # Append the next node to the ant's path
        ant.append(next_node)

    return ant


# Define the transition probabilities
def _transition_probabilities(graph, pheromone, current_node, alpha, beta):
    # Initialize an array of probabilities
    probabilities = np.zeros(graph.shape[0])

    # Calculate the denominator
    total = 0
    for i in range(graph.shape[0]):
        if i != current_node:
            total += np.power(pheromone[current_node, i], alpha) * np.power(1 / graph[current_node, i], beta)

        # Calculate each transition probability
    for i in range(graph.shape[0]):
        if i == current_node:
            probabilities[i] = 0
        else:
            numerator = np.power(pheromone[current_node, i], alpha) * np.power(1 / graph[current_node, i], beta)
            probabilities[i] = numerator / total

    return probabilities


# Define the tour length
def _tour_length(graph, ant):
    # Initialize the tour length
    tour_length = 0

    # Calculate the tour length
    for i in range(len(ant) - 1):
        tour_length += graph[ant[i], ant[i + 1]]

    # Add the tour length from the last to the first node
    tour_length += graph[ant[-1], ant[0]]

    return tour_length


# Define the function to update the pheromone matrix
def _update_pheromone(graph, pheromone, ant, rho, q):
    # Calculate the pheromone deposition
    pheromone_deposition = np.zeros(graph.shape)
    for i in range(len(ant) - 1):
        pheromone_deposition[ant[i], ant[i + 1]] = q / _tour_length(graph, ant)
    pheromone_deposition[ant[-1], ant[0]] = q / _tour_length(graph, ant)

    # Update the pheromone matrix
    return (1 - rho) * pheromone + pheromone_deposition


if __name__ == "__main__":
    print("XD")
