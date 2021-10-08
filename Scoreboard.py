import pygame as pg

class Scoreboard():

    def __init__(self, screen, ship_first_player, ship_second_player):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.first_player_life = ship_first_player.initial_life
        self.second_player_life = ship_second_player.initial_life


        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        self.prep_score()

    def prep_score(self):
        # Turn the score into a rendered image
        first_player_score = str(self.first_player_life)
        second_player_score = str(self.second_player_life)

        self.first_player_score_image = self.font.render(first_player_score, True, self.text_color, (230,230,230))
        self.second_player_score_image = self.font.render(second_player_score, True, self.text_color, (230,230,230))

        self.first_player_score_rect = self.first_player_score_image.get_rect()
        self.second_player_score_rect = self.second_player_score_image.get_rect()

        self.first_player_score_rect.right = self.screen_rect.right
        self.second_player_score_rect.right = self.screen_rect.left + 55

        self.first_player_score_rect.top = 50
        self.second_player_score_rect.bottom = 650

    def show_score(self):
        self.screen.blit(self.first_player_score_image, self.first_player_score_rect)
        self.screen.blit(self.second_player_score_image, self.second_player_score_rect)