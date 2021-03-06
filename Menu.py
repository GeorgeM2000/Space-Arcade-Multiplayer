from curses.textpad import rectangle
from more_itertools import first
import pygame as pg
import Multi_Player
import Single_Player
import json
import sys
import os


# This class creates the menu button
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



# Main Menu class
class Menu:

    def __init__(self) -> None:
        pass


    def get_font(self, size): 
        return pg.font.Font("Fonts/font.ttf", size)
    
    
    def show_menu(self):

        # Initialize pygame, set dimentions and title
        pg.init()
        surface = pg.display.set_mode((800, 600))
        pg.display.set_caption("Space Arcade")

        # Background image
        background_image = pg.image.load("Background/Space.png").convert()

        # Start background music
        pg.mixer.init()
        pg.mixer.music.load('Sounds/Menu_Music.wav')
        pg.mixer.music.play(-1)

        while True:
            surface.blit(background_image, (0, 0))

            menu_mouse_pos = pg.mouse.get_pos()

            # Create menu text
            menu_text = self.get_font(50).render("MAIN MENU", True, (182, 143, 64))
            menu_rect = menu_text.get_rect(center=(400, 50))

            # Create buttons
            multi_player = Menu_Button(pg.image.load("Fonts/Multiplayer_Rect.png"), (400, 150), "MULTIPLAYER", self.get_font(35), (215, 252, 212), (210,105,30))

            single_player = Menu_Button(pg.image.load("Fonts/Singleplayer_Rect.png"), (400, 250), "SINGLE PLAYER", self.get_font(35), (215, 252, 212), (128,0,128))

            score = Menu_Button(pg.image.load("Fonts/Score_Rect.png"), (400, 350), "SCORE", self.get_font(35), (215, 252, 212), (255, 140, 0))

            guide = Menu_Button(pg.image.load("Fonts/Guide_Rect.png"), (400, 450), "GUIDE", self.get_font(35), (215, 252, 212), (0, 255, 0))

            quit = Menu_Button(pg.image.load("Fonts/Quit_Rect.png"), (400, 550), "QUIT", self.get_font(35), (215, 252, 212), (0, 0, 0))

            surface.blit(menu_text, menu_rect)

            # Update the buttons and change their color as user hovers over them
            for button in [multi_player, single_player, score, guide, quit]:
                button.changeColor(menu_mouse_pos)
                button.update(surface)
            
            # Check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Multi player
                    if multi_player.checkForInput(menu_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        pg.mixer.music.stop()
                        multiplayer = Multi_Player.MultiPlayer()
                        multiplayer.run_game()
                    # Single player
                    if single_player.checkForInput(menu_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        choose_player = Player_Option()
                        choose_player.show_player_option()
                    # Score
                    if score.checkForInput(menu_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        score = Score()
                        score.show_score()
                    # Guide
                    if guide.checkForInput(menu_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        guide = Guide()
                        guide.show_guide()
                    # Quit
                    if quit.checkForInput(menu_mouse_pos):
                        pg.quit()
                        sys.exit()

            pg.display.update()

# Score class
# This class shows the score for the first ans second player
class Score:

    def __init__(self) -> None:
        pass

    def get_font(self, size): 
        return pg.font.Font("Fonts/font.ttf", size)

    def reset_score(self, players_score):
        
        # Set wins and losses for each player to zero
        for key in players_score.keys():
            players_score[key]["Wins"] = 0
            players_score[key]["Losses"] = 0
            
        # Write it to the "Players_Score.json" file
        with open("Players_Score.json", "w") as f:
            json.dump(players_score, f)

        return players_score            

    def show_score(self):

        # Initialize pygame, set dimentions and title
        pg.init()
        surface = pg.display.set_mode((800, 600))
        pg.display.set_caption("Space Arcade")

        # Background image
        background_image = pg.image.load("Background/Space.png").convert()

        # Set font style
        font = self.get_font(40)

        # Load players score
        players_score = {}
        with open("Players_Score.json", "r") as f:
            players_score = json.load(f)

        # Prepare the message for the first and second player
        first_player = ("WINS:" + str(players_score["First_Player"]["Wins"]), "LOSSES:" + str(players_score["First_Player"]["Losses"]))
        second_player = ("WINS:" + str(players_score["Second_Player"]["Wins"]), "LOSSES:" + str(players_score["Second_Player"]["Losses"]))
        surface_rect = surface.get_rect()

        while True:
            # Blit the background image
            surface.blit(background_image, (0, 0))

            score_mouse_pos = pg.mouse.get_pos()

            score_text = self.get_font(50).render("SCORE", True, (182, 143, 64))
            score_rect = score_text.get_rect(center=(400, 50))

            surface.blit(score_text, score_rect)

            # Show first player score
            first_player_images = (font.render(first_player[0], True, (255,0,0), None), font.render(first_player[1], True, (255,0,0), None))
            first_player_rectangles = (first_player_images[0].get_rect(), first_player_images[1].get_rect())
            first_player_rectangles[0].right = surface_rect.right
            first_player_rectangles[1].right = surface_rect.right
            first_player_rectangles[0].bottom = 300
            first_player_rectangles[1].bottom = 400

            surface.blit(first_player_images[0], first_player_rectangles[0])
            surface.blit(first_player_images[1], first_player_rectangles[1])

            # Show second player score
            second_player_images = (font.render(second_player[0], True, (0,0,255), None), font.render(second_player[1], True, (0,0,255), None))
            second_player_rectangles = (second_player_images[0].get_rect(), second_player_images[1].get_rect())
            second_player_rectangles[0].left = surface_rect.left
            second_player_rectangles[1].left = surface_rect.left
            second_player_rectangles[0].bottom = 300
            second_player_rectangles[1].bottom = 400

            surface.blit(second_player_images[0], second_player_rectangles[0])
            surface.blit(second_player_images[1], second_player_rectangles[1])

            # Create an exit button
            exit = Menu_Button(pg.image.load("Fonts/Quit_Rect.png"), (200, 550), "EXIT", self.get_font(35), (215, 252, 212), (0, 0, 0))
            
            # Create a reset button
            reset = Menu_Button(pg.image.load("Fonts/Quit_Rect.png"), (600, 550), "RESET", self.get_font(35), (215, 252, 212), (218,165,32))

            # Change button color when user hovers ove them
            for button in [exit, reset]:
                button.changeColor(score_mouse_pos)
                button.update(surface)

            # Check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Exit
                    if exit.checkForInput(score_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        return
                    # Reset
                    elif reset.checkForInput(score_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        players_score = self.reset_score(players_score)
                        first_player = ("WINS:" + str(players_score["First_Player"]["Wins"]), "LOSSES:" + str(players_score["First_Player"]["Losses"]))
                        second_player = ("WINS:" + str(players_score["Second_Player"]["Wins"]), "LOSSES:" + str(players_score["Second_Player"]["Losses"]))
                        
            pg.display.update()


# Guide class
# Guide shows information about the game
class Guide:
    def __init__(self) -> None:
        pass

    def get_font(self, size): 
        return pg.font.Font("Fonts/font.ttf", size)


    def show_guide(self):

        # Initialize pygame, set dimentions and title
        pg.init()
        surface = pg.display.set_mode((800, 600))
        pg.display.set_caption("Space Arcade")

        # Background image
        background_image = pg.image.load("Background/Space.png").convert()

        # Font
        font = self.get_font(15)

        # Container
        container_surface = pg.Surface((800, 400))
        container_surface.set_alpha(200)
        container_surface.fill((255,255,255))

        # Spaceship image
        first_spaceship = pg.image.load("Spaceship/Spaceship_1.png").convert_alpha()
        second_spaceship = pg.image.load("Spaceship/Spaceship_1.png").convert_alpha()
        second_spaceship = pg.transform.flip(second_spaceship, False, True)

        # Brown asteroid
        brown_asteroid = pg.image.load("Asteroids/AsteroidBrown.png").convert_alpha()
        
        while True:
            # Blit the background image
            surface.blit(background_image, (0, 0))

            guide_mouse_pos = pg.mouse.get_pos()

            guide_text = self.get_font(50).render("GUIDE", True, (182, 143, 64))
            guide_rect = guide_text.get_rect(center=(400, 50))

            # Show guide text
            surface.blit(guide_text, guide_rect)

            # Show container
            surface.blit(container_surface, (0,100))

            # Blit the images
            surface.blit(pg.transform.scale(first_spaceship, (60,48)), (15,120))
            surface.blit(pg.transform.scale(second_spaceship, (60,48)), (15,220))
            surface.blit(pg.transform.scale(brown_asteroid, (60,48)), (15,320))

            # Show instructions for first player
            surface.blit(font.render("Press R1 to fire.", True, (255,0,0), None), (80, 134))
            surface.blit(font.render("Move the left joystick to move left and right.", True, (255,0,0), None), (80, 154))

            # Show instructions for second player
            surface.blit(font.render("Press L1 to fire.", True, (51,51,255), None), (80, 234))
            surface.blit(font.render("Move the right joystick to move left and right.", True, (51,51,255), None), (80, 254))

            # Show instructions for destroying asteroids
            surface.blit(font.render("Destroy asteroids to upgrade your spaceship.", True, (0,0,0), None), (80, 334))
            surface.blit(font.render("The upgrades are random.", True, (0,0,0), None), (80, 354))
            
            
            # Show exit button
            exit = Menu_Button(pg.image.load("Fonts/Quit_Rect.png"), (400, 550), "EXIT", self.get_font(35), (215, 252, 212), (0, 0, 0))

            # Exit button functionality
            exit.changeColor(guide_mouse_pos)
            exit.update(surface)

            # Check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if exit.checkForInput(guide_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        return

            pg.display.update()

# Player_Option class
# This class allows the user to choose the player(first player, second player)
class Player_Option:
    def __init__(self) -> None:
         pass

    def get_font(self, size): 
        return pg.font.Font("Fonts/font.ttf", size)

    
    def show_player_option(self):
        # Initialize pygame, set dimentions and title
        pg.init()
        surface = pg.display.set_mode((800, 600))
        pg.display.set_caption("Space Arcade")

        # Background image
        background_image = pg.image.load("Background/Space.png").convert()


        while True:
            surface.blit(background_image, (0, 0))

            menu_mouse_pos = pg.mouse.get_pos()

            # Create menu text
            menu_text = self.get_font(45).render("CHOOSE PLAYER", True, (182, 143, 64))
            menu_rect = menu_text.get_rect(center=(400, 50))

            # Create buttons
            first_player = Menu_Button(pg.image.load("Fonts/Multiplayer_Rect.png"), (400, 150), "FIRST PLAYER", self.get_font(35), (215, 252, 212), (255, 0, 0))

            second_player = Menu_Button(pg.image.load("Fonts/Singleplayer_Rect.png"), (400, 250), "SECOND PLAYER", self.get_font(35), (215, 252, 212), (51, 51, 255))

            exit = Menu_Button(pg.image.load("Fonts/Quit_Rect.png"), (400, 350), "EXIT", self.get_font(35), (215, 252, 212), (0, 0, 0))

            surface.blit(menu_text, menu_rect)

            # Update the buttons and change their color au user hovers over them
            for button in [first_player, second_player, exit]:
                button.changeColor(menu_mouse_pos)
                button.update(surface)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # First player
                    if first_player.checkForInput(menu_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        pg.mixer.music.stop()
                        singleplayer = Single_Player.SinglePlayer("First_Player")
                        singleplayer.run_game()
                    # Seond player
                    if second_player.checkForInput(menu_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        pg.mixer.music.stop()
                        singleplayer = Single_Player.SinglePlayer("Second_Player")
                        singleplayer.run_game()
                    # Exit
                    if exit.checkForInput(menu_mouse_pos):
                        pg.mixer.Sound('Sounds/Menu_Selection_Click.wav').play()
                        return

            pg.display.update()

    


# Main -----------------------------------------
if __name__ == "__main__":
    menu = Menu()
    menu.show_menu()
        