import pygame as pg
from pygame.sprite import Sprite 

class First_Player_Bullets(Sprite):
    def __init__(self, screen, ship_first_player, ai, player):
        super(First_Player_Bullets, self).__init__()
        self.screen = screen

        # Bullet attributes
        self.bullet_speed_factor = ship_first_player.bullet_speed_factor
        self.bullet_width = ship_first_player.bullet_width
        self.bullet_height = ship_first_player.bullet_height

        # Determine the bullet color
        if not ai:
            self.bullet_color = (255,0,0)
        else:
            self.bullet_color = (255,0,0) if player == "First_Player" else (51,51,255)
       
        # Create and position the bullet on the screen
        self.rect = pg.Rect(0,0, self.bullet_width, self.bullet_height)
        self.rect.centerx = ship_first_player.rect.centerx
        self.rect.top = ship_first_player.rect.top

        # y is the initial position of the bullet
        self.y = float(self.rect.y)

    def update(self):
        # Move the bullet up the screen

        # Update the decimal position of the bullet
        self.y -= self.bullet_speed_factor

        # Update the rect position of the bullet
        self.rect.y = self.y

    def draw_bullet(self):
        # Draw bullet to the screen
        pg.draw.rect(self.screen, self.bullet_color, self.rect)