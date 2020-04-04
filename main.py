from sys import path

from sprites import *

from os import path

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


class Game:
    def __init__(self):
        # intialize game window, etc
        self.falling = True
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1280, 720),pygame.FULLSCREEN)
        pygame.display.update()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
        self.crouching = False
        self.running = True

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.grass_image = pygame.image.load('grass.PNG').convert_alpha()
        self.grass_image = pygame.transform.scale(self.grass_image, (TILESIZE, TILESIZE))
        self.dirt_image = pygame.image.load('dirt.PNG').convert_alpha()
        self.dirt_image = pygame.transform.scale(self.dirt_image, (TILESIZE, TILESIZE))

    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "2":
                    Wall2(self,col,row)
                if tile == "P":
                    self.player = Player(self, col, row)

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()

    def update(self):
        # Game Loop update
        self.all_sprites.update()
        print(self.player.pos)

    def event(self):
        # Game Loop events

        if self.player.pos.y >= HEIGHT:
            self.player.pos = self.player.resp

        for event in pygame.event.get():

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False

                if event.key==pygame.K_SPACE:
                    if self.crouching == False:
                        if self.crouching == False:
                            self.player.jump()

                if event.key==pygame.K_LCTRL:
                    if self.player.vel.y == 0:
                        if self.player.vel.x < 1:
                            self.player.pos.y += 16
                            self.player.image = player_crouch
                            self.player.hit_box = PLAYER_HIT_BOX_PRZYKUC
                            self.crouching = True
                            self.player.rect = self.player.image.get_rect()


            if event.type==pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LCTRL:
                    self.player.image = player_right
                    self.player.hit_box = PLAYER_HIT_BOX
                    self.crouching = False
                    self.player.rect = self.player.image.get_rect()



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
