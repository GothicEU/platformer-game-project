import os

from sprites import *


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
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
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, GRAY, outline_rect, 2)


def draw_player_lives(surf, x, y, pct):
    x = 0
    while pct > 0:
        screen.blit(heart, (120 + x, 10))
        pct -= 1
        x += 40


class Game:
    def __init__(self):
        # intialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
        pygame.display.update()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
        self.running = True
        self.playing = True
        self.font_name = pygame.font.match_font(FONT_NAME)

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        self.map_data = []
        with open(os.path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.tlo = pygame.image.load('tlo2.PNG').convert_alpha()
        self.tlo = pygame.transform.scale(self.tlo, (WIDTH, HEIGHT))
        self.dirt_image = pygame.image.load('dirt.PNG').convert_alpha()
        self.dirt_image = pygame.transform.scale(self.dirt_image, (TILESIZE, TILESIZE))
        self.grass_image = pygame.image.load('grass.PNG').convert_alpha()
        self.grass_image = pygame.transform.scale(self.grass_image, (TILESIZE, TILESIZE))
        self.mob_right = pygame.image.load('mob_right.PNG').convert_alpha()
        self.mob_right = pygame.transform.scale(self.mob_right,(self.mob_right.get_width(), self.mob_right.get_height()))
        self.mob_left = pygame.image.load('mob_left.PNG').convert_alpha()
        self.mob_left = pygame.transform.scale(self.mob_left, (self.mob_left.get_width(), self.mob_left.get_height()))
        self.zombie_right = pygame.image.load('zombie_right.PNG').convert_alpha()
        self.zombie_right = pygame.transform.scale(self.zombie_right,(self.zombie_right.get_width(), self.zombie_right.get_height()))
        self.zombie_left = pygame.image.load('zombie_left.PNG').convert_alpha()
        self.zombie_left = pygame.transform.scale(self.zombie_left,(self.zombie_left.get_width(), self.zombie_left.get_height()))
        self.player_right = pygame.image.load('right.PNG').convert_alpha()
        self.player_right = pygame.transform.scale(self.player_right,(self.player_right.get_width(), self.player_right.get_height()))
        self.player_left = pygame.image.load('left.PNG').convert_alpha()
        self.player_left = pygame.transform.scale(self.player_left,(self.player_left.get_width(), self.player_left.get_height()))
        self.player_crouch_right = pygame.image.load('crouch_right.PNG').convert_alpha()
        self.player_crouch_right = pygame.transform.scale(self.player_crouch_right, (
        self.player_crouch_right.get_width(), self.player_crouch_right.get_height()))
        self.player_crouch_left = pygame.image.load('crouch_left.PNG').convert_alpha()
        self.player_crouch_left = pygame.transform.scale(self.player_crouch_left, (
        self.player_crouch_left.get_width(), self.player_crouch_left.get_height()))
        self.player_attack_right = pygame.image.load('right_attack.PNG').convert_alpha()
        self.player_attack_right = pygame.transform.scale(self.player_attack_right,(55, 64))
        self.player_attack_left = pygame.image.load('left_attack.PNG').convert_alpha()
        self.player_attack_left = pygame.transform.scale(self.player_attack_left, (55, 64))
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
        self.fence_image = pygame.image.load('fence.PNG').convert_alpha()
        self.fence_image = pygame.transform.scale(self.fence_image, (32, 32))
        self.heart_image = pygame.image.load('lives.PNG').convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (TILESIZE, TILESIZE))
        self.start_screen = pygame.image.load('start_screen.PNG').convert_alpha()
        self.start_screen = pygame.transform.scale(self.start_screen, (WIDTH, HEIGHT))
        self.title = pygame.image.load('title3.PNG').convert_alpha()
        self.title = pygame.transform.scale(self.title, (self.title.get_width(), self.title.get_height()))
        self.napis_startowy = pygame.image.load('napis_startowy1.PNG').convert_alpha()
        self.napis_startowy = pygame.transform.scale(self.napis_startowy, (474, 24))
        self.sword = pygame.image.load('sword.PNG').convert_alpha()
        self.sword = pygame.transform.scale(self.sword, (45, 45))

    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.camera = Camera(len(self.map_data[0] * TILESIZE), len(self.map_data) * TILESIZE)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile=="1":
                    Wall(self, col, row)
                if tile=="2":
                    Wall2(self, col, row)
                if tile=="P":
                    self.player = Player(self, col, row)
                if tile=='M':
                    Mob(self, col, row)
                if tile=='Z':
                    Mob2(self, col, row)
                if tile=="S":
                    Sneakers(self, col, row)
                if tile=="W":
                    Walljump(self, col, row)
                if tile=="D":
                    Dash(self, col, row)
                if tile=="G":
                    Grave(self, col, row)
                if tile=="H":
                    Lives(self, col, row)
                if tile=="C":
                    Grave2(self, col, row)
                if tile=="F":
                    Fence(self, col, row)

    def run(self):
        # Game Loop
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.clock.tick(FPS)
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
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key==pygame.K_SPACE:
                    self.player.rect.x += 1
                    hits = pygame.sprite.spritecollide(self.player, self.walls, False)
                    self.player.rect.x -= 2
                    hits2 = pygame.sprite.spritecollide(self.player, self.walls, False)
                    self.player.rect.x += 1
                    if self.player.vel.y!=0 and not self.player.isWallJumping and (hits or hits2):
                        self.player.wall_jump()
                    elif self.player.vel.y==0 and not self.player.isCrouching and not self.player.isJumping:
                        self.player.jump()
                    else:
                        self.player.double_jump()

                if event.key==pygame.K_LCTRL:
                    if self.player.vel.y==0:
                        self.player.pos.y += 16
                        if self.player.moving_right:
                            self.player.image = self.player_crouch_right
                        else:
                            self.player.image = self.player_crouch_left
                        self.player.hit_box = PLAYER_HIT_BOX_PRZYKUC.copy()
                        self.player.isCrouching = True
                        self.player.isHoldingControl = True
                        self.player.rect = self.player.image.get_rect()
                if event.key==pygame.K_e:
                    self.player.r_dash()
                if event.key==pygame.K_q:
                    self.player.l_dash()
                if event.key==pygame.K_h:
                    self.player.attack = True

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LCTRL:
                    self.player.isHoldingControl = False

            if event.type==pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop draw
        self.screen.blit(self.tlo, (0, 0))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        draw_player_lives(self.screen, 50, 10, self.player.lives)
        pygame.display.flip()

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
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_RETURN:
                        waiting = False
                    if event.key==pygame.K_ESCAPE:
                        waiting = False
                        self.running = False

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("KONIEC GRY", 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Nacisnij Enter, zeby sprobowac ponowanie", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_RETURN:
                        waiting = False
                        self.running = True
                        self.playing = True
                    if event.key==pygame.K_ESCAPE:
                        waiting = False
                        self.running = False


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pygame.quit()
