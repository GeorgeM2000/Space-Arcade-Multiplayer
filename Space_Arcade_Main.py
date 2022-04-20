# Libraries ----------------------------------------------
import random
import pygame as pg
import Game_Functions as gf
import serial.tools.list_ports 
import sys
import os
from Spaceship_First_Player import Spaceship_First_Player
from Spacehip_Second_Player import Spaceship_Second_Player
from First_Player_Bullets import First_Player_Bullets as bfp
from Second_Player_Bullets import Second_Player_Bullets as bsp
from Start_Button import StartButton as sb
from Scoreboard import Scoreboard
from pygame.sprite import Group
    


def run_game():
    pg.init()
    surface = pg.display.set_mode((1200,700))
    pg.display.set_caption("Space Arcade")

    # Pygame Groups
    first_spaceship_bullets = Group()
    second_spaceship_bullets = Group()
    aliens = Group()

    # Create the fleet of aliens
    gf.create_fleet(surface, aliens)

    # Create a play button
    play_button = sb(surface, "Play")


    # Start alien sideway movement timer
    alien_movement_timer = pg.time.get_ticks()
    alien_movement_time_range = list(range(1, 6))      # In milliseconds e.g 1 millisec, 2 millisec

    # Fleet of aliens creation time range
    fleet_aliens_timer = pg.time.get_ticks()
    fleet_aliens_time_range = [time for time in range(20000, 120001, 5000)]


    # Uncomment to enable Accelerometer input data
    """ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial()

    portVariable = "COM" + str(3)

    serialInst.baudrate = 115200
    serialInst.port = portVariable
    serialInst.open()

    user_movement = 0.0"""

    # Background color
    background_color = (230, 230, 230)
    
    # Create two players
    ship_first_player = Spaceship_First_Player(surface)
    ship_second_player = Spaceship_Second_Player(surface)

    # Create a scoreboard
    scoreboard = Scoreboard(surface, ship_first_player, ship_second_player)


    while True:

        # If the game starts
        if play_button.running_state:

            # Uncomment to enable Accelerometer control
            """if serialInst.in_waiting:
                packet = serialInst.readline()
                user_movement = float(packet.decode("utf"))

            if user_movement < 0.0:
                if user_movement >= -0.20:
                    ship_first_player.left_movement = False
                    ship_first_player.right_movement = False
                else:
                    ship_first_player.speed_factor = 1
                    ship_first_player.left_movement = True

            elif user_movement > 0.0:
                if user_movement <= 0.20:
                    ship_first_player.left_movement = False
                    ship_first_player.right_movement = False
                else:
                    ship_first_player.speed_factor = 1
                    ship_first_player.right_movement = True
            """

            # Update for Aliens
            if (pg.time.get_ticks() - alien_movement_timer) > alien_movement_time_range[random.randint(0,4)]:
                alien_movement_timer = pg.time.get_ticks()
                gf.update_aliens(aliens)

            # Create fleet of aliens 
            if pg.time.get_ticks() - fleet_aliens_timer > fleet_aliens_time_range[random.randint(0,len(fleet_aliens_time_range)-1)]:
                fleet_aliens_timer = pg.time.get_ticks()
                gf.create_fleet(surface, aliens)
            
            # Updates for ships
            ship_first_player.update() 
            ship_second_player.update()

            # Check for ship-bullet collisions
            gf.check_first_ship_collision(ship_first_player, second_spaceship_bullets, scoreboard, play_button, ship_second_player)
            gf.check_second_ship_collision(ship_second_player, first_spaceship_bullets, scoreboard, play_button, ship_first_player)

        
            # Check for bullet-alien collisions
            gf.check_first_ship_bullet_alien_collision(first_spaceship_bullets, aliens, ship_first_player, scoreboard)
            gf.check_second_ship_bullet_alien_collision(second_spaceship_bullets, aliens, ship_second_player, scoreboard)

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
            

            # Get rid of aliens that have disappeared
            for alien in aliens.copy():
                if alien.alien_right_movement and alien.rect.x > 1200:
                    aliens.remove(alien)
                elif alien.alien_left_movement and alien.rect.x < 0:
                    aliens.remove(alien)


        # Check for events 
        gf.check_events(surface, ship_first_player, ship_second_player, first_spaceship_bullets, 
                        second_spaceship_bullets, play_button, scoreboard, aliens)


        # Update the screen
        gf.update_screen(surface, ship_first_player, ship_second_player, background_color, first_spaceship_bullets, 
                        second_spaceship_bullets, play_button, scoreboard, aliens)


# Main --------------------------------
if __name__ == "__main__":
    run_game()

