import pygame.font
import pygame as pg

class StartButton():

    def __init__(self, screen, message):
        self.screen = screen

        # Button attributes
        self.screen_rect = screen.get_rect()
        self.running_state = False
        self.width, self.height = 200, 50
        self.button_color = (51,51,255)
        self.text_color = (255,255,255)
        self.font = self.get_font(30)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Prepare the message
        self.prep_message(message)

    def get_font(self, size): 
        return pg.font.Font("Fonts/font.ttf", size)

    def prep_message(self, message):

        # Create the message image, the rectangle and position the rectangle on the screen
        self.msg_image = self.font.render(message, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    # Draw the button on the screen
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

