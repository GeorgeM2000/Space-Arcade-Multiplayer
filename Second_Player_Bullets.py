import pygame as pg
from pygame.sprite import Sprite 

class Second_Player_Bullets(Sprite):
    def __init__(self, screen, ship_second_player, ai, player):
        super(Second_Player_Bullets, self).__init__()
        self.screen = screen

        # Bullet attributes
        self.bullet_speed_factor = ship_second_player.bullet_speed_factor
        self.bullet_width = ship_second_player.bullet_width
        self.bullet_height = ship_second_player.bullet_height

        # Determine the bullet color
        if not ai:
            self.bullet_color = (51,51,255)
        else:
            self.bullet_color = (51,51,255) if player == "First_Player" else (255,0,0)
        
        # Create and position the bullet on the screen
        self.rect = pg.Rect(0,0, self.bullet_width, self.bullet_height)
        self.rect.centerx = ship_second_player.rect.centerx
        self.rect.bottom = ship_second_player.rect.bottom

        # y is the initial position of the bullet 
        self.y = float(self.rect.y)

    def update(self):
        # Move the bullet up the screen

        # Update the decimal position of the bullet
        self.y += self.bullet_speed_factor

        # Update the rect position of the bullet
        self.rect.y = self.y

    def draw_bullet(self):
        # Draw bullet to the screen
        pg.draw.rect(self.screen, self.bullet_color, self.rect)
