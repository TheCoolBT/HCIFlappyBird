# README for Flappy Bird AI Project

## Overview
This project is an implementation of a Flappy Bird AI using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to play Flappy Bird by evolving neural networks over generations.

### Files Description

- **main.py**: This is the main script that runs the entire Flappy Bird AI simulation. It initializes the game, sets up the display, and controls the game loop where the NEAT algorithm is applied.

- **game_objects.py**: This file contains the classes for the game objects like the Bird, Pipe, and Floor. It uses Pygame to handle the visuals and physics of the game.

- **config.txt**: Configuration file for the NEAT algorithm. Key parameters include population size, fitness threshold, maximum stagnation, species elitism, elitism, and survival threshold. These parameters control various aspects of the NEAT algorithm, such as how genomes (neural networks) evolve and how species are maintained.

### NEAT Configuration Explained

- `pop_size`: Number of genomes in each generation.
- `fitness_threshold`: The fitness score at which the simulation will end if a bird reaches it.
- `max_stagnation`: The number of generations a species can exist without any improvement before it's removed.
- `species_elitism`: Number of species that are protected from extinction each generation.
- `elitism`: Number of top individuals that are carried over to the next generation.
- `survival_threshold`: Proportion of individuals in each species allowed to reproduce.

### Fitness Function

The fitness function in this implementation is determined by two key factors:

1. **Survival Time**: The primary component of fitness is how many frames the bird stays alive. This encourages birds to avoid pipes and survive as long as possible.

2. **Score**: Birds gain fitness points for every pipe they successfully pass. This encourages the bird to not only stay alive but also to navigate through the pipes effectively.

3. **Penalty for Crashing**: Birds lose fitness points if they crash into a pipe or fall to the ground. This penalty discourages behaviors that lead to collisions.

### Bird's Input Data

Each bird (neural network) receives the following input data to make decisions:

1. Height of the top pipe.
2. Height of the bottom pipe.
3. The y-position of the bird.
4. The y-velocity of the bird.

These inputs allow the bird to assess its environment and make decisions on whether to jump or not at each frame of the game.

### Running the Project

To run the project, ensure you have Python and Pygame installed. Run `main.py` to start the simulation. The NEAT algorithm will evolve the birds over generations to improve their performance in the game. 
