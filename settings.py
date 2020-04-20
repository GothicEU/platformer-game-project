import pygame

TITLE = "Game"
FPS = 60
HEIGHT = 720
WIDTH = 1280

PLAYER_HEALTH = 100
PLAYER_GRAV = 0.9
PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.12
PLAYER_ACC_PRZYKUC = 0.2
MOB_ACC = 0.8
ZOMBIE_ACC = 0.5

WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
display = pygame.Surface((640, 360))

TILESIZE = 32

PLAYER_HIT_BOX = pygame.Rect(0, 0, 25, 64)
PLAYER_HIT_BOX_PRZYKUC = pygame.Rect(0, 0, 25, 32)

MOB_HIT_BOX = pygame.Rect(0, 0, 28, 26)

ZOMBIE_HIT_BOX = pygame.Rect(0, 0, 32, 64)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)