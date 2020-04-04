import pygame

TITLE = "Game"
FPS = 40
HEIGHT = 720
WIDTH = 1280

PLAYER_GRAV = 0.8
PLAYER_ACC = 0.5
PLAYER_ACC_PRZYKUC = 0.2
PLAYER_FRICTION = -0.12

WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE,pygame.FULLSCREEN)
display = pygame.Surface((600, 400))

tlo = pygame.image.load('tlo.PNG')
player_right = pygame.image.load('right.PNG')
player_left = pygame.image.load('left.PNG')
player_crouch = pygame.image.load('crouch.PNG')
player_image = player_right

TILESIZE = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

player_width = player_image.get_width()
player_height = player_image.get_height()

PLAYER_HIT_BOX = pygame.Rect(0, 0, player_width, player_height)
PLAYER_HIT_BOX_PRZYKUC = pygame.Rect(0, 0, player_width, player_height / 2)
