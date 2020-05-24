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
        self.groups = game.all_sprites, game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((55, 64))
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
        self.lives = 2
        self.timer = 0
        self.attack = False
        self.isHoldingControl = False
        self.isDoubleJumping = False
        self.canDoubleJump = True
        self.isWallJumping = False
        self.isCrouching = False
        self.isDashing = False
        self.isJumping = False
        self.isFalling = True
        self.canMove = True
        self.isKey = False
        self.czas = 0
        self.moving_right = True
        self.moving_left = False
        self.timer = 10
        self.hasSneakers = False
        self.hasWalljump = False
        self.hasDash = False
        self.fired = False
        self.weapon_select = 3
        self.czas = 0
        self.czas2 = 0
        self.isMaczuga = False
        self.isKusza = False
        self.isMiecz = False
        self.max_exp = 500
        self.max_health = 100
        self.health = self.max_health
        self.exp = 0
        self.level = 1
        self.damage_bonus = 0

    def update(self):
        if self.attack:
            self.czas += 1
        if self.fired:
            self.czas2 += 1
        if self.canMove:
            self.acc = vec(0, PLAYER_GRAV)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                if not self.isCrouching:
                    self.moving_right = True
                    self.moving_left = False
                    if not self.attack:
                        if self.game.player.weapon_select == 1:
                            self.image = self.game.player_right_maczuga
                        if self.game.player.weapon_select == 0:
                            self.image = self.game.player_right_miecz
                        if not self.game.player.isMiecz and not self.game.player.isMaczuga or self.game.player.weapon_select == 2:
                            self.image = self.game.player_right
                    self.acc.x = PLAYER_ACC
                else:
                    self.image = self.game.player_crouch_right
                    self.acc.x = PLAYER_ACC_PRZYKUC
            if keys[pygame.K_a]:
                if not self.isCrouching:
                    self.moving_right = False
                    self.moving_left = True
                    if not self.attack:
                        if self.game.player.weapon_select == 1:
                            self.image = self.game.player_left_maczuga
                        if self.game.player.weapon_select == 0:
                            self.image = self.game.player_left_miecz
                        if not self.game.player.isMiecz and not self.game.player.isMaczuga or self.game.player.weapon_select == 2:
                            self.image = self.game.player_left
                    self.acc.x = -PLAYER_ACC
                else:
                    self.image = self.game.player_crouch_left
                    self.acc.x = -PLAYER_ACC_PRZYKUC
        else:
            self.acc = vec(0, 0.001)

        if self.attack and self.czas > 2:
            Attack(self.game, self.pos.x, self.pos.y)
            if self.image == self.game.player_right_maczuga:
                self.image = self.game.player_attack_right_maczuga
            if self.image == self.game.player_left_maczuga:
                self.image = self.game.player_attack_left_maczuga

            if self.image == self.game.player_right_miecz:
                self.image = self.game.player_attack_right_miecz
            if self.image == self.game.player_left_miecz:
                self.image = self.game.player_attack_left_miecz

        if self.czas > 6 and self.attack:
            self.attack = False
            if self.game.player.weapon_select == 1:
                if self.image == self.game.player_attack_right_maczuga:
                    self.image = self.game.player_right_maczuga
                if self.image == self.game.player_attack_left_maczuga:
                    self.image = self.game.player_left_maczuga
            if self.game.player.weapon_select == 0:
                if self.image == self.game.player_attack_right_miecz:
                    self.image = self.game.player_right_miecz
                if self.image == self.game.player_attack_left_miecz:
                    self.image = self.game.player_left_miecz
            self.czas = 0

        if self.czas2 > 20:
            self.fired = False
            self.czas2 = 0

        if not self.isCrouching:
            self.mask = pygame.mask.from_surface(self.game.player_right)
        else:
            self.mask = pygame.mask.from_surface(self.game.player_crouch_right)

        hits = pygame.sprite.spritecollide(self, self.game.mobs, False, pygame.sprite.collide_mask)
        if hits:
            if self.image == self.game.player_attack_right_maczuga or self.image == self.game.player_attack_right_miecz:
                self.vel.x -= 20
                self.vel.y -= 5
                self.health -= 20
            if self.image == self.game.player_attack_left_maczuga or self.image == self.game.player_attack_left_miecz:
                self.vel.x += 20
                self.vel.y += 5
                self.health -= 20

        if self.isCrouching:
            self.rect.y -= 1
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            self.rect.y += 1
            if not hits and not self.isHoldingControl:
                if self.moving_left:
                    if self.game.player.weapon_select == 0:
                        player_image = self.game.player_left_miecz
                    elif self.game.player.weapon_select == 1:
                        player_image = self.game.player_left_maczuga
                    else:
                        player_image = self.game.player_left
                if self.moving_right:
                    if self.game.player.weapon_select == 0:
                        player_image = self.game.player_right_miecz
                    elif self.game.player.weapon_select == 1:
                        player_image = self.game.player_right_maczuga
                    else:
                        player_image = self.game.player_right
                self.image = player_image
                self.hit_box = PLAYER_HIT_BOX.copy()
                self.isCrouching = False
                self.rect = self.image.get_rect()

        self.timer += 1
        hits = pygame.sprite.spritecollide(self, self.game.mobs, False, pygame.sprite.collide_mask)
        if hits and self.timer > 9:
            if self.image == self.game.player_right or self.image == self.game.player_right_maczuga or self.image == self.game.player_right_miecz:
                self.vel.x -= 20
                self.vel.y -= 5
                self.health -= 20
            if self.image == self.game.player_left or self.image == self.game.player_left_maczuga or self.image == self.game.player_left_miecz:
                self.vel.x += 20
                self.vel.y += 5
                self.health -= 20
            if self.image == self.game.player_crouch_right:
                self.vel.x -= 20
                self.health -= 20
            if self.image == self.game.player_crouch_left:
                self.vel.x += 20
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

        if self.isJumping or self.isDoubleJumping:
            self.rect.y += 1
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            self.rect.y -= 1
            if hits:
                self.rect.y += 1
                hits = pygame.sprite.spritecollide(self, self.game.walls, False, pygame.sprite.collide_mask)
                self.rect.y -= 1
                if hits:
                    self.isJumping = False
                    self.isDoubleJumping = False

        hits = pygame.sprite.spritecollide(self, self.game.spikes, False, pygame.sprite.collide_mask)
        if hits:
            self.health -= 1

        hits = pygame.sprite.spritecollide(self, self.game.levels, False)
        if hits:
            self.game.change_level()

        if self.exp >= self.max_exp:
            self.max_health += 50
            self.health += 50
            self.level += 1
            self.exp = self.exp - self.max_exp
            self.max_exp += 100

    def die(self):
        self.pos = self.resp
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.health = self.max_health
        self.exp = 0
        self.lives -= 1

    def jump(self):
        self.isJumping = True
        if self.pos.y < len(self.game.map_data) * TILESIZE:
            self.vel.y = -13

    def double_jump(self):
        self.isDoubleJumping = True
        if self.pos.y < len(self.game.map_data) * TILESIZE:
            self.vel.y = -11

    def wall_jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.walls, False, pygame.sprite.collide_mask)
        self.rect.x -= 1
        if hits:
            self.vel.y = -10
            self.vel.x = -20
        self.rect.x -= 1
        hits = pygame.sprite.spritecollide(self, self.game.walls, False, pygame.sprite.collide_mask)
        self.rect.x += 1
        if hits:
            self.vel.y = -10
            self.vel.x = 20

    def r_dash(self):
        if self.hasDash:
            if self.vel.y != 0 and not self.isDashing:
                self.start_time = pygame.time.get_ticks()
                self.isDashing = True
                self.canMove = False
                self.vel.x = 20
                self.vel.y = 0

    def l_dash(self):
        if self.hasDash:
            if self.vel.y != 0 and not self.isDashing:
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
        x = min(0, x)
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


class Wall3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.brick1_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Wall4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.dirt2_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Wall5(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.brick1_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.door1
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 100 < self.game.player.rect.x and self.game.player.isKey:
            self.image = self.game.door2
            self.remove(self.game.walls)


class Pochodnia(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.pochodnia_image
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
        self.health = 50
        self.start_x = x
        self.path = [x * TILESIZE - 120, x * TILESIZE + 120]
        self.pos = vec(x, y) * TILESIZE
        self.ile_x = 0
        self.ifhit = False
        self.timer = 0
        self.change = 1
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)

        hits = pygame.sprite.spritecollide(self, self.game.bolts, True)
        if hits:
            if self.game.player.image == self.game.player_right or self.game.player.image == self.game.player_crouch_right:
                self.vel.x = 10
                self.health -= (7 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_left or self.game.player.image == self.game.player_crouch_left:
                self.vel.x = -10
                self.health -= (7 + self.game.player.damage_bonus)

        self.timer += 1

        hits = pygame.sprite.spritecollide(self, self.game.weapons, False)
        if hits and self.timer > 2:
            if self.game.player.image == self.game.player_attack_right_maczuga:
                self.vel.x = 25
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_right_miecz:
                self.vel.x = 15
                self.health -= (15 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_maczuga:
                self.vel.x = -25
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_miecz:
                self.vel.x = -15
                self.health -= (15 + self.game.player.damage_bonus)
            self.timer = 0

        if self.health <= 0 or self.pos.y >= len(self.game.map_data) * TILESIZE:
            self.game.player.exp += 100
            self.kill()

        if not self.ifhit:
            if self.pos.x > self.path[1]:
                self.image = self.game.mob_left
                self.change = -1

            if self.pos.x < self.path[0]:
                self.image = self.game.mob_right
                self.change = 1

        self.ile_x += 1
        if self.ile_x > 50 and self.vel.y == 0:
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

        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x -= 2
        self.rect.x -= 1
        hits1 = pygame.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x += 2
        if hits or hits1:
            self.ifhit = True
            if self.image == self.game.mob_left:
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
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.path = [x * TILESIZE - 120, x * TILESIZE + 120]
        self.pos = vec(x, y) * TILESIZE
        self.accel = ZOMBIE_ACC
        self.health = 100
        self.ile_x = 0
        self.timer1 = 0
        self.ifhit = False
        self.change = 1
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.dis_x = 0
        self.dis_y = 0
        self.min_dis_x = 300
        self.min_dis_y = 200
        self.timer = 0
        self.czySee = False
        self.image = self.game.zombie_right

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)

        if self.health <= 0 or self.pos.y >= len(self.game.map_data) * TILESIZE:
            self.game.player.exp += 150
            self.kill()

        hits = pygame.sprite.spritecollide(self, self.game.bolts, True)
        if hits:
            if self.game.player.image == self.game.player_right or self.game.player.image == self.game.player_crouch_right:
                self.vel.x = 10
                self.health -= (7 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_left or self.game.player.image == self.game.player_crouch_left:
                self.vel.x = -10
                self.health -= (7 + self.game.player.damage_bonus)
            self.czySee = True

        self.timer1 += 1
        hits = pygame.sprite.spritecollide(self, self.game.weapons, False)
        if hits and self.timer1 > 2:
            if self.game.player.image == self.game.player_attack_right_maczuga:
                self.vel.x = 25
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_right_miecz:
                self.vel.x = 15
                self.health -= (15 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_maczuga:
                self.vel.x = -25
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_miecz:
                self.vel.x = -15
                self.health -= (15 + self.game.player.damage_bonus)
            self.czySee = True
            self.timer1 = 0

        if not self.czySee and self.ifhit == False:
            if self.pos.x > self.path[1]:
                self.image = self.game.zombie_left
                self.change = -1

            if self.pos.x < self.path[0]:
                self.image = self.game.zombie_right
                self.change = 1

        self.acc.x = self.accel * self.change
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
            if self.dis_x <= 0 and self.image == self.game.zombie_right:
                self.czySee = True
                self.change = 1
                self.accel = 0.8
                self.rect.x += 1
                hits = pygame.sprite.spritecollide(self, self.game.walls, False)
                self.rect.x -= 2
                if hits and self.vel.y == 0:
                    self.vel.y -= 12
            elif self.dis_x <= 0 and self.image == self.game.zombie_left:
                self.czySee = False
                self.accel = ZOMBIE_ACC

            if self.dis_x > 0 and self.image == self.game.zombie_left:
                self.czySee = True
                self.change = -1
                self.accel = 0.8
                self.rect.x -= 1
                hits = pygame.sprite.spritecollide(self, self.game.walls, False)
                self.rect.x += 2
                if hits and self.vel.y == 0:
                    self.vel.y -= 12
            elif self.dis_x > 0 and self.image == self.game.zombie_right:
                self.czySee = False
                self.accel = ZOMBIE_ACC

        else:
            self.czySee = False
            self.accel = ZOMBIE_ACC

        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x -= 1
        self.rect.x -= 1
        hits1 = pygame.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x += 1
        if (hits or hits1) and not self.czySee and self.vel.x == 0:
            self.ifhit = True
            if self.image == self.game.zombie_left:
                self.image = self.game.zombie_right
            elif self.image == self.game.zombie_right:
                self.image = self.game.zombie_left
            self.change *= -1


class Mob3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((64, 64))
        self.image.blit(self.game.flying_right, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.hit_box = FLYING_HIT_BOX.copy()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.hit_box.center = self.rect.center
        self.health = 150
        self.path = [x * TILESIZE - 220, x * TILESIZE + 220]
        self.pos = vec(x, y) * TILESIZE
        self.start_y = y * TILESIZE
        self.czySee = False
        self.accel = FLYING_ACC
        self.change = 1
        self.dis_x = 0
        self.dis_y = 0
        self.timer = 0
        self.min_dis_x = 300
        self.min_dis_y = 300
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)

        hits = pygame.sprite.spritecollide(self, self.game.bolts, True)
        if hits:
            if self.game.player.image == self.game.player_right or self.game.player.image == self.game.player_crouch_right:
                self.vel.x = 10
                self.health -= (7 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_left or self.game.player.image == self.game.player_crouch_left:
                self.vel.x = -10
                self.health -= (7 + self.game.player.damage_bonus)

        self.timer += 1

        hits = pygame.sprite.spritecollide(self, self.game.weapons, False)
        if hits and self.timer > 2:
            if self.game.player.image == self.game.player_attack_right_maczuga:
                self.vel.x = 25
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_right_miecz:
                self.vel.x = 15
                self.health -= (15 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_maczuga:
                self.vel.x = -25
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_miecz:
                self.vel.x = -15
                self.health -= (15 + self.game.player.damage_bonus)
            self.timer = 0

        if self.health <= 0:
            self.game.player.exp += 200
            self.kill()

        if not self.czySee:
            if self.pos.x > self.path[1]:
                self.image = self.game.flying_left
                self.change = -1

            if self.pos.x < self.path[0]:
                self.image = self.game.flying_right
                self.change = 1

        self.acc.x = self.accel * self.change
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
            if self.dis_x <= 0:
                if self.image == self.game.flying_left:
                    self.image = self.game.flying_right
                self.czySee = True
                self.change = 1
                if self.game.player.pos.y > self.pos.y:
                    self.vel.y = 1
                if self.game.player.pos.y < self.pos.y:
                    self.vel.y = -1

            elif self.dis_x > 0:
                if self.image == self.game.flying_right:
                    self.image = self.game.flying_left
                self.czySee = True
                self.change = -1
                if self.game.player.pos.y > self.pos.y:
                    self.vel.y = 1
                if self.game.player.pos.y < self.pos.y:
                    self.vel.y = -1
        else:
            self.czySee = False
            self.accel = FLYING_ACC

        if not self.czySee:
            if self.pos.y > self.start_y:
                self.vel.y = -1
            elif self.pos.y < self.start_y:
                self.vel.y = 1
            elif self.pos.y == self.start_y:
                self.vel.y = 0


class Mob4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((32, 48))
        self.image.blit(self.game.ghost_right, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.hit_box = GHOST_HIT_BOX.copy()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.hit_box.center = self.rect.center
        self.health = 100
        self.path = [x * TILESIZE - 150, x * TILESIZE + 150]
        self.pos = vec(x, y) * TILESIZE
        self.start_y = y * TILESIZE
        self.czySee = False
        self.accel = GHOST_ACC
        self.timer = 0
        self.change = 1
        self.dis_x = 0
        self.dis_y = 0
        self.min_dis_x = 250
        self.min_dis_y = 250
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)

        hits = pygame.sprite.spritecollide(self, self.game.bolts, True)
        if hits:
            if self.game.player.image == self.game.player_right or self.game.player.image == self.game.player_crouch_right:
                self.vel.x = 10
                self.health -= (7 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_left or self.game.player.image == self.game.player_crouch_left:
                self.vel.x = -10
                self.health -= (7 + self.game.player.damage_bonus)

        self.timer += 1

        hits = pygame.sprite.spritecollide(self, self.game.weapons, False)
        if hits and self.timer > 2:
            if self.game.player.image == self.game.player_attack_right_maczuga:
                self.vel.x = 25
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_right_miecz:
                self.vel.x = 15
                self.health -= (15 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_maczuga:
                self.vel.x = -25
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_miecz:
                self.vel.x = -15
                self.health -= (15 + self.game.player.damage_bonus)
            self.timer = 0

        if self.health <= 0:
            self.game.player.exp += 150
            self.kill()

        if not self.czySee:
            if self.pos.x > self.path[1]:
                self.image = self.game.ghost_left
                self.change = -1

            if self.pos.x < self.path[0]:
                self.image = self.game.ghost_right
                self.change = 1

        self.acc.x = self.accel * self.change
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

        self.dis_x = self.rect.x - self.game.player.rect.x
        self.dis_y = self.rect.y - self.game.player.rect.y

        if self.min_dis_x > self.dis_x > -self.min_dis_x and self.min_dis_y > self.dis_y > -self.min_dis_y:
            if self.dis_x <= 0:
                self.accel = 0.6
                if self.image == self.game.ghost_left:
                    self.image = self.game.ghost_right
                self.czySee = True
                self.change = 1
                if self.game.player.pos.y > self.pos.y:
                    self.vel.y = 1
                if self.game.player.pos.y < self.pos.y:
                    self.vel.y = -1
                if self.game.player.pos.y == self.pos.y:
                    self.vel.y = 0

            elif self.dis_x > 0:
                self.accel = 0.6
                if self.image == self.game.ghost_right:
                    self.image = self.game.ghost_left
                self.czySee = True
                self.change = -1
                if self.game.player.pos.y > self.pos.y:
                    self.vel.y = 1
                if self.game.player.pos.y < self.pos.y:
                    self.vel.y = -1
                if self.game.player.pos.y == self.pos.y:
                    self.vel.y = 0
        else:
            self.czySee = False
            self.accel = GHOST_ACC
            self.vel.y = 0


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
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
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
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
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
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
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


class Grave2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grave2_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Fence(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.fence_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Spikes1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.spikes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spike1
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE + (TILESIZE - game.spike1.get_height())


class Spikes2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.spikes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spike2
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Spikes3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.spikes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spike3
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Spikes4(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.spikes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spike4
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE + (TILESIZE - game.spike4.get_width())
        self.rect.y = y * TILESIZE


class Lives(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.heart_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
            self.kill()
            self.game.player.lives += 1


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.weapons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((45, 45))
        self.image.blit(self.game.sword, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = (self.image.get_rect())
        self.hit_box = ATTACK_HIT_BOX.copy()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.hit_box.center = self.rect.center
        if self.game.player.image == self.game.player_right_maczuga or self.game.player.image == self.game.player_right_miecz:
            self.rect.x = x + 12
            self.rect.y = y - 15
        elif self.game.player.image == self.game.player_left_maczuga or self.game.player.image == self.game.player_left_miecz:
            self.rect.x = x - 56
            self.rect.y = y - 15
        self.ile = 0

    def update(self):
        self.ile += 1
        if self.ile > 0:
            self.kill()
            self.ile = 0


class Bolt(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.bolts
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if game.player.image == game.player_right or game.player.image == game.player_crouch_right:
            self.image = game.bolt
            self.rect = self.image.get_rect()
            self.vel = 20
            self.rect.x = game.player.rect.x + 25
            self.rect.y = game.player.rect.y + 20
        else:
            self.image = game.bolt2
            self.rect = self.image.get_rect()
            self.vel = -20
            self.rect.x = game.player.rect.x + 5
            self.rect.y = game.player.rect.y + 20

    def update(self):
        self.rect.x += self.vel
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.kill()


class Maczuga(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.maczuga
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
            self.kill()
            self.game.player.isMaczuga = True
            self.game.player.weapon_select = 1
            if not self.game.player.isCrouching:
                if self.game.player.image == self.game.player_right or self.game.player.image == self.game.player_right_miecz:
                    self.game.player.image = self.game.player_right_maczuga
                if self.game.player.image == self.game.player_left or self.game.player.image == self.game.player_left_miecz:
                    self.game.player.image = self.game.player_left_maczuga


class Miecz(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.miecz
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
            self.kill()
            self.game.player.isMiecz = True
            self.game.player.weapon_select = 0
            if not self.game.player.isCrouching:
                if self.game.player.image == self.game.player_right or self.game.player.image == self.game.player_right_maczuga:
                    self.game.player.image = self.game.player_right_miecz
                if self.game.player.image == self.game.player_left or self.game.player.image == self.game.player_left_maczuga:
                    self.game.player.image = self.game.player_left_miecz


class Kusza(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.kusza
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
            self.kill()
            self.game.player.isKusza = True
            self.game.player.weapon_select = 2


class Level(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.levels
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.level
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.checkpoints
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.checkpoint
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.players, False)
        if hits:
            self.game.player.resp = (self.x * TILESIZE + 16, self.y * TILESIZE)


class Potion1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.potion1
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
            if self.game.player.health <= self.game.player.max_health - 30:
                self.game.player.health += 30
                self.kill()
            elif self.game.player.health < self.game.player.max_health:
                self.game.player.health = self.game.player.max_health
                self.kill()


class Potion2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.potion2
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
            self.kill()
            self.game.player.exp += 100


class Potion3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.potion3
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.czas = 0

    def update(self):
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
            self.kill()
            self.czas += 1
            self.game.player.damage_bonus = 10
        if self.czas >= 1:
            if self.czas >= 200:
                self.czas = 0
                self.game.player.damage_bonus = 0
            self.czas += 1


class Key(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.key
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.czas = 0

    def update(self):
        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x + 17 and self.rect.y - 63 < self.game.player.rect.y < self.rect.y + 32:
            self.kill()
            self.game.player.isKey = True


class Tabliczka(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.tabliczka
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Gates(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.gates
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Cross(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cross_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Cannon_right(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cannon_right
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.health = 25
        self.timer = 0
        self.timer1 = 0
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE - 18

    def update(self):
        self.timer1 += 1
        if self.timer1 > 50:
            Cannon_ball_right(self.game, self.x, self.y)
            self.timer1 = 0

        hits = pygame.sprite.spritecollide(self, self.game.bolts, True)
        if hits:
            self.health -= (7 + self.game.player.damage_bonus)

        self.timer += 1

        hits = pygame.sprite.spritecollide(self, self.game.weapons, False)
        if hits and self.timer > 2:
            if self.game.player.image == self.game.player_attack_right_maczuga or self.game.player.image == self.game.player_attack_left_maczuga:
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_right_miecz or self.game.player.image == self.game.player_attack_left_miecz:
                self.health -= (15 + self.game.player.damage_bonus)
            self.timer = 0

        if self.health <= 0:
            self.game.player.exp += 150
            self.kill()


class Cannon_left(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cannon_left
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.health = 25
        self.timer = 0
        self.timer1 = 0
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE - 18

    def update(self):
        self.timer1 += 1
        if self.timer1 > 50:
            Cannon_ball_left(self.game, self.x, self.y)
            self.timer1 = 0

        hits = pygame.sprite.spritecollide(self, self.game.bolts, True)
        if hits:
            if self.game.player.image == self.game.player_right or self.game.player.image == self.game.player_crouch_right:
                self.health -= (7 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_left or self.game.player.image == self.game.player_crouch_left:
                self.health -= (7 + self.game.player.damage_bonus)

        self.timer += 1

        hits = pygame.sprite.spritecollide(self, self.game.weapons, False)
        if hits and self.timer > 2:
            if self.game.player.image == self.game.player_attack_right_maczuga:
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_right_miecz:
                self.health -= (15 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_maczuga:
                self.health -= (10 + self.game.player.damage_bonus)
            if self.game.player.image == self.game.player_attack_left_miecz:
                self.health -= (15 + self.game.player.damage_bonus)
            self.timer = 0

        if self.health <= 0:
            self.game.player.exp += 150
            self.kill()


class Cannon_ball_left(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.cannon_balls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cannon_ball
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vel = -10
        self.timer = 0
        self.rect.x = x * TILESIZE - 15
        self.rect.y = y * TILESIZE + 9

    def update(self):
        self.rect.x += self.vel
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.kill()

        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x and self.rect.y - 50 < self.game.player.rect.y < self.rect.y + 19:
            self.kill()
            self.game.player.vel.x = -10
            self.game.player.health -= 10
            self.timer = 0


class Cannon_ball_right(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.cannon_balls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cannon_ball
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vel = 10
        self.timer = 0
        self.rect.x = x * TILESIZE + 46
        self.rect.y = y * TILESIZE + 9

    def update(self):
        self.rect.x += self.vel
        hits = pygame.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.kill()

        if self.rect.x - 40 < self.game.player.rect.x < self.rect.x and self.rect.y - 50 < self.game.player.rect.y < self.rect.y + 19:
            self.kill()
            self.game.player.vel.x = 10
            self.game.player.health -= 10
            self.timer = 0


class Grave3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.grave3_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
