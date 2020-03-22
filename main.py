import pygame, sys
import graphics
from settings import *
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption('My Game Window')

moving_right = False
moving_left = False
air_timer = 0

player_rect = pygame.Rect(320, 256, graphics.player_Right.get_width(), graphics.player_Right.get_height())


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map('map')


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


while True:
    display.blit(graphics.background, (0, 0))

    scroll[0] += (player_rect.x - scroll[0] - 306) / 5
    scroll[1] += (player_rect.y - scroll[1] - 256) / 5

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(graphics.dirt, (x * graphics.dirt.get_width() - scroll[0], y * graphics.dirt.get_height() - scroll[1]))
            if tile == '2':
                display.blit(graphics.grass, (x * graphics.grass.get_width() - scroll[0], y * graphics.grass.get_height() - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2

    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 8:
        vertical_momentum = 8

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    if collisions['top'] == True:
        vertical_momentum = 0

    if air_timer > 100:
        player_rect = pygame.Rect(320, 256, graphics.player_Right.get_width(), graphics.player_Right.get_height())

    display.blit(graphics.player_Right, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_SPACE:
                if air_timer < 6:
                    vertical_momentum = -5
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)
