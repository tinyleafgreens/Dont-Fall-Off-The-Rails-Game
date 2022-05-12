# Don't Fall Off The Rails! by Tinyleaf Greens #

<p align="center">
  <img src="https://user-images.githubusercontent.com/87482570/168091209-bbfac212-a413-4e03-84b6-c7dada0cef1b.jpg"/>
</p>

A simple, yet fun sidescrolling game based on my favorite cryptocurrency. The game respesents the ups and downs that the price of Algorand takes. In the background is the creator of Algorand, Turing-award winner, Silvio Micali. The goal of the game is to gather as many points as possible without completely falling off of the rails. You can hang off of the rails as you please, but if you go completely off the rails, you will lose a life and your avatar will reset. You will have three lives to do this after which, the game will be over and you'll recieve your final score. The game is scored by adding points for each rail, increasing point values with speed. How far can you go!?

This game was developed in Python using the PyGame module as a way to test out game logic development and quite frankly, have a bit of fun... 

## Controls ##
The gameplay is very simple. To get started, use the up, down, left and right arrow keys on your keyboard to control your avatar. When you fall off the rails, the avatar will reset and you'll be instructed to press any arrow key to continue. Once you've run out of lives you'll reach the game over screen. Press the space key to reset the game and play again!

## Running the Game ##

Currently, there are two ways to run the game. The game was designed to be played using option 1 (download and run in python interpreter), but it is possible to sample the game online using option 2 (repl.it). Option 2 will result in siginificanly worse performance, due to the nature of the method.

### Option 1: Download and Run in Python Interpreter (Preferred) ###

Ideally, you will be playing this on a desktop computer. In your terminal window, you should be able to clone this repository using the following command.

`git clone https://github.com/tinyleafgreens/Dont-Fall-Off-The-Rails-Game.git`

You'll need to have the PyGame module installed to play this, so if you don't already have it installed, use the following command to install it.

`pip install pygame`

Once you've cloned the repository and pip installed pygame, you should be able to play the game by changing the current directory to the repository directory and running the main file.

`cd Dont-Fall-Off-The-Rails-Game`

`python dfotr_game_main.py`

### Option 2: [Repl.it](https://replit.com/@tinyleafgreens/DontFallOffTheRailsGame#main.py "repl.it link") Online Version (Less Preferred) ###

This method will be much simpler to use, but will have poor performance and lag once the game gets going, due to limitations in processing and the required transfer of the pygame output to an HTML web browser user interface. It will, however, give you a good idea as to what the game looks like and could help you decide if you want to download/play it. To use this, go to the [**repl.it site**](https://replit.com/@tinyleafgreens/DontFallOffTheRailsGame#main.py "repl.it link"). 

The game size window is a set size, so to play you'll need to:
1. Ensure that your page zoom is set to 100% 
2. Click on the run button (this will show the game start page in the pygame window)
3. Ensure that you close or minimize the all windows (code/files/terminal) aside from the pygame window.
4. Once your window shows only the pygame screen, you should be good to play!
