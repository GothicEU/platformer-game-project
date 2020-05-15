import pygame

TITLE = "Creeping Death"
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
MOB_HEALTH = 50
ZOMBIE_HEALTH = 100
FLYING_ACC = 0.5

WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
display = pygame.Surface((640, 360))

TILESIZE = 32

PLAYER_HIT_BOX = pygame.Rect(0, 0, 25, 64)
PLAYER_HIT_BOX_PRZYKUC = pygame.Rect(0, 0, 25, 32)

PLAYER_ATTACK_HIT_BOX = pygame.Rect(0, 0, 25, 64)

MOB_HIT_BOX = pygame.Rect(0, 0, 28, 26)

ZOMBIE_HIT_BOX = pygame.Rect(0, 0, 32, 64)

FLYING_HIT_BOX = pygame.Rect(0, 0, 64, 64)

ITEMS_HIT_BOX = pygame.Rect(0, 0, 32, 32)

ATTACK_HIT_BOX = pygame.Rect(0, 0, 45, 45)

heart = pygame.image.load('lives_icon.PNG')


BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (55, 208, 71)
YELLOW = (216, 222, 52)
