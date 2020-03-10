import pygame
from settings import *
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 10, HEIGHT / 10)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.level = None

    def jump(self):
            self.rect.x += 1
            hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.x -= 1
            if hits:
                self.vel.y = -15

    def update(self):
            self.acc = vec(0, PLAYER_GRAV)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.acc.x = -PLAYER_ACC
            if keys[pygame.K_d]:
                self.acc.x = PLAYER_ACC

            self.acc.x += self.vel.x * PLAYER_FRICTION
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            self.rect.midbottom = self.pos

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GROUND)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
