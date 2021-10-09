import sys
import pygame as pg
import random
from First_Player_Bullets import First_Player_Bullets as bfp
from Second_Player_Bullets import Second_Player_Bullets as bsp
from Alien import Alien


def check_events(screen, ship_first_player, ship_second_player, first_player_bullets, second_player_bullets, 
                play_button, scoreboard, aliens):

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(mouse_x, mouse_y, play_button, ship_first_player, ship_second_player, first_player_bullets, 
            second_player_bullets, scoreboard, aliens)


        # Ship movement functionalities
        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_RIGHT:
                ship_second_player.right_movement = True

            elif event.key == pg.K_LEFT:
                ship_second_player.left_movement = True

            if event.key == pg.K_a:
                ship_first_player.left_movement = True

            elif event.key == pg.K_d:
                ship_first_player.right_movement = True            

            if event.key == pg.K_SPACE and play_button.running_state:
                if len(second_player_bullets) < ship_second_player.bullets_allowed:
                    new_bullet = bsp(screen, ship_second_player)
                    second_player_bullets.add(new_bullet)

            if event.key == pg.K_w and play_button.running_state:
                if len(first_player_bullets) < ship_first_player.bullets_allowed:
                    new_bullet = bfp(screen, ship_first_player)
                    first_player_bullets.add(new_bullet)

        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                ship_second_player.right_movement = False

            elif event.key == pg.K_LEFT:
                ship_second_player.left_movement = False

            elif event.key == pg.K_a:
                ship_first_player.left_movement = False

            elif event.key == pg.K_d:
                ship_first_player.right_movement = False

def update_screen(screen, ship_first_player, ship_second_player, bgc, first_player_bullets, 
                    second_player_bullets, play_button, scoreboard, aliens):
    # Fill the screen with background color
    screen.fill(bgc)

    # Show the first ship
    ship_first_player.blitme()

    # Show the second ship
    ship_second_player.blitme()

    # Draw Aliens on the screen
    aliens.draw(screen)

    # Show score
    scoreboard.show_score()

    # Drawing bullets for the first ship
    for firstPlayerBullet in first_player_bullets.sprites():
        firstPlayerBullet.draw_bullet()

    # Drawing bullets for the first ship
    for secondPlayerBullet in second_player_bullets.sprites():
        secondPlayerBullet.draw_bullet()

    # Draw play button if game state is false
    if not play_button.running_state:
        play_button.draw_button(play_button.running_state)

    # Show the most recent screen updates
    pg.display.flip()


def upgrade_ship(ship, alien_life, scoreboard, player):
    random_upgrade = random.randint(1, 6)

    # Speed factor upgrade
    if random_upgrade == 1:
        if alien_life > 9:
            ship.bullet_speed_factor += 2
        else:
            ship.bullet_speed_factor += 1
    # Bullet width upgrade
    elif random_upgrade == 2:
        if alien_life > 9:
            ship.bullet_width += 2
        else:
            ship.bullet_width += 1
    # Bullets allowed upgrade
    elif random_upgrade == 3:
        if alien_life > 9:
            ship.bullets_allowed += 2
        else:
            ship.bullets_allowed += 1
    # Life reduction upgrade
    elif random_upgrade == 4:
        if alien_life > 9:
            ship.life_reduction += 2
        else:
            ship.life_reduction += 1
        print("Life Reduction", ship.life_reduction)
    # Life upgrade
    elif random_upgrade == 5:
        if alien_life > 9:
            if player == 1:
                scoreboard.first_player_life += 20
            else:
                scoreboard.second_player_life += 20
        else:
            if player == 1:
                scoreboard.first_player_life += 10
            else:
                scoreboard.second_player_life += 10
        scoreboard.prep_score()
    

# Bullet - Ship Collisions ----------------------------------------------------------------------------------

def check_first_ship_collision(first_ship, second_ship_bullets, scoreboard, play_button, second_ship):

    collided_bullet = pg.sprite.spritecollideany(first_ship, second_ship_bullets)

    # If a bullet has collided with the ship
    if collided_bullet:
        second_ship_bullets.remove(collided_bullet) # Remove the bullet from the group
        scoreboard.first_player_life -= second_ship.life_reduction   # Reduce ship's life by one
        if(scoreboard.second_player_life <= 0):
            play_button.running_state = False
            return
        scoreboard.prep_score()    # Update the score
       


        

def check_second_ship_collision(second_ship, first_ship_bullets, scoreboard, play_button, first_ship):

    collided_bullet = pg.sprite.spritecollideany(second_ship, first_ship_bullets)
    
    # If a bullet has collided with the ship
    if collided_bullet:
        first_ship_bullets.remove(collided_bullet)  # Remove the bullet from the group
        scoreboard.second_player_life -= first_ship.life_reduction   # Reduce ship's life by one
        if(scoreboard.first_player_life <= 0):
            play_button.running_state = False  
            return 
        scoreboard.prep_score()    # Update the score


 
# Bullet - Alien Collisions ---------------------------------------------------------------------------

def check_first_ship_bullet_alien_collision(first_ship_bullets, aliens, first_ship, scoreboard):

    collision = pg.sprite.groupcollide(first_ship_bullets, aliens, True, False)

    # If an alien has collided with a bullet
    if collision:
        collided_alien = collision[list(collision.keys())[0]][0]
        collided_alien.life -= first_ship.life_reduction
        if collided_alien.life <= 0:
            upgrade_ship(first_ship, collided_alien.life_initial_value, scoreboard, 1)
            aliens.remove(collided_alien)
            
        

        

def check_second_ship_bullet_alien_collision(second_ship_bullets, aliens, second_ship, scoreboard):

    collision = pg.sprite.groupcollide(second_ship_bullets, aliens, True, False)

    # If an alien has collided with a bullet
    if collision:
        collided_alien = collision[list(collision.keys())[0]][0]
        collided_alien.life -= second_ship.life_reduction
        if collided_alien.life <= 0:
            upgrade_ship(second_ship, collided_alien.life_initial_value, scoreboard, 2)
            aliens.remove(collided_alien)
            



def check_play_button(mouse_x, mouse_y, play_button, ship_first_player, ship_second_player, 
                     bulletsFirstPlayer, bulletsSecondPlayer, scoreboard, aliens):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # If the start button is clicked and the game has not started
    if button_clicked and not play_button.running_state:
        play_button.running_state = True

        # Set first ship utilities
        ship_first_player.speed_factor = None
        ship_first_player.bullet_speed_factor = 1
        ship_first_player.bullet_width = 3
        ship_first_player.bullet_height = 15
        ship_first_player.bullets_allowed = 3
        ship_first_player.initial_life = 100

        # Set second ship utilities
        ship_second_player.speed_factor = 1.5
        ship_second_player.bullet_speed_factor = 1
        ship_second_player.bullet_width = 3
        ship_second_player.bullet_height = 15
        ship_second_player.bullets_allowed = 3
        ship_second_player.initial_life = 100

        # Empty the bullets group
        bulletsFirstPlayer.empty()
        bulletsSecondPlayer.empty()

        # Empty the alien group
        aliens.empty()

        # Center both ships
        ship_first_player.center_ship()
        ship_second_player.center_ship()

        # Update the score
        scoreboard.second_player_life = ship_second_player.initial_life
        scoreboard.first_player_life = ship_first_player.initial_life
        scoreboard.prep_score()


def create_fleet(screen, aliens):
    # Each time a new fleet of aliens is created, a random number of aliens is choosen
    number_aliens_x = random.randint(1, 9)

    available_alien_positions = [80, 140, 200, 260, 320, 380, 440, 500, 560]

    # Create 'number_aliens_x' aliens 
    for i in range(number_aliens_x):
        random_index = random.randint(0,(8-i))
        alien_y_pos = available_alien_positions[random_index]
        alien = Alien(screen, [1260,-60, 1320, -120], alien_y_pos)
        available_alien_positions.remove(alien_y_pos)
        aliens.add(alien)       # Add each alien to the group of aliens

def update_aliens(aliens):
        aliens.update()
