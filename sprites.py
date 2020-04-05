from settings import *

vec = pygame.math.Vector2


def collide_with_walls(sprite, group, direction):
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_box.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_box.width / 2
            sprite.vel.x = 0
            sprite.hit_box.centerx = sprite.pos.x
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_box.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_box.height / 2
            sprite.vel.y = 0
            sprite.hit_box.centery = sprite.pos.y


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        global player_image
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((player_image.get_width(), player_image.get_height()))
        self.image.blit(player_image, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.hit_box = PLAYER_HIT_BOX
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.hit_box.center = self.rect.center
        self.resp = (x * TILESIZE, y * TILESIZE)
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.start_time = 0
        self.timer = 0
        self.isHoldingControl = False
        self.isCrouching = False
        self.isDashing = False
        self.isFalling = True
        self.canMove = True

    def update(self):
        if self.canMove:
            self.acc = vec(0, PLAYER_GRAV)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                if not self.isCrouching:
                    self.acc.x = PLAYER_ACC
                else:
                    self.acc.x = PLAYER_ACC_PRZYKUC
            if keys[pygame.K_a]:
                if not self.isCrouching:
                    self.acc.x = -PLAYER_ACC
                else:
                    self.acc.x = -PLAYER_ACC_PRZYKUC
        else:
            self.acc = vec(0, 0.001)

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_box.center

        if self.isDashing:
            if self.vel.y == 0:
                self.isDashing = False
                self.canMove = True
                self.start_time = 0
                self.timer = 0
            self.timer = pygame.time.get_ticks() - self.start_time
            self.timer = self.timer / 1000
            if self.timer >= 0.4:
                self.canMove = True
                self.start_time = 0
                self.timer = 0

        if self.isCrouching:
            self.rect.y -= 1
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            self.rect.y += 1
            if not hits and not self.isHoldingControl:
                self.image = player_right
                self.hit_box = PLAYER_HIT_BOX
                self.isCrouching = False
                self.rect = self.image.get_rect()

    def jump(self):
        if self.vel.y == 0 and not self.isDashing:
            if self.pos.y < 720:
                self.vel.y = -10

    def fall(self):
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def r_dash(self):
        if self.vel.y != 0 and not self.isDashing:
            self.start_time = pygame.time.get_ticks()
            self.isDashing = True
            self.canMove = False
            self.vel.x = 20
            self.vel.y = 0

    def l_dash(self):
        if self.vel.y != 0 and not self.isDashing:
            self.start_time = pygame.time.get_ticks()
            self.isDashing = True
            self.canMove = False
            self.vel.x = -20
            self.vel.y = 0


def collide_hit_box(one, two):
    return one.hit_box.colliderect(two.rect)


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip())  # strips away any \n characters when read

        self.tile_width = len(self.data[0])
        self.tile_height = len(self.data)
        self.width = self.tile_width * TILESIZE
        self.height = self.tile_height * TILESIZE


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.dirt_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Wall2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grass_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
