import os

from sprites import *

game_map = 'map3.txt'


def change_map():
    global game_map
    if game_map == 'map1.txt':
        game_map = 'map2.txt'
    elif game_map == 'map2.txt':
        game_map = 'map3.txt'
    elif game_map == 'map3.txt':
        game_map = 'map4.txt'
    elif game_map == 'map4.txt':
        game_map = 'map5.txt'


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def draw_player_icons(game):
    if game.player.isMiecz:
        game.screen.blit(game.miecz, (1088, 688))
    if game.player.isMaczuga:
        game.screen.blit(game.maczuga, (1120, 688))
    if game.player.isKusza:
        game.screen.blit(game.kusza, (1152, 688))
    if game.player.hasSneakers:
        game.screen.blit(game.sneakers_image, (1184, 688))
    if game.player.hasDash:
        game.screen.blit(game.dash_image, (1216, 688))
    if game.player.hasWalljump:
        game.screen.blit(game.walljump_image, (1248, 688))


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.66:
        col = GREEN
    elif pct > 0.33:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, GRAY, pygame.Rect(x, y, 150, 20))
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, GRAY, outline_rect, 2)


def draw_player_exp(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

    col = YELLOW
    pygame.draw.rect(surf, GRAY, pygame.Rect(x, y, 100, 15))
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, GRAY, outline_rect, 2)


def draw_player_lives(pct):
    x = 0
    while pct > 0:
        screen.blit(heart, (170 + x, 10))
        pct -= 1
        x += 25


def change_levels():
    change_map()


class Game:
    def __init__(self):
        # intialize game window, etc
        global game_map
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
        pygame.display.update()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
        self.running = True
        self.playing = True

    def load_data(self):
        global game_map
        game_folder = os.path.dirname(__file__)
        self.map_data = []
        with open(os.path.join(game_folder, game_map), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.ghost_left = pygame.image.load('ghost_left.PNG').convert_alpha()
        self.ghost_left = pygame.transform.scale(self.ghost_left,
                                                 (self.ghost_left.get_width(), self.ghost_left.get_height()))
        self.ghost_right = pygame.image.load('ghost_right.PNG').convert_alpha()
        self.ghost_right = pygame.transform.scale(self.ghost_right,
                                                  (self.ghost_right.get_width(), self.ghost_right.get_height()))
        self.dirt2_image = pygame.image.load('dirt2.PNG').convert_alpha()
        self.dirt2_image = pygame.transform.scale(self.dirt2_image, (self.dirt2_image.get_width(), self.dirt2_image.get_height()))
        self.checkpoint = pygame.image.load('checkpoint.png').convert_alpha()
        self.checkpoint = pygame.transform.scale(self.checkpoint,
                                                 (self.checkpoint.get_width(), self.checkpoint.get_height()))
        self.level = pygame.image.load('level.png').convert_alpha()
        self.level = pygame.transform.scale(self.level, (TILESIZE, TILESIZE))
        self.potion1 = pygame.image.load('hp.png').convert_alpha()
        self.potion1 = pygame.transform.scale(self.potion1, (TILESIZE, TILESIZE))
        self.potion2 = pygame.image.load('exp2.png').convert_alpha()
        self.potion2 = pygame.transform.scale(self.potion2, (TILESIZE, TILESIZE))
        self.potion3 = pygame.image.load('ws.png').convert_alpha()
        self.potion3 = pygame.transform.scale(self.potion3, (TILESIZE, TILESIZE))
        self.key = pygame.image.load('key.PNG').convert_alpha()
        self.key = pygame.transform.scale(self.key, (TILESIZE, TILESIZE))
        self.bolt = pygame.image.load('bolt.png').convert_alpha()
        self.bolt = pygame.transform.scale(self.bolt, (self.bolt.get_width(), self.bolt.get_height()))
        self.bolt2 = pygame.image.load('bolt2.png').convert_alpha()
        self.bolt2 = pygame.transform.scale(self.bolt2, (self.bolt2.get_width(), self.bolt2.get_height()))
        self.spike1 = pygame.image.load('spikes_up.png').convert_alpha()
        self.spike1 = pygame.transform.scale(self.spike1, (self.spike1.get_width(), self.spike1.get_height()))
        self.spike2 = pygame.image.load('spikes_down.png').convert_alpha()
        self.spike2 = pygame.transform.scale(self.spike2, (self.spike2.get_width(), self.spike2.get_height()))
        self.spike3 = pygame.image.load('spikes_left.png').convert_alpha()
        self.spike3 = pygame.transform.scale(self.spike3, (self.spike3.get_width(), self.spike3.get_height()))
        self.spike4 = pygame.image.load('spikes_right.png').convert_alpha()
        self.spike4 = pygame.transform.scale(self.spike4, (self.spike3.get_width(), self.spike3.get_height()))
        self.tlo = pygame.image.load('tlo2.PNG').convert_alpha()
        self.tlo = pygame.transform.scale(self.tlo, (WIDTH, HEIGHT))
        self.tlo2 = pygame.image.load('test1.PNG').convert_alpha()
        self.tlo2 = pygame.transform.scale(self.tlo2, (WIDTH, HEIGHT))
        self.dirt_image = pygame.image.load('dirt.PNG').convert_alpha()
        self.dirt_image = pygame.transform.scale(self.dirt_image, (TILESIZE, TILESIZE))
        self.brick1_image = pygame.image.load('brick.PNG').convert_alpha()
        self.brick1_image = pygame.transform.scale(self.brick1_image, (TILESIZE, TILESIZE))
        self.pochodnia_image = pygame.image.load('pochodnia.PNG').convert_alpha()
        self.pochodnia_image = pygame.transform.scale(self.pochodnia_image, (32, 64))
        self.grass_image = pygame.image.load('grass.PNG').convert_alpha()
        self.door1 = pygame.image.load('door1.PNG').convert_alpha()
        self.door1 = pygame.transform.scale(self.door1, (9, 64))
        self.door2 = pygame.image.load('door2.PNG').convert_alpha()
        self.door2 = pygame.transform.scale(self.door2, (32, 64))
        self.grass_image = pygame.transform.scale(self.grass_image, (TILESIZE, TILESIZE))
        self.mob_right = pygame.image.load('mob_right.PNG').convert_alpha()
        self.mob_right = pygame.transform.scale(self.mob_right,
                                                (self.mob_right.get_width(), self.mob_right.get_height()))
        self.mob_left = pygame.image.load('mob_left.PNG').convert_alpha()
        self.mob_left = pygame.transform.scale(self.mob_left, (self.mob_left.get_width(), self.mob_left.get_height()))
        self.zombie_right = pygame.image.load('zombie_right.PNG').convert_alpha()
        self.zombie_right = pygame.transform.scale(self.zombie_right,
                                                   (self.zombie_right.get_width(), self.zombie_right.get_height()))
        self.zombie_left = pygame.image.load('zombie_left.PNG').convert_alpha()
        self.zombie_left = pygame.transform.scale(self.zombie_left,
                                                  (self.zombie_left.get_width(), self.zombie_left.get_height()))
        self.player_right = pygame.image.load('right.PNG').convert_alpha()
        self.player_right = pygame.transform.scale(self.player_right,
                                                   (self.player_right.get_width(), self.player_right.get_height()))
        self.player_left = pygame.image.load('left.PNG').convert_alpha()
        self.player_left = pygame.transform.scale(self.player_left,
                                                  (self.player_left.get_width(), self.player_left.get_height()))
        self.player_right_maczuga = pygame.image.load('right_maczuga.PNG').convert_alpha()
        self.player_right_maczuga = pygame.transform.scale(self.player_right_maczuga, (55, 64))
        self.player_left_maczuga = pygame.image.load('left_maczuga.PNG').convert_alpha()
        self.player_left_maczuga = pygame.transform.scale(self.player_left_maczuga, (55, 64))
        self.player_right_miecz = pygame.image.load('right_miecz.PNG').convert_alpha()
        self.player_right_miecz = pygame.transform.scale(self.player_right_miecz, (55, 64))
        self.player_left_miecz = pygame.image.load('left_miecz.PNG').convert_alpha()
        self.player_left_miecz = pygame.transform.scale(self.player_left_miecz, (55, 64))
        self.player_crouch_right = pygame.image.load('crouch_right.PNG').convert_alpha()
        self.player_crouch_right = pygame.transform.scale(self.player_crouch_right, (
            self.player_crouch_right.get_width(), self.player_crouch_right.get_height()))
        self.player_crouch_left = pygame.image.load('crouch_left.PNG').convert_alpha()
        self.player_crouch_left = pygame.transform.scale(self.player_crouch_left, (
            self.player_crouch_left.get_width(), self.player_crouch_left.get_height()))
        self.player_attack_right_miecz = pygame.image.load('right_attack_miecz.PNG').convert_alpha()
        self.player_attack_right_miecz = pygame.transform.scale(self.player_attack_right_miecz, (55, 64))
        self.player_attack_left_miecz = pygame.image.load('left_attack_miecz.PNG').convert_alpha()
        self.player_attack_left_miecz = pygame.transform.scale(self.player_attack_left_miecz, (55, 64))
        self.player_attack_right_maczuga = pygame.image.load('right_attack_maczuga.PNG').convert_alpha()
        self.player_attack_right_maczuga = pygame.transform.scale(self.player_attack_right_maczuga, (55, 64))
        self.player_attack_left_maczuga = pygame.image.load('left_attack_maczuga.PNG').convert_alpha()
        self.player_attack_left_maczuga = pygame.transform.scale(self.player_attack_left_maczuga, (55, 64))
        self.player_image = self.player_right
        self.sneakers_image = pygame.image.load('sneakers.png').convert_alpha()
        self.sneakers_image = pygame.transform.scale(self.sneakers_image, (TILESIZE, TILESIZE))
        self.walljump_image = pygame.image.load('walljump.png').convert_alpha()
        self.walljump_image = pygame.transform.scale(self.walljump_image, (TILESIZE, TILESIZE))
        self.dash_image = pygame.image.load('dash.png').convert_alpha()
        self.dash_image = pygame.transform.scale(self.dash_image, (TILESIZE, TILESIZE))
        self.grave_image = pygame.image.load('grave.PNG').convert_alpha()
        self.grave_image = pygame.transform.scale(self.grave_image, (24, 32))
        self.grave2_image = pygame.image.load('grave2.PNG').convert_alpha()
        self.grave2_image = pygame.transform.scale(self.grave2_image, (64, 32))
        self.cross_image = pygame.image.load('cross.PNG').convert_alpha()
        self.cross_image = pygame.transform.scale(self.cross_image,
                                                  (self.cross_image.get_width(), self.cross_image.get_height()))
        self.fence_image = pygame.image.load('fence.PNG').convert_alpha()
        self.fence_image = pygame.transform.scale(self.fence_image, (32, 32))
        self.tabliczka = pygame.image.load('tabliczka.png').convert_alpha()
        self.tabliczka = pygame.transform.scale(self.tabliczka,
                                                (self.tabliczka.get_width(), self.tabliczka.get_height()))
        self.gates = pygame.image.load('gates.PNG').convert_alpha()
        self.gates = pygame.transform.scale(self.gates, (self.gates.get_width(), self.gates.get_height()))
        self.heart_image = pygame.image.load('lives.PNG').convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (TILESIZE, TILESIZE))
        self.start_screen = pygame.image.load('start_screen.PNG').convert_alpha()
        self.start_screen = pygame.transform.scale(self.start_screen, (WIDTH, HEIGHT))
        self.title = pygame.image.load('title3.PNG').convert_alpha()
        self.title = pygame.transform.scale(self.title, (self.title.get_width(), self.title.get_height()))
        self.game_over = pygame.image.load('game_over2.png').convert_alpha()
        self.game_over = pygame.transform.scale(self.game_over, (WIDTH, HEIGHT))
        self.napis_startowy = pygame.image.load('napis_startowy1.PNG').convert_alpha()
        self.napis_startowy = pygame.transform.scale(self.napis_startowy, (474, 24))
        self.sword = pygame.image.load('sword.PNG').convert_alpha()
        self.sword = pygame.transform.scale(self.sword, (45, 45))
        self.spike1 = pygame.image.load('spikes_up.png').convert_alpha()
        self.spike1 = pygame.transform.scale(self.spike1, (self.spike1.get_width(), self.spike1.get_height()))
        self.spike2 = pygame.image.load('spikes_down.png').convert_alpha()
        self.spike2 = pygame.transform.scale(self.spike2, (self.spike2.get_width(), self.spike2.get_height()))
        self.spike3 = pygame.image.load('spikes_left.png').convert_alpha()
        self.spike3 = pygame.transform.scale(self.spike3, (self.spike3.get_width(), self.spike3.get_height()))
        self.spike4 = pygame.image.load('spikes_right.png').convert_alpha()
        self.spike4 = pygame.transform.scale(self.spike4, (self.spike3.get_width(), self.spike3.get_height()))
        self.maczuga = pygame.image.load('maczuga1.png').convert_alpha()
        self.maczuga = pygame.transform.scale(self.maczuga, (self.maczuga.get_width(), self.maczuga.get_height()))
        self.miecz = pygame.image.load('miecz1.png').convert_alpha()
        self.miecz = pygame.transform.scale(self.miecz, (self.miecz.get_width(), self.miecz.get_height()))
        self.kusza = pygame.image.load('crossbow.png').convert_alpha()
        self.kusza = pygame.transform.scale(self.kusza, (self.kusza.get_width(), self.kusza.get_height()))
        self.flying_right = pygame.image.load('flying_right.PNG').convert_alpha()
        self.flying_right = pygame.transform.scale(self.flying_right,
                                                   (self.flying_right.get_width(), self.flying_right.get_height()))
        self.flying_left = pygame.image.load('flying_left.PNG').convert_alpha()
        self.flying_left = pygame.transform.scale(self.flying_left,
                                                  (self.flying_left.get_width(), self.flying_left.get_height()))

    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.bolts = pygame.sprite.Group()
        self.levels = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.camera = Camera(len(self.map_data[0] * TILESIZE), len(self.map_data) * TILESIZE)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "8":
                    Wall4(self, col, row)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "2":
                    Wall2(self, col, row)
                if tile == "7":
                    Wall3(self, col, row)
                if tile == "9":
                    Pochodnia(self, col, row)
                if tile == "S":
                    Sneakers(self, col, row)
                if tile == "W":
                    Walljump(self, col, row)
                if tile == "D":
                    Dash(self, col, row)
                if tile == "H":
                    Lives(self, col, row)
                if tile == "K":
                    Maczuga(self, col, row)
                if tile == "B":
                    Miecz(self, col, row)
                if tile == "A":
                    Kusza(self, col, row)
                if tile == "T":
                    Tabliczka(self, col, row)
                if tile == "L":
                    Level(self, col, row)
                if tile == "X":
                    Checkpoint(self, col, row)
                if tile == "E":
                    Potion1(self, col, row)
                if tile == "I":
                    Potion2(self, col, row)
                if tile == "N":
                    Potion3(self, col, row)
                if tile == "U":
                    Key(self, col, row)
                if tile == "Y":
                    Cross(self, col, row)
                if tile == "G":
                    Grave(self, col, row)
                if tile == "C":
                    Grave2(self, col, row)
                if tile == "O":
                    Door(self, col, row)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    self.player = Player(self, col, row)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'Z':
                    Mob2(self, col, row)
                if tile == "J":
                    Mob3(self, col, row)
                if tile == "R":
                    Wall5(self, col, row)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "V":
                    Gates(self, col, row)
                if tile == "Q":
                    Mob4(self, col, row)
                if tile == "F":
                    Fence(self, col, row)
                if tile == "3":
                    Spikes1(self, col, row)
                if tile == "4":
                    Spikes2(self, col, row)
                if tile == "5":
                    Spikes3(self, col, row)
                if tile == "6":
                    Spikes4(self, col, row)


    def run(self):
        # Game Loop
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def update(self):
        # Game Loop update
        self.all_sprites.update()
        self.camera.update(self.player)

        if self.player.lives == -1:
            for sprite in self.all_sprites:
                sprite.kill()
                self.playing = False

    def event(self):
        # Game Loop events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.player.rect.x -= 1
                    hits = pygame.sprite.spritecollide(self.player, self.walls, False)
                    self.player.rect.x += 2
                    hits2 = pygame.sprite.spritecollide(self.player, self.walls, False)
                    self.player.rect.x -= 1
                    if self.player.vel.y == 0 and not self.player.isJumping and not self.player.isCrouching:
                        self.player.jump()
                    elif self.player.hasWalljump and (hits or hits2):
                        self.player.wall_jump()
                    elif not self.player.isDoubleJumping and self.player.hasSneakers and not self.player.isCrouching:
                        self.player.double_jump()
                if event.key == pygame.K_LCTRL:
                    if self.player.vel.y == 0:
                        self.player.pos.y += 16
                        if self.player.moving_right:
                            self.player.image = self.player_crouch_right
                        else:
                            self.player.image = self.player_crouch_left
                        self.player.hit_box = PLAYER_HIT_BOX_PRZYKUC.copy()
                        self.player.isCrouching = True
                        self.player.isHoldingControl = True
                        self.player.rect = self.player.image.get_rect()
                if event.key == pygame.K_e:
                    if not self.player.isCrouching:
                        self.player.r_dash()
                if event.key == pygame.K_q:
                    if not self.player.isCrouching:
                        self.player.l_dash()
                if event.key == pygame.K_h:
                    if self.player.isMaczuga or self.player.isMiecz or self.player.isKusza:
                        if self.player.weapon_select == 0 or self.player.weapon_select == 1:
                            self.player.attack = True
                        elif self.player.weapon_select == 2 and not self.player.fired:
                            self.player.fired = True
                            Bolt(self)
                if event.key == pygame.K_1 and self.player.isMiecz:
                    self.player.weapon_select = 0
                    if self.player.image == self.player_right_miecz or self.player.image == self.player_right_maczuga or self.player.image == self.player_right or self.player_attack_right_miecz or self.player_attack_right_maczuga:
                        self.player.image = self.player_right_miecz
                    else:
                        self.player.image = self.player_left_miecz
                if event.key == pygame.K_2 and self.player.isMaczuga:
                    self.player.weapon_select = 1
                    if self.player.image == self.player_right_maczuga or self.player.image == self.player_right_miecz or self.player.image == self.player_right or self.player_attack_right_miecz or self.player_attack_right_maczuga:
                        self.player.image = self.player_right_maczuga
                    else:
                        self.player.image = self.player_left_maczuga
                if event.key == pygame.K_3 and self.player.isKusza:
                    self.player.weapon_select = 2
                    if self.player.image == self.player_right_maczuga or self.player.image == self.player_right_miecz or self.player.image == self.player_right or self.player_attack_right_miecz or self.player_attack_right_maczuga:
                        self.player.image = self.player_right
                    else:
                        self.player.image = self.player_left
                if event.key == pygame.K_x:
                    change_map()
                    self.load_data()
                    self.new()
                    self.player.hasSneakers = True
                    self.player.hasDash = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.player.isHoldingControl = False

            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw_exp(self):
        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        text1 = myfont.render(str(self.player.exp), False, WHITE)
        text2 = myfont.render("/", False, WHITE)
        text3 = myfont.render(str(self.player.max_exp), False, WHITE)
        screen.blit(text1, (40, 40))
        screen.blit(text2, (60, 40))
        screen.blit(text3, (70, 40))

    def draw_health(self):
        myfont = pygame.font.SysFont('Comic Sans MS', 15)
        text1 = myfont.render(str(self.player.health), False, WHITE)
        text2 = myfont.render("/", False, WHITE)
        text3 = myfont.render(str(self.player.max_health), False, WHITE)
        screen.blit(text1, (60, 10))
        screen.blit(text2, (85, 10))
        screen.blit(text3, (95, 10))

    def draw_level(self):
        myfont = pygame.font.SysFont('Comic Sans MS', 15)
        text1 = myfont.render("Level: ", False, WHITE)
        text2 = myfont.render(str(self.player.level), False, WHITE)
        screen.blit(text1, (120, 36))
        screen.blit(text2, (170, 36))

    def draw(self):
        if game_map == 'map1.txt' or game_map == 'map2.txt':
            self.screen.blit(self.tlo, (0, 0))
        elif game_map == 'map3.txt':
            self.screen.blit(self.tlo2, (0, 0))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.screen, 10, 10, self.player.health / self.player.max_health)
        draw_player_exp(self.screen, 10, 40, self.player.exp / self.player.max_exp)
        self.draw_exp()
        self.draw_health()
        self.draw_level()
        draw_player_lives(self.player.lives)
        draw_player_icons(self)
        pygame.display.update((0, 0, WIDTH, HEIGHT))

    def show_start_screen(self):
        # game splash/start screen
        self.screen.blit(self.start_screen, (0, 0))
        self.screen.blit(self.title, (100, 100))
        self.screen.blit(self.napis_startowy, (150, 300))
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.running = False

    def show_go_screen(self):
        # game over/continue
        global game_map
        if not self.running:
            return
        self.screen.blit(self.game_over, (0, 0))
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        waiting = False
                        self.running = True
                        self.playing = True
                        game_map = 'map1.txt'
                        self.load_data()
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.running = False

    def change_level(self):
        self.temp_exp = self.player.exp
        self.temp_level = self.player.level
        self.temp_weapon = self.player.weapon_select
        self.temp_lives = self.player.lives
        change_map()
        self.load_data()
        self.new()
        self.player.level = self.temp_level
        self.player.exp = self.temp_exp
        self.player.max_health = 100 + 50 * (self.player.level - 1)
        self.player.health = self.player.max_health
        self.player.max_exp = 500 + 100 * (self.player.level - 1)
        self.player.weapon_select = self.temp_weapon
        self.player.lives = self.temp_lives
        if game_map == "map2.txt" or game_map == "map3.txt":
            self.player.isKusza = True
            self.player.isMaczuga = True
            self.player.hasSneakers = True

        if game_map == "map3.txt":
            self.player.isKusza = True
            self.player.isMaczuga = True
            self.player.hasSneakers = True
            self.player.hasWalljump = True
            self.player.hasDash = True


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pygame.quit()