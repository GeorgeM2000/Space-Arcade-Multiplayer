import pygame as pg

class Scoreboard():

    def __init__(self, screen, ship_first_player, ship_second_player):

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.first_player_life = ship_first_player.initial_life
        self.second_player_life = ship_second_player.initial_life
        self.first_player_score= 0
        self.second_player_score = 0
        self.winner = None
        self.font = self.get_font(20)
        self.prepare_HP()
        self.prepare_Score()

    def get_font(self, size): 
        return pg.font.Font("Fonts/font.ttf", size)

    def prepare_HP(self):

        # Turn the HP into a rendered image
        first_player_hp = "HP " + str(self.first_player_life)
        second_player_hp = "HP " + str(self.second_player_life)

        # Create HP image
        self.first_player_hp_image = self.font.render(first_player_hp, True, (255,0,0), None) # (204,0,0) (230,230,230)
        self.second_player_hp_image = self.font.render(second_player_hp, True, (51,51,255), None) # (0,0,204) (230,230,230)

        # Create HP rectangle
        self.first_player_hp_rect = self.first_player_hp_image.get_rect()
        self.second_player_hp_rect = self.second_player_hp_image.get_rect()

        # Place rectangle on the screen
        self.first_player_hp_rect.right = self.screen_rect.right
        self.second_player_hp_rect.left = self.screen_rect.left

        self.first_player_hp_rect.bottom = 650
        self.second_player_hp_rect.top = 50

    def prepare_Score(self):
        # Turn the score into a rendered image
        first_player_score = "Score " + str(self.first_player_score)
        second_player_score = "Score " + str(self.second_player_score)

        # Create score image
        self.first_player_score_image = self.font.render(first_player_score, True, (255,0,0), None)
        self.second_player_score_image = self.font.render(second_player_score, True, (51,51,255), None)

        # Create score rectangle
        self.first_player_score_rect = self.first_player_score_image.get_rect()
        self.second_player_score_rect = self.second_player_score_image.get_rect()

        # Place rectangle on the screen
        self.first_player_score_rect.right = self.screen_rect.right
        self.second_player_score_rect.left = self.screen_rect.left

        self.first_player_score_rect.bottom = 625
        self.second_player_score_rect.top = 75

    def prepare_winner_message(self):
        # Create winner image
        if self.winner == 1:
            self.winner_image = self.font.render("First Player Wins!", True, (204,0,0), None)
        else:
            self.winner_image = self.font.render("Second Player Wins!", True, (0,0,204), None)
        
        # Create winner image rect and place it on the screen
        self.winner_rect = self.winner_image.get_rect()
        self.winner_rect.center = self.screen_rect.center
        self.winner_rect.bottom = 480

    # Show the winner
    def show_winner(self):
        if self.winner != None:
            self.screen.blit(self.winner_image, self.winner_rect)

    # Show the score
    def show_score(self):
        # HP -------------------
        self.screen.blit(self.first_player_hp_image, self.first_player_hp_rect)
        self.screen.blit(self.second_player_hp_image, self.second_player_hp_rect)

        # Score -------------------
        self.screen.blit(self.first_player_score_image, self.first_player_score_rect)
        self.screen.blit(self.second_player_score_image, self.second_player_score_rect)