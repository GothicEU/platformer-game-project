import pygame
from sprites import *

# kolizje, zmienne do wartosci konfiguracyjnych, grafik, pelen ekran
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platform Game")
        self.clock = pygame.time.Clock()
        self.tlo = pygame.image.load('tlo.PNG')
        self.walkRight = pygame.image.load('first.PNG')
        self.walkLeft = pygame.image.load('first1.PNG')
        self.running = True

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(WIDTH / 2 - 50, HEIGHT * 3 / 5, 100, 20)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
        p3 = Platform(WIDTH + 50, HEIGHT * 3 / 5, 100, 20)
        self.all_sprites.add(p3)
        self.platforms.add(p3)
        p4 = Platform(WIDTH + 200, HEIGHT * 2 / 5, 100, 20)
        self.all_sprites.add(p4)
        self.platforms.add(p4)
        p5 = Platform(WIDTH + 300, HEIGHT / 5, 100, 20)
        self.all_sprites.add(p5)
        self.platforms.add(p5)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            if self.player.vel.y > 0:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0
            else:
                self.player.vel.y *= -1

                

        if self.player.rect.right > WIDTH / 2:
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            for plat in self.platforms:
                plat.rect.right -= max(abs(self.player.vel.x), 2)
        if self.player.rect.left < WIDTH / 2:
            self.player.pos.x += max(abs(self.player.vel.x), 2)
            for plat in self.platforms:
                plat.rect.right += max(abs(self.player.vel.x), 2)
        if self.player.rect.top <= HEIGHT / 3:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.top += max(abs(self.player.vel.y), 2)
        if self.player.rect.bottom > HEIGHT / 1.2:
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.bottom -= max(abs(self.player.vel.y), 2)
    def events(self):
        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):

        self.screen.blit(self.tlo, (0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_gameover_screen()

pygame.quit()
