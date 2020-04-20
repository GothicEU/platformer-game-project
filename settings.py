import pygame

TITLE = "Game"
FPS = 60
HEIGHT = 720
WIDTH = 1280

PLAYER_HEALTH = 100
PLAYER_GRAV = 0.8
PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.12
PLAYER_ACC_PRZYKUC = 0.2

MOB_SPEED = 10
MOB_HIT_BOX = pygame.Rect(0, 0, 35, 35)

WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
display = pygame.Surface((600, 400))

tlo = pygame.image.load('tlo.png')
player_right = pygame.image.load('right.png')
player_left = pygame.image.load('left.png')
player_crouch_right = pygame.image.load('crouch_right.png')
player_crouch_left = pygame.image.load('crouch_left.png')
player_image = player_right

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

player_width = player_right.get_width()
player_height = player_right.get_height()

PLAYER_HIT_BOX = pygame.Rect(0, 0, player_width, player_height)
PLAYER_HIT_BOX_PRZYKUC = pygame.Rect(0, 0, player_width, player_height / 2)

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)