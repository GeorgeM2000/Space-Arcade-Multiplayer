import pygame as pg
import random
from pygame.sprite import Sprite

class Asteroid(Sprite):

    def __init__(self, screen, asteroid_x_position, asteroid_y_position):
        super(Asteroid, self).__init__()

        self.screen = screen
        self.asteroid_code = random.randint(1, 5)
        self.asteroid_x = asteroid_x_position

        # Load asteroid image
        self.image = pg.image.load(self.pick_asteroid_type(self.asteroid_code)).convert_alpha()

        # Get alien image width and height
        self.rect = self.image.get_rect()
 

        # Set alien coordinates(x and y)
        self.rect.x = asteroid_x_position
        self.rect.y =  asteroid_y_position

        # Set alien movement
        self.asteroid_right_movement = False
        self.asteroid_left_movement = False

        if self.rect.x > 1200: 
            self.asteroid_left_movement = True
        else:
            self.asteroid_right_movement = True

        # Alien utilities
        self.speed_factor = 1
        self.life_reduction_rate = 1
        self.life = random.randint(5, 10) 
        self.life_initial_value = self.life


    def update(self):
        if self.asteroid_right_movement and self.rect.x <= 1200:
            self.rect.x += self.speed_factor
        elif self.asteroid_left_movement and self.rect.x >= 0:
            self.rect.x -= self.speed_factor

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # Pick an alien type based on the alien code
    def pick_asteroid_type(self, asteroid_code):
        if asteroid_code == 1:
            return 'Asteroids/AsteroidBlue.png' 
        elif asteroid_code == 2:
            return 'Asteroids/AsteroidBrown.png'
        elif asteroid_code == 3:
            return 'Asteroids/AsteroidYellow.png'
        elif asteroid_code == 4:
            return 'Asteroids/AsteroidOrange.png'
        elif asteroid_code == 5:
            return 'Asteroids/AsteroidGreen.png'
        
        
