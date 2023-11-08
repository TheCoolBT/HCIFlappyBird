import random
import pygame

SCREEN_HEIGHT = 512
SCREEN_WIDTH = 288
SCROLL_SPEED = 2

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


        self.image_sets = {
            'yellow': [
                pygame.image.load('assets/images/yellowbird-downflap.png'),
                pygame.image.load('assets/images/yellowbird-midflap.png'),
                pygame.image.load('assets/images/yellowbird-upflap.png')
            ],
            'blue': [
                pygame.image.load('assets/images/bluebird-downflap.png'),
                pygame.image.load('assets/images/bluebird-midflap.png'),
                pygame.image.load('assets/images/bluebird-upflap.png')
            ],
            'red': [
                pygame.image.load('assets/images/redbird-downflap.png'),
                pygame.image.load('assets/images/redbird-midflap.png'),
                pygame.image.load('assets/images/redbird-upflap.png')
            ]

        }
        #randomly select color for bird
        self.color = random.choice(['yellow','blue','red'])
        self.images = self.image_sets[self.color]

        self.index = 0
        self.image = self.images[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = (144,206))
        self.velocity = 0
        self.gravity = 0.25
        self.flap_time = 0
        self.base_animation_speed = 3
        self.animation_speed = self.base_animation_speed #The higher the number the slower the animation speed
        self.animation_counter = self.animation_speed
        self.flap_power = 5
        self.rotation = 0






    def update(self, event_list):
        self.velocity += self.gravity
        self.rect.y += self.velocity


        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jump()
        self.adjust_animation_speed()
        self.animate_flap()



        #Bird Rotation
        self.rotation = -self.velocity * 7
        self.rotate()

    def jump(self):
        self.velocity = -self.flap_power
        self.flap_time = 8
        self.animation_speed = self.base_animation_speed
        self.animation_counter = self.animation_speed


    def adjust_animation_speed(self):
        if self.velocity > 1:
            self.animation_speed = max(self.base_animation_speed, int(self.velocity * 2))
        else:
            self.animation_speed = self.base_animation_speed



    def animate_flap(self):
        if self.flap_time > 0 and self.animation_counter <=0:
            self.index = (self.index + 1) % len(self.images)
            self.animation_counter = self.animation_speed
        elif self.flap_time == 0:
            self.index = 0

        self.animation_counter -= 1
        self.image = self.images[self.index]

    def rotate(self):
        self.image = pygame.transform.rotate(self.images[self.index], self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)



class Pipe(pygame.sprite.Sprite):
    GAP_SIZE = 100  # The space between the top and bottom pipes, class variable
    PIPE_HEIGHT = 320  # The height of the pipe image, class variable
    FLOOR_HEIGHT = 112  # The floor height, class variable
    PIPE_WIDTH = 52  # The pipe image width, class variable
    USABLE_SPACE = SCREEN_HEIGHT - FLOOR_HEIGHT
    SPAWN_OFFSET = 100

    def __init__(self, inverted, x, y):
        super().__init__()
        self.inverted = inverted
        self.image = pygame.image.load('assets/images/pipe-green.png')
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

    def create_pipe_pair(cls):
        min_top = cls.GAP_SIZE + 100
        max_top = cls.USABLE_SPACE
        bottom_pipe_top = random.randint(min_top, max_top)
        bottom_pipe = Pipe(False, SCREEN_WIDTH + cls.SPAWN_OFFSET, bottom_pipe_top + cls.GAP_SIZE)
        top_pipe = Pipe(True, SCREEN_WIDTH + cls.SPAWN_OFFSET, bottom_pipe_top - cls.PIPE_HEIGHT)
        return bottom_pipe, top_pipe


class Floor(pygame.sprite.Sprite):
    HEIGHT = 112

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/base.png')
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right <= SCREEN_WIDTH:
            self.rect.left = 0




