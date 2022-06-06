import random
import pygame as pg
import json
import Game_Functions as gf
import os
from Spaceship_First_Player import Spaceship_First_Player
from Spacehip_Second_Player import Spaceship_Second_Player
from First_Player_Bullets import First_Player_Bullets as bfp
from Second_Player_Bullets import Second_Player_Bullets as bsp
from Start_Button import StartButton as sb
from Exit_Button import ExitButton as eb
from Scoreboard import Scoreboard
from pygame.sprite import Group
    
class MultiPlayer:
    def __init__(self) -> None:
        pass

    def run_game(self):
        pg.init()
        surface = pg.display.set_mode((1200,700))
        pg.display.set_caption("Space Arcade")

        # Pygame Groups
        first_spaceship_bullets = Group()
        second_spaceship_bullets = Group()
        asteroids = Group()
        explosions = Group()

        # Create the fleet of asteroids
        gf.create_asteroids(surface, asteroids)

        # Create a play button
        play_button = sb(surface, "Play")

        # Create an exit button
        exit_button = eb(surface, "Exit")


        # Start asteroid sideway movement timer
        asteroid_movement_timer = pg.time.get_ticks()
        asteroid_movement_time_range = list(range(1, 6))      # In milliseconds e.g 1 millisec, 2 millisec

        # Set of asteroids creation time range
        fleet_asteroids_timer = pg.time.get_ticks()
        fleet_asteroids_time_range = [time for time in range(20000, 120001, 5000)]

        # Background image
        background_image = pg.image.load("Background/Space.png").convert()
        
        # Create two players
        ship_first_player = Spaceship_First_Player(surface)
        ship_second_player = Spaceship_Second_Player(surface)

        # Create a scoreboard
        scoreboard = Scoreboard(surface, ship_first_player, ship_second_player)


        # Initialize controller
        joysticks = []
        for i in range(pg.joystick.get_count()):
            joysticks.append(pg.joystick.Joystick(i))
        for joystick in joysticks:
            joystick.init()

        with open(os.path.join("PS4_Keys.json"), 'r+') as file:
            button_keys = json.load(file)

        analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5:-1}


        # Initialize sound effects
        bullet_sound = pg.mixer.Sound('Sounds/laser1.wav')
        asteroid_sound = pg.mixer.Sound('Sounds/Explosion_02.wav')
        hit_sound = pg.mixer.Sound("Sounds/Hit_02.wav")


        while True:

            # If the game starts
            if play_button.running_state:

                # Create asteroids 
                if pg.time.get_ticks() - fleet_asteroids_timer > fleet_asteroids_time_range[random.randint(0,len(fleet_asteroids_time_range)-1)]:
                    fleet_asteroids_timer = pg.time.get_ticks()
                    gf.create_asteroids(surface, asteroids)
                
                # Updates for ships
                ship_first_player.update() 
                ship_second_player.update()

                # Check for ship-bullet collisions
                gf.check_first_ship_collision(ship_first_player, second_spaceship_bullets, scoreboard, play_button, ship_second_player, hit_sound, False, "", explosions)
                gf.check_second_ship_collision(ship_second_player, first_spaceship_bullets, scoreboard, play_button, ship_first_player, hit_sound, False, "", explosions)

            
                # Check for bullet-asteroid collisions
                gf.check_first_ship_bullet_asteroid_collision(first_spaceship_bullets, asteroids, ship_first_player, scoreboard, asteroid_sound)
                gf.check_second_ship_bullet_asteroid_collision(second_spaceship_bullets, asteroids, ship_second_player, scoreboard, asteroid_sound)

                # Updates for bullets
                first_spaceship_bullets.update()
                second_spaceship_bullets.update()


                # Get rid of bullets that have disappeared
                for firstPlayerBullet in second_spaceship_bullets.copy():
                    if firstPlayerBullet.rect.bottom >= 700:
                        second_spaceship_bullets.remove(firstPlayerBullet)


                for secondPlayerBullet in first_spaceship_bullets.copy():
                    if secondPlayerBullet.rect.bottom <= 0:
                        first_spaceship_bullets.remove(secondPlayerBullet)
                

                # Get rid of asteroids that have disappeared
                for asteroid in asteroids.copy():
                    # Update for asteroids
                    if (pg.time.get_ticks() - asteroid_movement_timer) > asteroid_movement_time_range[random.randint(0,4)]:
                        asteroid_movement_timer = pg.time.get_ticks()
                        gf.update_asteroids(asteroids)

                    if asteroid.asteroid_right_movement and asteroid.rect.x > 1200:
                        asteroids.remove(asteroid)

                    elif asteroid.asteroid_left_movement and asteroid.rect.x < 0:
                        asteroids.remove(asteroid)


            # Check for events 
            gf.check_events(surface, ship_first_player, ship_second_player, first_spaceship_bullets, 
                            second_spaceship_bullets, play_button, scoreboard, asteroids, analog_keys, bullet_sound, exit_button, False, "")


            # Update the screen
            gf.update_screen(surface, ship_first_player, ship_second_player, background_image, first_spaceship_bullets, 
                            second_spaceship_bullets, play_button, scoreboard, asteroids, exit_button, explosions, False, "")



