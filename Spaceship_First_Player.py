import pygame as pg

class Spaceship_First_Player():

    def __init__(self, screen):
        self.screen = screen

        # Load the spaceship image
        self.image = pg.image.load("Spaceship/Spaceship_1.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Position the rectangle on the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Set initial movement
        self.right_movement = False
        self.left_movement = False

        # Set initial settings
        self.bullets_allowed = 3
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.life_reduction = 1
        self.initial_life = 50

    # Update function to move the spaceship
    def update(self):

        # If the spaceship is moving right and the x position of it's right side is less than the width of the screen
        if self.right_movement and self.rect.right < self.screen_rect.right:
            # Move right
            self.rect.centerx += 1  

        # If the spaceship is moving left and the x position of it's left side is greater than 0
        elif self.left_movement and self.rect.left > 0:
            # Move left
            self.rect.centerx -= 1

    # Function to draw the image on the screen
    def blitme(self):
        self.screen.blit(pg.transform.scale(self.image, (60,48)), self.rect)

    # Function to center the spaceship
    def center_ship(self):
        self.center = self.screen_rect.centerx