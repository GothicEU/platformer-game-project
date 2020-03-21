import pygame

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8

WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE,pygame.FULLSCREEN)
display = pygame.Surface((600, 400))
air_timer = 0
scroll = [0, 0]

# images

player_Right = pygame.image.load('right.PNG')
player_Left = pygame.image.load('left.PNG')
background = pygame.image.load('tlo.PNG')
grass = pygame.image.load('grass.PNG')
dirt = pygame.image.load('dirt.PNG')

player_location = [screen.get_width() * 0.5, screen.get_height() *0.5]
vertical_momentum = 0







