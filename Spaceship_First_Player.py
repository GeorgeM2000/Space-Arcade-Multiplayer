import pygame as pg

class Spaceship_First_Player():

    def __init__(self, screen):
        self.screen = screen

        self.image = pg.image.load('C:\\Users\\giorg\\SpaceshipArcade\\ship.bmp')

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.right_movement = False
        self.left_movement = False

        self.speed_factor = 1 
        self.bullets_allowed = 3
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.life_reduction = 1
        self.initial_life = 100

    def update(self):
        if self.right_movement and self.rect.right < self.screen_rect.right:
            self.rect.centerx += 1  #self.speed_factor
        elif self.left_movement and self.rect.left > 0:
            self.rect.centerx -= 1  #self.speed_factor

    def blitme(self):
        self.screen.blit(pg.transform.scale(self.image, (60,48)), self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx