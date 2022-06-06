import pygame as pg
from pygame.sprite import Sprite

class Explosion(Sprite):

    def __init__(self, x, y):
        Sprite.__init__(self)

        # Append the images to a list
        self.images = []
        for num in range(1,6):
            img = pg.transform.scale(pg.image.load(f'Explosions/exp{num}.png'), (100,100))
            self.images.append(img)

        # Specify the position of the explosion
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        # Update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
    


        