import sys
import pygame as pg
import random
import json
from First_Player_Bullets import First_Player_Bullets as bfp
from Menu import Menu
from Second_Player_Bullets import Second_Player_Bullets as bsp
from Asteroid import Asteroid


def check_events(screen, ship_first_player, ship_second_player, first_player_bullets, second_player_bullets, 
                play_button, scoreboard, asteroids, analog_keys, bullet_sound, exit_button):

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(mouse_x, mouse_y, play_button, ship_first_player, ship_second_player, first_player_bullets, 
            second_player_bullets, scoreboard, asteroids)
            check_exit_button(mouse_x, mouse_y, exit_button)


        # Controller joy button
        if event.type == pg.JOYBUTTONDOWN and play_button.running_state:
            # First player bullet control
            if event.button == 5 and event.joy == 0:
                if len(first_player_bullets) < ship_first_player.bullets_allowed:
                        bullet_sound.play()
                        new_bullet = bfp(screen, ship_first_player)
                        first_player_bullets.add(new_bullet)
                
            # Second player bullet control
            if event.button == 4 and event.joy == 1:
                if len(second_player_bullets) < ship_second_player.bullets_allowed:
                        bullet_sound.play()
                        new_bullet = bsp(screen, ship_second_player)
                        second_player_bullets.add(new_bullet)
                        
                    


        # Controller joy axis motion movement
        if event.type == pg.JOYAXISMOTION:
            analog_keys[event.axis] = event.value
            
            # Controller movement for the second player
            if event.joy == 1 and event.axis == 4:
                if analog_keys[4] < -.1:
                    ship_second_player.left_movement = True
                else:
                    ship_second_player.left_movement = False

                if analog_keys[4] > .1:
                    ship_second_player.right_movement = True
                else:
                    ship_second_player.right_movement = False
            
            # Controller movement for the second player
            if event.joy == 0 and event.axis == 0:
                if analog_keys[0] < -.1:
                    ship_first_player.left_movement = True
                else:
                    ship_first_player.left_movement = False

                if analog_keys[0] > .1:
                    ship_first_player.right_movement = True
                else:
                    ship_first_player.right_movement = False

        #------------------ Uncomment if you want to play the game with keyboard buttons ---------------------
        # Ship movement functionalities
        """elif event.type == pg.KEYDOWN:

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
                ship_first_player.right_movement = False"""

        

        

def update_screen(screen, ship_first_player, ship_second_player, bgi, first_player_bullets, 
                    second_player_bullets, play_button, scoreboard, asteroids, exit_button):
    # Render background image
    screen.blit(bgi, (0, 0))

    # Show the first ship
    ship_first_player.blitme()

    # Show the second ship
    ship_second_player.blitme()

    # Draw asteroids on the screen
    asteroids.draw(screen)

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
        play_button.draw_button()
        exit_button.draw_button()
        scoreboard.show_winner()

    # Show the most recent screen updates
    pg.display.flip()


def upgrade_ship(ship, asteroid, scoreboard, player):

    # Speed factor upgrade
    if asteroid.asteroid_code == 1:
        if asteroid.life > 8:
            ship.bullet_speed_factor += 2
        else:
            ship.bullet_speed_factor += 1

    # Bullet width upgrade
    elif asteroid.asteroid_code == 2:
        if asteroid.life > 8:
            ship.bullet_width += 2
        else:
            ship.bullet_width += 1

    # Bullets allowed upgrade
    elif asteroid.asteroid_code == 3:
        if asteroid.life > 8:
            ship.bullets_allowed += 2
        else:
            ship.bullets_allowed += 1

    # Life reduction upgrade
    elif asteroid.asteroid_code == 4:
        if asteroid.life > 8:
            ship.life_reduction += 2
        else:
            ship.life_reduction += 1

    # Life upgrade
    elif asteroid.asteroid_code == 5:
        if asteroid.life > 8:
            if player == 1:
                scoreboard.first_player_life += 20
            else:
                scoreboard.second_player_life += 20
        else:
            if player == 1:
                scoreboard.first_player_life += 10
            else:
                scoreboard.second_player_life += 10
        

        scoreboard.prepare_HP()

# Update the player score
def update_players_score(winner, ai_player=False):
    # Get players score from json file
    players_score = {}
    with open("Players_Score.json", "r") as f:
            players_score = json.load(f)

    # Update the Wins and Losses 
    if winner == -1:
        if not ai_player:
            players_score["Second_Player"]["Wins"] += 1
            players_score["First_Player"]["Losses"] += 1
    else:
        players_score["Second_Player"]["Losses"] += 1
        players_score["First_Player"]["Wins"] += 1

    # Update the json file
    with open("Players_Score.json", "w") as f:
        json.dump(players_score, f)

# Bullet - Ship Collisions ----------------------------------------------------------------------------------

def check_first_ship_collision(first_ship, second_ship_bullets, scoreboard, play_button, second_ship, hit_sound, ai_player):

    collided_bullet = pg.sprite.spritecollideany(first_ship, second_ship_bullets)

    # If a bullet has collided with the first ship
    if collided_bullet:
        hit_sound.play()
        second_ship_bullets.remove(collided_bullet) # Remove the bullet from the group
        scoreboard.first_player_life -= second_ship.life_reduction   # Reduce ship's life by one
        if(scoreboard.first_player_life <= 0):
            play_button.running_state = False
            scoreboard.second_player_score += 1
            scoreboard.winner = -1
            scoreboard.prepare_winner_message() # Update the winner
            scoreboard.prepare_Score()  # Update the score
            update_players_score(scoreboard.winner)  # Update the score stored in the json file
            return
        scoreboard.prepare_HP()    # Update the HP
       


def check_second_ship_collision(second_ship, first_ship_bullets, scoreboard, play_button, first_ship, hit_sound):

    collided_bullet = pg.sprite.spritecollideany(second_ship, first_ship_bullets)
    
    # If a bullet has collided with the second ship
    if collided_bullet:
        hit_sound.play()
        first_ship_bullets.remove(collided_bullet)  # Remove the bullet from the group
        scoreboard.second_player_life -= first_ship.life_reduction   # Reduce ship's life by one
        if(scoreboard.second_player_life <= 0):
            play_button.running_state = False  
            scoreboard.first_player_score += 1
            scoreboard.winner = 1
            scoreboard.prepare_winner_message() # Winner the winner
            scoreboard.prepare_Score()  # Update the score
            update_players_score(scoreboard.winner) # Update the score stored in the json file
            return 
        scoreboard.prepare_HP()    # Update the HP


 
# Bullet - Alien Collisions ---------------------------------------------------------------------------

def check_first_ship_bullet_asteroid_collision(first_ship_bullets, asteroids, first_ship, scoreboard, asteroid_sound):

    collision = pg.sprite.groupcollide(first_ship_bullets, asteroids, True, False)

    # If an asteroid has collided with a bullet
    if collision:

        # Get the collided asteroid
        collided_asteroid = collision[list(collision.keys())[0]][0]

        # Reduce it's life by the spaceship's life reduction value
        collided_asteroid.life -= first_ship.life_reduction

        # If the collided asteroid's life reaches below zero remove it from the group of asteroids
        if collided_asteroid.life <= 0:
            asteroid_sound.play()
            upgrade_ship(first_ship, collided_asteroid, scoreboard, 1)
            asteroids.remove(collided_asteroid)
            
        

        

def check_second_ship_bullet_asteroid_collision(second_ship_bullets, asteroids, second_ship, scoreboard, asteroid_sound):

    collision = pg.sprite.groupcollide(second_ship_bullets, asteroids, True, False)

    # If an asteroid has collided with a bullet
    if collision:

        # Get the collided asteroid
        collided_asteroid = collision[list(collision.keys())[0]][0]

        # Reduce it's life by the spaceship's life reduction value
        collided_asteroid.life -= second_ship.life_reduction

        # If the collided asteroid's life reaches below zero remove it from the group of asteroids
        if collided_asteroid.life <= 0:
            asteroid_sound.play()
            upgrade_ship(second_ship, collided_asteroid, scoreboard, 2)
            asteroids.remove(collided_asteroid)
            
            



def check_play_button(mouse_x, mouse_y, play_button, ship_first_player, ship_second_player, 
                     bulletsFirstPlayer, bulletsSecondPlayer, scoreboard, asteroids):

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
        ship_first_player.initial_life = 10
        ship_first_player.life_reduction = 1

        # Set second ship utilities
        ship_second_player.speed_factor = 1.5
        ship_second_player.bullet_speed_factor = 1
        ship_second_player.bullet_width = 3
        ship_second_player.bullet_height = 15
        ship_second_player.bullets_allowed = 3
        ship_second_player.initial_life = 10
        ship_second_player.life_reduction = 1

        # Empty the bullets group
        bulletsFirstPlayer.empty()
        bulletsSecondPlayer.empty()

        # Empty the alien group
        asteroids.empty()

        # Center both ships
        ship_first_player.center_ship()
        ship_second_player.center_ship()

        # Update the score
        scoreboard.second_player_life = ship_second_player.initial_life
        scoreboard.first_player_life = ship_first_player.initial_life
        scoreboard.prepare_HP()


def check_exit_button(mouse_x, mouse_y, exit_button):
    button_clicked = exit_button.rect.collidepoint(mouse_x, mouse_y)
    # If the exit button is clicked and the game has not started
    if button_clicked:
        menu = Menu()
        menu.show_menu()



def create_fleet(screen, asteroids):
    # Each time a new fleet of aliens is created, a random number of asteroids is choosen
    number_aliens_x = random.randint(1, 9)

    available_alien_y_positions = [80, 140, 200, 260, 320, 380, 440, 500, 560]
    available_alien_x_positions = [1260,-60, 1320, -120, 1380, -180, 1440, -240, 1500]
    
    
    # Create 'number_aliens_x' aliens 
    for i in range(number_aliens_x):
        # Choose a random index from available alien positions
        random_index_y = random.randint(0,(8-i))
        random_index_x = random.randint(0,(8-i))
        
        alien_y_pos = available_alien_y_positions[random_index_y]
        alien_x_pos = available_alien_x_positions[random_index_x]


        # Create an alien
        asteroid = Asteroid(screen, alien_x_pos, alien_y_pos)

        # Remove alien from available positions
        available_alien_y_positions.remove(alien_y_pos)
        available_alien_x_positions.remove(alien_x_pos)

        asteroids.add(asteroid)       # Add each alien to the group of aliens

def update_asteroids(asteroids):
    asteroids.update()
