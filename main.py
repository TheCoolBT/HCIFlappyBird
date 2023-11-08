"""
A game of flappy bird made with pygame

Date Modified:  Nov 7, 2023
Author: Ben Tyler
Estimated Work Time: 20 Hours
"""

import os.path
import neat
import pygame
from game_objects import Bird, Pipe, Floor

# Initialize Pygame
pygame.init()

base_image = pygame.image.load('assets/images/base.png')
background_image = pygame.image.load('assets/images/background-day.png')
SCREEN_WIDTH, SCREEN_HEIGHT = background_image.get_size()
FPS = 60
gen = 0

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Clock to control the frame rate
clock = pygame.time.Clock()


# Initialize pipes
pipe_group = pygame.sprite.Group()
PIPE_SPAWN_TIME = 1800
last_pipe_time = pygame.time.get_ticks()

# Initialize floor
floor = Floor(0, SCREEN_HEIGHT - 112)
floor_group = pygame.sprite.GroupSingle(floor)

# Initialize Font
pygame.font.init()
font = pygame.font.SysFont('Arial', 10)


def check_collison(bird, pipes):
    bird_mask = bird.mask
    for pipe in pipes:
        pipe_mask = pipe.mask

        # Check collision with bottom pipe
        offset_x = pipe.rect.left - bird.rect.left
        offset_y = pipe.rect.top - bird.rect.top


        if bird_mask.overlap(pipe_mask, (offset_x, offset_y)):
            return True

    return False


def calculate_inputs(bird, pipes):
    for pipe in pipes:
        # Since pipes are moving left, we find the set of pipes that are coming next
        if pipe.rect.right > bird.rect.left:
            bottom_edge_of_gap = pipe.rect.top  # The top of the bottom pipe
            top_edge_of_gap = bottom_edge_of_gap - Pipe.GAP_SIZE # The bottom of the top piper
            vertical_distance = bird.rect.top # The y value of the bird's height
            velocity = bird.velocity 


            # Calculate vertical distances
            vertical_distance_bottom_of_top_pipe = bird.rect.top - top_edge_of_gap
            vertical_distance_top_of_bottom_pipe = bottom_edge_of_gap - bird.rect.bottom

            return vertical_distance_bottom_of_top_pipe, vertical_distance_top_of_bottom_pipe, vertical_distance,velocity
            

    # If there are no pipes on screen, will compare to dummy pipe that is perfectly centered
    distance_from_top_default_pipe = bird.rect.top - 180
    distance_from_bottom_default_pipe = 250 - bird.rect.bottom
    return distance_from_top_default_pipe,distance_from_bottom_default_pipe, bird.rect.top, bird.velocity
    


def calculate_fitness_reward(bird, pipes):
    #This function can be used later to make the birds so smart that they perfect the game after 1 generation
    for pipe in pipes:
        bird_center_y = bird.rect.centery
        if pipe.rect.right > bird.rect.left:
            center_of_gap = pipe.rect.top + 50
            distance_from_center = abs(center_of_gap - bird_center_y)
            distances = calculate_inputs(bird, pipes)
            if distances[0] < 0 or distances[1] < 0:
                reward = 0
            else:
                reward = abs(0.3 * (1 - distance_from_center / 50))

            return reward
    return 0






def fitness_function(genomes, config):
    global last_pipe_time, score, gen
    nets = []
    ge = []
    birds = []
    bird_groups = [pygame.sprite.GroupSingle(b) for b in birds]
    score = 0
    gen += 1
    last_pipe = None


    for pipe in pipe_group:
        pipe.kill()

    last_pipe_time = pygame.time.get_ticks()

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        new_bird = Bird()
        birds.append(new_bird)
        bird_group = pygame.sprite.GroupSingle(new_bird)
        bird_groups.append(bird_group)
        g.fitness = 0
        ge.append(g)



    running = True

    while running and len(birds) > 0:
        clock.tick(FPS)
        screen.blit(background_image, (0, 0))

        # Handle events
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()




        for x, bird in enumerate(birds):
            # give reward for remaining between the next 2 pipes
            distances = calculate_inputs(bird,pipe_group)
            
            ge[x].fitness += 0.1

            #If you want the birds to enter "god-mode" replace ge[x].fitness += 0.1 with:
            #if distances[0] > 0 and distances[1] > 0:
                #ge[x].fitness += calculate_fitness_reward(bird, pipe_group) 

            output = nets[birds.index(bird)].activate(calculate_inputs(bird, pipe_group))
            if output[0] > 0.8:
                bird.jump()

        # Handle Collison
        for x, bird in enumerate(birds):
            if check_collison(bird, pipe_group) or bird.rect.bottom >= SCREEN_HEIGHT - 112 or bird.rect.y < -50:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                bird.kill()

        # Pipe logic
        time_now = pygame.time.get_ticks()
        if (last_pipe is None or (birds and birds[0].rect.left > last_pipe.rect.right)) and (time_now - last_pipe_time > PIPE_SPAWN_TIME):
            bottom_pipe, top_pipe = Pipe.create_pipe_pair(Pipe)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe_time = time_now
            last_pipe = top_pipe

        for pipe in pipe_group:
            for x, bird in enumerate(birds):
                if pipe.rect.right < bird.rect.left and not pipe.passed:
                    score += 0.5
                    ge[x].fitness += 2.5
                    pipe.passed = True


        # Game logic goes here
        for bird_group in bird_groups:
            bird_group.update(event_list)
        pipe_group.update()
        floor_group.update()

        # Draw Bird, Pipes, and Floor
        for bird_group in bird_groups:
            bird_group.draw(screen)
        pipe_group.draw(screen)
        floor_group.draw(screen)

        #Draw the Score
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Calculate and Draw the Distances
        gen_text = font.render(f'Generation: {gen}', True, (255, 255, 255))
        screen.blit(gen_text, (10, 50))  # You can adjust the position as needed

        birds_alive = len(birds)
        birds_alive_text = font.render(f'Birds Alive: {birds_alive}', True, (255, 255, 255))
        screen.blit(birds_alive_text, (10, 100))  # You can adjust the position as needed

        if len(birds) > 0:
            inputs = calculate_inputs(birds[0], pipe_group)
            distance_text = font.render(f'Inputs: {inputs}', True, (255, 255, 255))
            screen.blit(distance_text, (10, 150))  # You can adjust the position as needed


        # Update the display
        pygame.display.update()



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(fitness_function, 10) #run for 10 generations

    print('\nBest genome:\n{!s}'.format(winner))




if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    run(config_path)


