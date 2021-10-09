# Space Arcade Multiplayer
 A space arcade multiplayer game inspired by Eric Matthes's alien invasion game. 
 This game is played by two players. One player uses an Arduino Nano 33 BLE Sense 
 Accelerometer to read X and Y coordinates to move the spaceship. The other player
 uses the left and right arrow keys to move the spaceship. 
 The two players can shoot aliens that appear on the screen to upgrade their spaceship.
 The game is over once a player's life has reached below zero.

# Requirements
- Python (I use 3.8.5 version)
- Pygame (I use 1.9.6 version)
- Arduino IDE
- Arduino Nano 33 BLE Sense

# Usage 
Both players can play the game using buttons or one of the players can use the 
Arduino Nano 33 Nano BLE Sense accelerometer capabilities. To enable accelerometer
uncomment the specified code in the 'Space_Arcade_Main.py', comment the if and 
elif block in the 'Game_Functions.py' and uncomment the code in the 'Spaceship_First_Player.py'.
Connect the Arduino Nano 33 BLE Sense in your computer, start Arduino IDE and then 
open the serial monitor. In the serial monitor press 's' to start reading data and 'e'
to stop. Close the serial monitor window and run 'Space_Arcade_Main.py'.
The accelerometer capabilities are disabled by default.
