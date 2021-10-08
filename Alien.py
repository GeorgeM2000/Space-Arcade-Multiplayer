import pygame as pg
import random
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, screen, aliens_x_position, alien_y_position):
        super(Alien, self).__init__()
        self.screen = screen

        # Load alien image
        self.image = pg.image.load_basic('C:\\Users\\giorg\\SpaceshipArcade\\Aliens\\alien.bmp')

        # Get alien image width and height
        self.rect = self.image.get_rect()
 

        # Set alien coordinates(x and y)
        self.rect.x = aliens_x_position[random.randint(0, 3)]
        self.rect.y =  alien_y_position


        self.x = float(self.rect.x)

        # Set alien movement
        self.alien_right_movement = False
        self.alien_left_movement = False

        if self.rect.x > 1200: 
            self.alien_left_movement = True
        else:
            self.alien_right_movement = True

        # Alien utilities
        self.speed_factor = 1
        self.life_reduction_rate = 1
        self.life = random.randint(1, 3) # 5 15
        self.life_initial_value = self.life


    def update(self):
        if self.alien_right_movement and self.rect.x <= 1200:
            self.rect.x += self.speed_factor
        elif self.alien_left_movement and self.rect.x >= 0:
            self.rect.x -= self.speed_factor

    def blitme(self):
        self.screen.blit(self.image, self.rect)
