import os

from sprites import *


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


class Game:
    def __init__(self):
        # intialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
        self.running = True
        self.playing = True

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        self.map_data = []
        with open(os.path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.dirt_image = pygame.image.load('dirt.PNG').convert_alpha()
        self.dirt_image = pygame.transform.scale(self.dirt_image, (TILESIZE, TILESIZE))
        self.grass_image = pygame.image.load('grass.PNG').convert_alpha()
        self.grass_image = pygame.transform.scale(self.grass_image, (TILESIZE, TILESIZE))

    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "2":
                    Wall2(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)

    def run(self):
        # Game Loop
        while self.playing:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def update(self):
        # Game Loop update
        self.all_sprites.update()
        self.player.draw_health()

    def event(self):
        # Game Loop events
        if self.player.pos[1] > HEIGHT:
            self.player.fall()
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.player.rect.y += 1
                    hits = pygame.sprite.spritecollide(self.player, self.walls, False)
                    self.player.rect.y -= 1
                    if not self.player.isCrouching and not self.player.isJumping and hits:
                        self.player.jump()
                    else:
                        self.player.double_jump()
                if event.key == pygame.K_LCTRL:
                    if self.player.vel.y == 0:
                        if self.player.vel.x < 1:
                            self.player.pos.y += 16
                            self.player.image = player_crouch
                            self.player.hit_box = PLAYER_HIT_BOX_PRZYKUC
                            self.player.isCrouching = True
                            self.player.isHoldingControl = True
                            self.player.rect = self.player.image.get_rect()
                if event.key == pygame.K_e:
                    self.player.r_dash()
                if event.key == pygame.K_q:
                    self.player.l_dash()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.player.isHoldingControl = False

            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop draw
        self.screen.blit(tlo, (0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        # Game start screen
        pass

    def show_go_screen(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pygame.quit()