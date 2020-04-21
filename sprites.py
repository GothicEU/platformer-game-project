import math

from settings import *

vec = pygame.math.Vector2


def collide_with_walls(sprite, group, direction):
    if direction=='x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_box)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_box.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_box.width / 2
            sprite.vel.x = 0
            sprite.hit_box.centerx = sprite.pos.x
    if direction=='y':
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
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((self.game.player_image.get_width(), self.game.player_image.get_height()))
        self.image.blit(self.game.player_image, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.hit_box = PLAYER_HIT_BOX.copy()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.hit_box.center = self.rect.center
        self.resp = (x * TILESIZE, y * TILESIZE)
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.start_time = 0
        self.health = PLAYER_HEALTH
        self.lives = 2
        self.timer = 0
        self.isHoldingControl = False
        self.isDoubleJumping = False
        self.canDoubleJump = True
        self.isWallJumping = False
        self.isCrouching = False
        self.isDashing = False
        self.isJumping = False
        self.isFalling = True
        self.canMove = True
        self.moving_right = True
        self.moving_left = False
        self.timer = 10
        self.hasSneakers = False
        self.hasWalljump = False
        self.hasDash = False

    def update(self):
        global player_image
        if self.canMove:
            self.acc = vec(0, PLAYER_GRAV)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                if not self.isCrouching:
                    self.moving_right = True
                    self.moving_left = False
                    self.image = self.game.player_right
                    self.acc.x = PLAYER_ACC
                else:
                    self.image = self.game.player_crouch_right
                    self.acc.x = PLAYER_ACC_PRZYKUC
            if keys[pygame.K_a]:
                if not self.isCrouching:
                    self.moving_right = False
                    self.moving_left = True
                    self.image = self.game.player_left
                    self.acc.x = -PLAYER_ACC
                else:
                    self.image = self.game.player_crouch_left
                    self.acc.x = -PLAYER_ACC_PRZYKUC
        else:
            self.acc = vec(0, 0.001)

        if self.isCrouching:
            self.rect.y -= 1
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            self.rect.y += 1
            if not hits and not self.isHoldingControl:
                if self.moving_left:
                    player_image = self.game.player_left
                if self.moving_right:
                    player_image = self.game.player_right
                self.image = player_image
                self.hit_box = PLAYER_HIT_BOX.copy()
                self.isCrouching = False
                self.rect = self.image.get_rect()

        self.timer += 1
        self.rect.y -= 1
        hits = pygame.sprite.spritecollide(self, self.game.mobs, False)
        self.rect.y += 1
        if hits and self.timer > 9:
            if self.image==self.game.player_right:
                self.vel.x -= 20
                self.vel.y -= 5
                self.health -= 20
            if self.image==self.game.player_left:
                self.vel.x += 20
                self.vel.y += 5
                self.health -= 20
            if self.image==self.game.player_crouch_right:
                self.vel.x -= 20
                self.health -= 20
            if self.image==self.game.player_crouch_left:
                self.vel.x += 20
                self.health -= 20

            self.timer = 0

        self.rect.y += 1
        hits2 = pygame.sprite.spritecollide(self, self.game.mobs, False)
        self.rect.y -= 1
        if hits2 and self.timer > 9:
            if self.image==self.game.player_right:
                self.vel.x = 20
                self.vel.y = 20
                self.health -= 20
            if self.image==self.game.player_left:
                self.vel.x = 20
                self.vel.y = 20
                self.health -= 20
            if self.image==self.game.player_crouch_right:
                self.vel.x = 20
                self.health -= 20
            if self.image==self.game.player_crouch_left:
                self.vel.x = 20
                self.health -= 20

            self.timer = 0

        if self.health <= 0 or self.pos.y >= len(self.game.map_data) * TILESIZE:
            self.die()

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_box.center

        if self.isDashing:
            if self.vel.y==0:
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

        if self.isJumping or self.isDoubleJumping or self.isWallJumping:
            self.rect.y += 1
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            self.rect.y -= 1
            if hits:
                self.isJumping = False
                self.isWallJumping = False
                self.isDoubleJumping = False
                self.canDoubleJump = True

        if self.isWallJumping:
            self.canDoubleJump = True

    def die(self):
        self.pos = self.resp
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.health = PLAYER_HEALTH
        self.lives -= 1


    def jump(self):
        self.isJumping = True
        if self.pos.y < len(self.game.map_data) * TILESIZE:
            self.vel.y = -13

    def double_jump(self):
        if not self.isDoubleJumping and self.hasSneakers:
            self.isDoubleJumping = True
            if self.pos.y < len(self.game.map_data) * TILESIZE:
                self.vel.y = -10

    def wall_jump(self):
        if self.hasWalljump:
            self.isWallJumping = True
            self.rect.x += 1
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            self.rect.x -= 1
            if hits:
                self.vel.y = -10
                self.vel.x = -10
            self.rect.x -= 1
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            self.rect.x += 1
            if hits:
                self.vel.y = -10
                self.vel.x = 10


    def r_dash(self):
        if self.hasDash:
            if self.vel.y!=0 and not self.isDashing:
                self.start_time = pygame.time.get_ticks()
                self.isDashing = True
                self.canMove = False
                self.vel.x = 20
                self.vel.y = 0

    def l_dash(self):
        if self.hasDash:
            if self.vel.y!=0 and not self.isDashing:
                self.start_time = pygame.time.get_ticks()
                self.isDashing = True
                self.canMove = False
                self.vel.x = -20
                self.vel.y = 0


def collide_hit_box(one, two):
    return one.hit_box.colliderect(two.rect)


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)
        # limit scrolling
        x = min(0, x)  # left
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)


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


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((28, 26))
        self.image.blit(self.game.mob_right, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.hit_box = MOB_HIT_BOX.copy()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.hit_box.center = self.rect.center
        self.start_x = x
        self.path = [x * TILESIZE - 120, x * TILESIZE + 120]
        self.pos = vec(x, y) * TILESIZE
        self.ile_x = 0
        self.ifhit = False
        self.change = 1
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)

        if not self.ifhit:
            if self.pos.x > self.path[1]:
                self.image = self.game.mob_left
                self.change = -1

            if self.pos.x < self.path[0]:
                self.image = self.game.mob_right
                self.change = 1

        self.ile_x += 1
        if self.ile_x > 50 and self.vel.y==0:
            self.vel.y = -15
            self.ile_x = 0

        self.acc.x = MOB_ACC * self.change
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_box.center

        if self.vel.x==0:
            self.ifhit = True
            if self.image==self.game.mob_left:
                self.image = self.game.mob_right
            else:
                self.image = self.game.mob_left
            self.change *= -1


class Mob2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((32, 64))
        self.image.blit(self.game.zombie_right, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.hit_box = ZOMBIE_HIT_BOX.copy()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.hit_box.center = self.rect.center
        self.start_x = x
        self.path = [x * TILESIZE - 120, x * TILESIZE + 120]
        self.pos = vec(x, y) * TILESIZE
        self.ile_x = 0
        self.ifhit = False
        self.change = 1
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dis_x = 0
        self.dis_y = 0
        self.min_dis_x = 300
        self.min_dis_y = 150
        self.timer = 0
        self.czySee = False
        self.image = self.game.zombie_right

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)

        if not self.czySee:
            if not self.ifhit:
                if self.pos.x > self.path[1]:
                    self.image = self.game.zombie_left
                    self.change = -1

            if self.pos.x < self.path[0]:
                self.image = self.game.zombie_right
                self.change = 1

        self.acc.x = ZOMBIE_ACC * self.change
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

        self.hit_box.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_box.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_box.center

        self.dis_x = self.rect.x - self.game.player.rect.x
        self.dis_y = self.rect.y - self.game.player.rect.y

        if self.min_dis_x > self.dis_x > -self.min_dis_x and self.min_dis_y > self.dis_y > -self.min_dis_y:
            if self.dis_x <= 0 and self.image==self.game.zombie_right:
                self.czySee = True
                self.vel.x = 0.8
                self.pos.x += 4
                self.rect.x += 1
                hits = pygame.sprite.spritecollide(self, self.game.walls, False)
                self.rect.x -= 2
                if hits and self.vel.y == 0:
                    self.vel.y -= 12
            else:
                self.czySee = False

            if self.dis_x > 0 and self.image==self.game.zombie_left:
                self.czySee = True
                self.vel.x = -0.8
                self.pos.x -= 4
                self.rect.x -= 1
                hits = pygame.sprite.spritecollide(self, self.game.walls, False)
                self.rect.x += 2
                if hits and self.vel.y == 0:
                    self.vel.y -= 12

            if self.vel.y==0:
                self.czyJump = False
        else:
            self.czySee = False

        if not self.czySee:
            if self.vel.x==0:
                self.ifhit = True
                if self.image==self.game.zombie_left:
                    self.image = self.game.zombie_right
                else:
                    self.image = self.game.zombie_left
                self.change *= -1


class Sneakers(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.sneakers_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 33 < self.game.player.rect.x < self.rect.x + 33 and self.rect.y - 33 < self.game.player.rect.y < self.rect.y + 33:
            self.kill()
            self.game.player.hasSneakers = True


class Walljump(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.walljump_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 33 < self.game.player.rect.x < self.rect.x + 33 and self.rect.y - 33 < self.game.player.rect.y < self.rect.y + 33:
            self.kill()
            self.game.player.hasWalljump = True


class Dash(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.dash_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 33 < self.game.player.rect.x < self.rect.x + 33 and self.rect.y - 33 < self.game.player.rect.y < self.rect.y + 33:
            self.remove(self.game.items)
            self.kill()
            self.game.player.hasDash = True


class Grave(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grave_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Lives(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = heart
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 33 < self.game.player.rect.x < self.rect.x + 33 and self.rect.y - 33 < self.game.player.rect.y < self.rect.y + 33:
            self.kill()
            self.game.player.lives += 1
