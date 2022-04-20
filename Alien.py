import pygame as pg
import random
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, screen, aliens_x_position, alien_y_position):
        super(Alien, self).__init__()
        self.screen = screen

        self.alien_code = random.randint(1, 5)

        # Load alien image
        self.image = pg.image.load_basic(self.pick_alien_type(self.alien_code))

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
        self.life = random.randint(5, 15) # 5 15
        self.life_initial_value = self.life


    def update(self):
        if self.alien_right_movement and self.rect.x <= 1200:
            self.rect.x += self.speed_factor
        elif self.alien_left_movement and self.rect.x >= 0:
            self.rect.x -= self.speed_factor

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def pick_alien_type(self, alien_code):
        if alien_code == 1:
            return 'Aliens\\alien.bmp'
        elif alien_code == 2:
            return 'Aliens\\alienblue.bmp'
        elif alien_code == 3:
            return 'Aliens\\alienred.bmp'
        elif alien_code == 4:
            return 'Aliens\\alienblack.bmp'
        elif alien_code == 5:
            return 'Aliens\\alienorange.bmp'
        
        
