import pygame as pg
import Multi_Player
import Single_Player
import json
import sys
import os

class Menu_Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)




class Menu:

    def __init__(self) -> None:
        pass


    def get_font(self, size): 
        return pg.font.Font("Fonts/font.ttf", size)
    
    
    def show_menu(self):
        pg.init()
        surface = pg.display.set_mode((800, 600))
        pg.display.set_caption("Space Arcade")

        # Background image
        background_image = pg.image.load("Background/Space.png").convert()


        while True:
            surface.blit(background_image, (0, 0))

            menu_mouse_pos = pg.mouse.get_pos()

            menu_text = self.get_font(50).render("MAIN MENU", True, (182, 143, 64))
            menu_rect = menu_text.get_rect(center=(400, 50))

            multi_player = Menu_Button(pg.image.load("Fonts/Multiplayer_Rect.png"), (400, 150), "MULTIPLAYER", self.get_font(35), (215, 252, 212), (255, 255, 255))

            single_player = Menu_Button(pg.image.load("Fonts/Singleplayer_Rect.png"), (400, 250), "SINGLE PLAYER", self.get_font(35), (215, 252, 212), (255, 255, 255))

            score = Menu_Button(pg.image.load("Fonts/Score_Rect.png"), (400, 350), "SCORE", self.get_font(35), (215, 252, 212), (255, 255, 255))

            guide = Menu_Button(pg.image.load("Fonts/Guide_Rect.png"), (400, 450), "GUIDE", self.get_font(35), (215, 252, 212), (255, 255, 255))

            quit = Menu_Button(pg.image.load("Fonts/Quit_Rect.png"), (400, 550), "QUIT", self.get_font(35), (215, 252, 212), (255, 255, 255))

            surface.blit(menu_text, menu_rect)

            for button in [multi_player, single_player, score, guide, quit]:
                button.changeColor(menu_mouse_pos)
                button.update(surface)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if multi_player.checkForInput(menu_mouse_pos):
                        multiplayer = Multi_Player.MultiPlayer()
                        multiplayer.run_game()
                    if single_player.checkForInput(menu_mouse_pos):
                        singleplayer = Single_Player.SinglePlayer()
                        singleplayer.run_game()
                    if score.checkForInput(menu_mouse_pos):
                        score = Score()
                        score.show_score()
                    if guide.checkForInput(menu_mouse_pos):
                        pass
                    if quit.checkForInput(menu_mouse_pos):
                        pg.quit()
                        sys.exit()

            pg.display.update()


class Score:

    def __init__(self) -> None:
        pass

    def get_font(self, size): 
        return pg.font.Font("Fonts/font.ttf", size)

    def reset_score(self, players_score):
        
        for key in players_score.keys():
            players_score[key]["Wins"] = 0
            players_score[key]["Losses"] = 0
            
        with open("Players_Score.json", "w") as f:
            json.dump(players_score, f)

        return players_score            

    def show_score(self):
        pg.init()
        surface = pg.display.set_mode((800, 600))
        pg.display.set_caption("Space Arcade")

        # Background image
        background_image = pg.image.load("Background/Space.png").convert()

        font = self.get_font(40)


        players_score = {}
        with open("Players_Score.json", "r") as f:
            players_score = json.load(f)

        first_player = ("WINS:" + str(players_score["First_Player"]["Wins"]), "LOSSES:" + str(players_score["First_Player"]["Losses"]))
        second_player = ("WINS:" + str(players_score["Second_Player"]["Wins"]), "LOSSES:" + str(players_score["Second_Player"]["Losses"]))
        surface_rect = surface.get_rect()

        while True:
            surface.blit(background_image, (0, 0))

            menu_mouse_pos = pg.mouse.get_pos()

            menu_text = self.get_font(50).render("SCORE", True, (182, 143, 64))
            menu_rect = menu_text.get_rect(center=(400, 50))

            surface.blit(menu_text, menu_rect)

            first_player_images = (font.render(first_player[0], True, (255,0,0), None), font.render(first_player[1], True, (255,0,0), None))
            first_player_rectangles = (first_player_images[0].get_rect(), first_player_images[1].get_rect())
            first_player_rectangles[0].right = surface_rect.right
            first_player_rectangles[1].right = surface_rect.right
            first_player_rectangles[0].bottom = 300
            first_player_rectangles[1].bottom = 400

            surface.blit(first_player_images[0], first_player_rectangles[0])
            surface.blit(first_player_images[1], first_player_rectangles[1])


            second_player_images = (font.render(second_player[0], True, (0,0,255), None), font.render(second_player[1], True, (0,0,255), None))
            second_player_rectangles = (second_player_images[0].get_rect(), second_player_images[1].get_rect())
            second_player_rectangles[0].left = surface_rect.left
            second_player_rectangles[1].left = surface_rect.left
            second_player_rectangles[0].bottom = 300
            second_player_rectangles[1].bottom = 400

            surface.blit(second_player_images[0], second_player_rectangles[0])
            surface.blit(second_player_images[1], second_player_rectangles[1])

            quit = Menu_Button(pg.image.load("Fonts/Quit_Rect.png"), (200, 550), "EXIT", self.get_font(35), (215, 252, 212), (255, 255, 255))
            reset = Menu_Button(pg.image.load("Fonts/Quit_Rect.png"), (600, 550), "RESET", self.get_font(35), (215, 252, 212), (255, 255, 255))


            for button in [quit, reset]:
                button.changeColor(menu_mouse_pos)
                button.update(surface)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if quit.checkForInput(menu_mouse_pos):
                        return
                    elif reset.checkForInput(menu_mouse_pos):
                        players_score = self.reset_score(players_score)
                        first_player = ("WINS:" + str(players_score["First_Player"]["Wins"]), "LOSSES:" + str(players_score["First_Player"]["Losses"]))
                        second_player = ("WINS:" + str(players_score["Second_Player"]["Wins"]), "LOSSES:" + str(players_score["Second_Player"]["Losses"]))
                        



            pg.display.update()
    



if __name__ == "__main__":
    menu = Menu()
    menu.show_menu()
        