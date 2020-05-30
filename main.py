import os

from sprites import *
from graphics import *

game_map = 'map1.txt'


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
    elif game_map == 'map5.txt':
        game_map = 'credits.txt'


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def draw_player_icons(game):
    if game.player.isMiecz:
        game.screen.blit(miecz, (1088, 688))
    if game.player.isMaczuga:
        game.screen.blit(maczuga, (1120, 688))
    if game.player.isKusza:
        game.screen.blit(kusza, (1152, 688))
    if game.player.hasSneakers:
        game.screen.blit(sneakers_image, (1184, 688))
    if game.player.hasDash:
        game.screen.blit(dash_image, (1216, 688))
    if game.player.hasWalljump:
        game.screen.blit(walljump_image, (1248, 688))


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
        self.player_image = player_right

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.cannon_balls = pygame.sprite.Group()
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
                if tile == "?":
                    Grave3(self, col, row)
                if tile == "O":
                    Door(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'Z':
                    Mob2(self, col, row)
                if tile == "Q":
                    Mob4(self, col, row)
                if tile == "J":
                    Mob3(self, col, row)
                if tile == "-":
                    Cannon_right(self, col, row)
                if tile == "+":
                    Cannon_left(self, col, row)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    self.player = Player(self, col, row)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "R":
                    Wall5(self, col, row)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "V":
                    Gates(self, col, row)
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
                if tile == "a":
                    Credits(self, col, row)

    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        if self.player.lives == -1:
            for sprite in self.all_sprites:
                sprite.kill()
                self.playing = False

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.player.rect.x -= 1
                    hits = pygame.sprite.spritecollide(self.player, self.walls, False, pygame.sprite.collide_mask)
                    self.player.rect.x += 2
                    hits2 = pygame.sprite.spritecollide(self.player, self.walls, False, pygame.sprite.collide_mask)
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
                        if self.player.image == player_right or self.player.image == player_attack_right_maczuga or self.player.image == player_attack_right_miecz or self.player.image == player_right_maczuga or self.player.image == player_right_miecz:
                            self.player.image = player_crouch_right
                        else:
                            self.player.image = player_crouch_left
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
                if event.key == pygame.K_2 and self.player.isMiecz and not self.player.isCrouching:
                    self.player.weapon_select = 0
                    if self.player.image == player_right or self.player.image == player_attack_right_maczuga or self.player.image == player_attack_right_miecz or self.player.image == player_right_maczuga or self.player.image == player_right_miecz:
                        self.player.image = player_right_miecz
                    else:
                        self.player.image = player_left_miecz
                if event.key == pygame.K_1 and self.player.isMaczuga and not self.player.isCrouching:
                    self.player.weapon_select = 1
                    if self.player.image == player_right or self.player.image == player_attack_right_maczuga or self.player.image == player_attack_right_miecz or self.player.image == player_right_maczuga or self.player.image == player_right_miecz:
                        self.player.image = player_right_maczuga
                    else:
                        self.player.image = player_left_maczuga
                if event.key == pygame.K_3 and self.player.isKusza and not self.player.isCrouching:
                    self.player.weapon_select = 2
                    if self.player.image == player_right or self.player.image == player_attack_right_maczuga or self.player.image == player_attack_right_miecz or self.player.image == player_right_maczuga or self.player.image == player_right_miecz:
                        self.player.image = player_right
                    else:
                        self.player.image = player_left
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
        if game_map == 'map1.txt' or game_map == 'map2.txt' or game_map == 'map5.txt':
            self.screen.blit(tlo, (0, 0))
        elif game_map == 'map3.txt' or game_map == 'map4.txt':
            self.screen.blit(tlo2, (0, 0))
        elif game_map == 'credits.txt':
            screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if game_map != 'credits.txt':
            draw_player_health(self.screen, 10, 10, self.player.health / self.player.max_health)
            draw_player_exp(self.screen, 10, 40, self.player.exp / self.player.max_exp)
            self.draw_exp()
            self.draw_health()
            self.draw_level()
            draw_player_lives(self.player.lives)
            draw_player_icons(self)
        pygame.display.update((0, 0, WIDTH, HEIGHT))

    def show_start_screen(self):
        self.screen.blit(start_screen, (0, 0))
        self.screen.blit(title, (100, 100))
        self.screen.blit(napis_startowy, (150, 300))
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
        global game_map
        if not self.running:
            return
        self.screen.blit(game_over, (0, 0))
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
        if game_map != "credits.txt":
            self.player.level = self.temp_level
            self.player.exp = self.temp_exp
            self.player.max_health = 100 + 20 * (self.player.level - 1)
            self.player.health = self.player.max_health
            self.player.max_exp = 500 + 100 * (self.player.level - 1)
            self.player.weapon_select = self.temp_weapon
            self.player.lives = self.temp_lives
            if game_map == "map2.txt":
                self.player.isKusza = True
                self.player.isMaczuga = True
                self.player.hasSneakers = True

            if game_map == "map3.txt":
                self.player.isKusza = True
                self.player.isMaczuga = True
                self.player.hasSneakers = True
                self.player.hasWalljump = True
                self.player.hasDash = True

            if game_map == "map4.txt" or game_map == "map5.txt":
                self.player.isMiecz = True
                self.player.isKusza = True
                self.player.isMaczuga = True
                self.player.hasSneakers = True
                self.player.hasWalljump = True
                self.player.hasDash = True

            if self.player.weapon_select == 0:
                self.player.image = player_right_miecz
            elif self.player.weapon_select == 1:
                self.player.image = player_right_maczuga
            elif self.player.weapon_select == 2:
                self.player.image = player_right

    def exit_game(self):
        waiting = True
        self.screen.blit(end_screen, (0, 0))
        pygame.display.flip()
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.playing = False
                        self.running = False


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pygame.quit()
