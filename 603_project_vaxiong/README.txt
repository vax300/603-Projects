'''
603 Final Project from Va Xiong
PING PONG GAME with visuals, music and sound effects.

This project is based on a Ping Pong Game code using pygame installation. I refactored and modified this code by using
a few existing ping pong examples. There are many tutorials and similar coding they all use in python and with pygame.

This ping pong game code uses classes to define certain parts of this game, 
where it has a def functions to operate objects and variables. For example: ball has movement and speed,
the ball can reset when it scores, makes sounds if hitting walls or paddle. Makes sound when a player scores.

This project is mostly involves with the visuals and sounds. Using background images, sprites, music and sound effects.
There are codes which involves image, text and sound files. The files are in a respective folder for path.

For images they come in a code:  pygame.image.load('folder/filename').
For music and sound effects in code:  pygame.mixer.Sound("folder/filename")
For text fonts come in code: pygame.font.Font('folder/filename')

How to play this game:

1) Click the file PINGPONG.py and run it, it will start the game
2) The game will start and a timer will count down
3) You are playing as the paddle on the right, you can move up and down
4) You can score points by blocking the ball which will bounce on the opposite side
5) The opponent AI will attempt to counter block the ball to your side
6) There is no working code for a menu or a game over screen

You can press the ESC key anytime to exit the game or close the window/program.

This code can be refactored and enhanced for future projects.

Thanks for playing!
'''