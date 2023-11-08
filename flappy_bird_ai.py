import random
from deap import base, creator, tools, algorithms
import numpy as np

import main

#Neural Network Structure
INPUT_NODES = 3
HIDDEN_NODES = 5
OUTPUT_NODES = 1

# Define the genetic algorithm
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -1.0, 1.0)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=INPUT_NODES * HIDDEN_NODES + HIDDEN_NODES * OUTPUT_NODES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the neural network operations
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def neural_network(individual, inputs):
    # Assume individual is a flat list of weights
    hidden_layer = np.dot(inputs, np.reshape(individual[:INPUT_NODES * HIDDEN_NODES], (INPUT_NODES, HIDDEN_NODES)))
    hidden_layer = sigmoid(hidden_layer)
    output_layer = np.dot(hidden_layer, np.reshape(individual[INPUT_NODES * HIDDEN_NODES:], (HIDDEN_NODES, OUTPUT_NODES)))
    return sigmoid(output_layer)



def evaluate(individual):
    game_state = main.reset_game()
    score = 0
    time_survived = 0

    while True:
        inputs = main.get_game_state()
        action = neural_network(individual, inputs)
        game_over, current_score, time_elapsed = main.update_game(action >0.5)

        if game_over:
            break
        else:
            score = current_score
            time_survived += time_elapsed

    return score, time_survived


# Register genetic algorithm operations in toolbox
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

# Now we can set up the main evolutionary loop
def run_with_ai():
    population = toolbox.population(n=50)

    # Statistics to be gathered
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # Run the genetic algorithm
    final_population = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, verbose=True)

if __name__ == "__main__":
    run_with_ai()






