import pygame

TITLE = "Game"
FPS = 60
HEIGHT = 720
WIDTH = 1280

PLAYER_GRAV = 0.8
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12

tlo = pygame.image.load('tlo.PNG')
player_right = pygame.image.load('right.PNG')
player_left = pygame.image.load('left.PNG')

TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

player_width = player_right.get_width()
player_height = player_right.get_height()

PLAYER_HIT_BOX = pygame.Rect(0, 0, player_width, player_height)
