import random
from time import time
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

class SinglePlayer:

    def __init__(self) -> None:
        pass
        

    # Function to choose the closest alien based on their y value
    def get_asteroid_target(self, asteroids):
        closest_asteroid = asteroids.sprites()[0]
        for i in range(1, len(asteroids)):
            if asteroids.sprites()[i].rect.y < closest_asteroid.rect.y:
                closest_asteroid = asteroids.sprites()[i]

        return closest_asteroid

    # Function to fire bullet
    def fire_bullet(self, second_player_bullets, ship_second_player, bullet_sound, screen, firing_frequency):
        if random.random() < firing_frequency:
            if len(second_player_bullets) < 1:
                bullet_sound.play()
                new_bullet = bsp(screen, ship_second_player)
                second_player_bullets.add(new_bullet)

    # Calculate distance between the A.I spaceship and the alien
    def calculate_distance(self, ship_second_player, target, average_loop_cycle):
        return (ship_second_player.rect.x - target.rect.x) / (1.0 / average_loop_cycle)

    # Function to target the alien
    def target_asteroid(self, ship_second_player, target, BLC, second_spaceship_bullets, bullet_sound, surface, firing_frequency, average_loop_cycle):

        # If the x position of the A.I spaceship is greater than the x position of the alien's spaceship
        # and the alien target is moving right 
        if target.asteroid_right_movement:

            # If the distance between the alien and the A.I spaceship is greater than the bullet loop cycle plus the width of the alien image
            # then move left
            if self.calculate_distance(ship_second_player, target, average_loop_cycle) > BLC + 5.0:
                ship_second_player.left_movement = True
                ship_second_player.right_movement = False

            # Similarly if it is less that the bullet loop cycle, move right
            elif self.calculate_distance(ship_second_player, target, average_loop_cycle) < BLC :# -60.0: 
                ship_second_player.left_movement = False
                ship_second_player.right_movement = True

            # Else, stop moving and fire bullets
            elif BLC <= self.calculate_distance(ship_second_player, target, average_loop_cycle) <= BLC + 5.0:
                ship_second_player.left_movement = False
                ship_second_player.right_movement = False
                self.fire_bullet(second_spaceship_bullets, ship_second_player, bullet_sound, surface, firing_frequency)

        # If the x position of the A.I spaceship is less than the x position of the alien's spaceship
        # and the alien target is moving left 
        elif target.asteroid_left_movement:
            # If the distance between the alien and the A.I spaceship is greater than the bullet loop cycle plus the width of the alien image
            # then move left
            if self.calculate_distance(ship_second_player, target, average_loop_cycle) < -(BLC):
                ship_second_player.left_movement = False
                ship_second_player.right_movement = True

            # Similarly if it is less that the bullet loop cycle, move right
            elif self.calculate_distance(ship_second_player, target, average_loop_cycle) > -(BLC - 10.0):
                ship_second_player.left_movement = True
                ship_second_player.right_movement = False

            # Else, stop moving and fire bullets
            elif -(BLC - 5.0) <= self.calculate_distance(ship_second_player, target, average_loop_cycle) <= -(BLC - 10.0):
                ship_second_player.left_movement = False
                ship_second_player.right_movement = False
                self.fire_bullet(second_spaceship_bullets, ship_second_player, bullet_sound, surface, firing_frequency)

    # Function to target the player
    def target_player(self, ship_second_player, target, right_movement_freq, left_movement_freq, second_spaceship_bullets, bullet_sound, surface, firing_frequency):

        
        # If the x position of the player's spaceship is greater than the x position of the A.I spaceship
        # and a random number is less than a frequency, then start moving right
        if ship_second_player.rect.x < target.rect.x and random.random() < right_movement_freq:
            ship_second_player.right_movement = True
            ship_second_player.left_movement = False
            
        # Similarly if the conditions are met, start moving left
        elif ship_second_player.rect.x > target.rect.x and random.random() < left_movement_freq:
            ship_second_player.left_movement = True
            ship_second_player.right_movement = False

        # If the two spaceships are on the same position, stop moving
        elif ship_second_player.rect.x == target.rect.x:
            ship_second_player.left_movement = False
            ship_second_player.right_movement = False
        
        self.fire_bullet(second_spaceship_bullets, ship_second_player, bullet_sound, surface, firing_frequency)
                
            
    # Function to move the spaceship depending on the target
    def move_spaceship(self, ship_second_player, ship_first_player, left_movement_freq, right_movement_freq, target_aquired, target_asteroid, 
                        asteroids, second_spaceship_bullets, bullet_sound, surface, firing_frequency, average_loop_cycle):

        # If target is aquired and there are aliens on the screen
        if target_aquired and len(asteroids):
            # Set alien as the target
            target = target_asteroid

            # Begin moving accordingly to destroy the targeted alien
            self.target_asteroid(ship_second_player, target, (target_asteroid.rect.y / float(ship_second_player.bullet_speed_factor)), second_spaceship_bullets, bullet_sound, surface, firing_frequency, average_loop_cycle[target_asteroid.asteroid_x])

        # If the target is not aquired
        else:
            # Set player ship as the target
            target = ship_first_player

            # begin moving accordingly to destroy the targeted player
            self.target_player(ship_second_player, target, right_movement_freq, left_movement_freq, second_spaceship_bullets, bullet_sound, surface, firing_frequency)


    def run_game(self):
        pg.init()
        surface = pg.display.set_mode((1200,700))
        pg.display.set_caption("Space Arcade")

        # Pygame Groups
        first_spaceship_bullets = Group()
        second_spaceship_bullets = Group()
        asteroids = Group()

        # Create the fleet of asteroids
        gf.create_asteroids(surface, asteroids)

        # Create a play button
        play_button = sb(surface, "Play")

        # Create an exit button
        exit_button = eb(surface, "Exit")


        # Start alien sideway movement timer
        asteroid_movement_timer = pg.time.get_ticks()
        asteroid_movement_time_range = 2.0      # In milliseconds e.g 1 millisec, 2 millisec
        

        # Fleet of aliens creation time range
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

        # Target settings
        target_aquired = False
        target_asteroid = None

        # Set loop cycles
        loop_cycles = {
            1260: 2.9820702262315426,
            -60: 3.4154639175257726,
            1320: 2.9820702262315426,
            -120: 3.0514761544284634,
            1380: 2.9820702262315426,
            -180: 4.02896451846488,
            1440: 2.9820702262315426,
            -240: 3.612421929215822,
            1500: 2.9820702262315426 
        }

        while True:

            # If the game starts
            if play_button.running_state:
                

                # Create fleet of aliens 
                if pg.time.get_ticks() - fleet_asteroids_timer > fleet_asteroids_time_range[random.randint(0,len(fleet_asteroids_time_range)-1)]:
                    fleet_asteroids_timer = pg.time.get_ticks()
                    gf.create_asteroids(surface, asteroids)
                
                # Updates for ships
                ship_first_player.update() 
                ship_second_player.update()

                # Check for ship-bullet collisions
                gf.check_first_ship_collision(ship_first_player, second_spaceship_bullets, scoreboard, play_button, ship_second_player, hit_sound, True)
                gf.check_second_ship_collision(ship_second_player, first_spaceship_bullets, scoreboard, play_button, ship_first_player, hit_sound)

            
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
                

                for asteroid in asteroids.copy():

                    if (pg.time.get_ticks() - asteroid_movement_timer) > asteroid_movement_time_range:
                        asteroid_movement_timer = pg.time.get_ticks()
                        gf.update_asteroids(asteroids)

                    # Get rid of aliens that have disappeared
                    if asteroid.asteroid_right_movement and asteroid.rect.x > 1200:
                        asteroids.remove(asteroid)
                

                    elif asteroid.asteroid_left_movement and asteroid.rect.x < 0:
                        asteroids.remove(asteroid)                        

                    
                    # Check if target is aquired and there are alien on the screen
                    if not target_aquired and len(asteroids):
                        # Get random target alien
                        target_asteroid = self.get_asteroid_target(asteroids)
                        target_aquired = True
                    elif target_aquired:
                        if not target_asteroid in asteroids:
                            target_aquired = False
                            target_asteroid = None

                # Firing the A.I spaceship is dependent on the A.I spaceship's movement
                self.move_spaceship(ship_second_player, ship_first_player, 0.1, 0.1, target_aquired, target_asteroid, asteroids, second_spaceship_bullets, bullet_sound, surface, 0.2, loop_cycles)


            # Check first player events 
            gf.check_events(surface, ship_first_player, ship_second_player, first_spaceship_bullets, 
                            second_spaceship_bullets, play_button, scoreboard, asteroids, analog_keys, bullet_sound, exit_button)


            # Update the screen
            gf.update_screen(surface, ship_first_player, ship_second_player, background_image, first_spaceship_bullets, 
                            second_spaceship_bullets, play_button, scoreboard, asteroids, exit_button)
            
            
    

        