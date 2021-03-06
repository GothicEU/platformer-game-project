from settings import *

end_screen = pygame.image.load('graphics/end_screen.png')
end_screen = pygame.transform.scale(end_screen, (WIDTH, HEIGHT))
credits = pygame.image.load('graphics/credits.PNG').convert_alpha()
credits = pygame.transform.scale(credits, (credits.get_width(), credits.get_height()))
ghost_left = pygame.image.load('graphics/ghost_left.PNG').convert_alpha()
ghost_left = pygame.transform.scale(ghost_left, (ghost_left.get_width(), ghost_left.get_height()))
ghost_right = pygame.image.load('graphics/ghost_right.PNG').convert_alpha()
ghost_right = pygame.transform.scale(ghost_right, (ghost_right.get_width(), ghost_right.get_height()))
dirt2_image = pygame.image.load('graphics/dirt2.PNG').convert_alpha()
dirt2_image = pygame.transform.scale(dirt2_image, (dirt2_image.get_width(), dirt2_image.get_height()))
checkpoint = pygame.image.load('graphics/checkpoint.png').convert_alpha()
checkpoint = pygame.transform.scale(checkpoint, (checkpoint.get_width(), checkpoint.get_height()))
level = pygame.image.load('graphics/level.png').convert_alpha()
level = pygame.transform.scale(level, (TILESIZE, TILESIZE))
potion1 = pygame.image.load('graphics/hp.png').convert_alpha()
potion1 = pygame.transform.scale(potion1, (TILESIZE, TILESIZE))
potion2 = pygame.image.load('graphics/exp2.png').convert_alpha()
potion2 = pygame.transform.scale(potion2, (TILESIZE, TILESIZE))
potion3 = pygame.image.load('graphics/ws.png').convert_alpha()
potion3 = pygame.transform.scale(potion3, (TILESIZE, TILESIZE))
key = pygame.image.load('graphics/key.PNG').convert_alpha()
key = pygame.transform.scale(key, (TILESIZE, TILESIZE))
bolt = pygame.image.load('graphics/bolt.png').convert_alpha()
bolt = pygame.transform.scale(bolt, (bolt.get_width(), bolt.get_height()))
bolt2 = pygame.image.load('graphics/bolt2.png').convert_alpha()
bolt2 = pygame.transform.scale(bolt2, (bolt2.get_width(), bolt2.get_height()))
spike1 = pygame.image.load('graphics/spikes_up.png').convert_alpha()
spike1 = pygame.transform.scale(spike1, (spike1.get_width(), spike1.get_height()))
spike2 = pygame.image.load('graphics/spikes_down.png').convert_alpha()
spike2 = pygame.transform.scale(spike2, (spike2.get_width(), spike2.get_height()))
spike3 = pygame.image.load('graphics/spikes_left.png').convert_alpha()
spike3 = pygame.transform.scale(spike3, (spike3.get_width(), spike3.get_height()))
spike4 = pygame.image.load('graphics/spikes_right.png').convert_alpha()
spike4 = pygame.transform.scale(spike4, (spike3.get_width(), spike3.get_height()))
tlo = pygame.image.load('graphics/tlo2.PNG').convert_alpha()
tlo = pygame.transform.scale(tlo, (WIDTH, HEIGHT))
tlo2 = pygame.image.load('graphics/test1.PNG').convert_alpha()
tlo2 = pygame.transform.scale(tlo2, (WIDTH, HEIGHT))
dirt_image = pygame.image.load('graphics/dirt.PNG').convert_alpha()
dirt_image = pygame.transform.scale(dirt_image, (TILESIZE, TILESIZE))
brick1_image = pygame.image.load('graphics/brick.PNG').convert_alpha()
brick1_image = pygame.transform.scale(brick1_image, (TILESIZE, TILESIZE))
pochodnia_image = pygame.image.load('graphics/pochodnia.PNG').convert_alpha()
pochodnia_image = pygame.transform.scale(pochodnia_image, (32, 64))
grass_image = pygame.image.load('graphics/grass.PNG').convert_alpha()
door1 = pygame.image.load('graphics/door1.PNG').convert_alpha()
door1 = pygame.transform.scale(door1, (9, 64))
door2 = pygame.image.load('graphics/door2.PNG').convert_alpha()
door2 = pygame.transform.scale(door2, (32, 64))
grass_image = pygame.transform.scale(grass_image, (TILESIZE, TILESIZE))
mob_right = pygame.image.load('graphics/mob_right.PNG').convert_alpha()
mob_right = pygame.transform.scale(mob_right, (mob_right.get_width(), mob_right.get_height()))
mob_left = pygame.image.load('graphics/mob_left.PNG').convert_alpha()
mob_left = pygame.transform.scale(mob_left, (mob_left.get_width(), mob_left.get_height()))
zombie_right = pygame.image.load('graphics/zombie_right.PNG').convert_alpha()
zombie_right = pygame.transform.scale(zombie_right, (zombie_right.get_width(), zombie_right.get_height()))
zombie_left = pygame.image.load('graphics/zombie_left.PNG').convert_alpha()
zombie_left = pygame.transform.scale(zombie_left, (zombie_left.get_width(), zombie_left.get_height()))
player_right = pygame.image.load('graphics/right.PNG').convert_alpha()
player_right = pygame.transform.scale(player_right, (player_right.get_width(), player_right.get_height()))
player_left = pygame.image.load('graphics/left.PNG').convert_alpha()
player_left = pygame.transform.scale(player_left, (player_left.get_width(), player_left.get_height()))
player_right_maczuga = pygame.image.load('graphics/right_maczuga.PNG').convert_alpha()
player_right_maczuga = pygame.transform.scale(player_right_maczuga, (55, 64))
player_left_maczuga = pygame.image.load('graphics/left_maczuga.PNG').convert_alpha()
player_left_maczuga = pygame.transform.scale(player_left_maczuga, (55, 64))
player_right_miecz = pygame.image.load('graphics/right_miecz.PNG').convert_alpha()
player_right_miecz = pygame.transform.scale(player_right_miecz, (55, 64))
player_left_miecz = pygame.image.load('graphics/left_miecz.PNG').convert_alpha()
player_left_miecz = pygame.transform.scale(player_left_miecz, (55, 64))
player_crouch_right = pygame.image.load('graphics/crouch_right.PNG').convert_alpha()
player_crouch_right = pygame.transform.scale(player_crouch_right, (player_crouch_right.get_width(), player_crouch_right.get_height()))
player_crouch_left = pygame.image.load('graphics/crouch_left.PNG').convert_alpha()
player_crouch_left = pygame.transform.scale(player_crouch_left, (player_crouch_left.get_width(), player_crouch_left.get_height()))
player_attack_right_miecz = pygame.image.load('graphics/right_attack_miecz.PNG').convert_alpha()
player_attack_right_miecz = pygame.transform.scale(player_attack_right_miecz, (55, 64))
player_attack_left_miecz = pygame.image.load('graphics/left_attack_miecz.PNG').convert_alpha()
player_attack_left_miecz = pygame.transform.scale(player_attack_left_miecz, (55, 64))
player_attack_right_maczuga = pygame.image.load('graphics/right_attack_maczuga.PNG').convert_alpha()
player_attack_right_maczuga = pygame.transform.scale(player_attack_right_maczuga, (55, 64))
player_attack_left_maczuga = pygame.image.load('graphics/left_attack_maczuga.PNG').convert_alpha()
player_attack_left_maczuga = pygame.transform.scale(player_attack_left_maczuga, (55, 64))
sneakers_image = pygame.image.load('graphics/sneakers.png').convert_alpha()
sneakers_image = pygame.transform.scale(sneakers_image, (TILESIZE, TILESIZE))
walljump_image = pygame.image.load('graphics/walljump.png').convert_alpha()
walljump_image = pygame.transform.scale(walljump_image, (TILESIZE, TILESIZE))
dash_image = pygame.image.load('graphics/dash.png').convert_alpha()
dash_image = pygame.transform.scale(dash_image, (TILESIZE, TILESIZE))
grave_image = pygame.image.load('graphics/grave.PNG').convert_alpha()
grave_image = pygame.transform.scale(grave_image, (24, 32))
grave2_image = pygame.image.load('graphics/grave2.PNG').convert_alpha()
grave2_image = pygame.transform.scale(grave2_image, (64, 32))
cross_image = pygame.image.load('graphics/cross.PNG').convert_alpha()
cross_image = pygame.transform.scale(cross_image, (cross_image.get_width(), cross_image.get_height()))
fence_image = pygame.image.load('graphics/fence.PNG').convert_alpha()
fence_image = pygame.transform.scale(fence_image, (32, 32))
tabliczka = pygame.image.load('graphics/tabliczka.png').convert_alpha()
tabliczka = pygame.transform.scale(tabliczka, (tabliczka.get_width(), tabliczka.get_height()))
gates = pygame.image.load('graphics/gates.PNG').convert_alpha()
gates = pygame.transform.scale(gates, (gates.get_width(), gates.get_height()))
heart_image = pygame.image.load('graphics/lives.PNG').convert_alpha()
heart_image = pygame.transform.scale(heart_image, (TILESIZE, TILESIZE))
start_screen = pygame.image.load('graphics/start_screen.PNG').convert_alpha()
start_screen = pygame.transform.scale(start_screen, (WIDTH, HEIGHT))
title = pygame.image.load('graphics/title3.PNG').convert_alpha()
title = pygame.transform.scale(title, (title.get_width(), title.get_height()))
game_over = pygame.image.load('graphics/game_over2.png').convert_alpha()
game_over = pygame.transform.scale(game_over, (WIDTH, HEIGHT))
napis_startowy = pygame.image.load('graphics/napis_startowy1.PNG').convert_alpha()
napis_startowy = pygame.transform.scale(napis_startowy, (474, 24))
sword = pygame.image.load('graphics/sword.PNG').convert_alpha()
sword = pygame.transform.scale(sword, (45, 45))
spike1 = pygame.image.load('graphics/spikes_up.png').convert_alpha()
spike1 = pygame.transform.scale(spike1, (spike1.get_width(), spike1.get_height()))
spike2 = pygame.image.load('graphics/spikes_down.png').convert_alpha()
spike2 = pygame.transform.scale(spike2, (spike2.get_width(), spike2.get_height()))
spike3 = pygame.image.load('graphics/spikes_left.png').convert_alpha()
spike3 = pygame.transform.scale(spike3, (spike3.get_width(), spike3.get_height()))
spike4 = pygame.image.load('graphics/spikes_right.png').convert_alpha()
spike4 = pygame.transform.scale(spike4, (spike3.get_width(), spike3.get_height()))
maczuga = pygame.image.load('graphics/maczuga1.png').convert_alpha()
maczuga = pygame.transform.scale(maczuga, (maczuga.get_width(), maczuga.get_height()))
miecz = pygame.image.load('graphics/miecz1.png').convert_alpha()
miecz = pygame.transform.scale(miecz, (miecz.get_width(), miecz.get_height()))
kusza = pygame.image.load('graphics/crossbow.png').convert_alpha()
kusza = pygame.transform.scale(kusza, (kusza.get_width(), kusza.get_height()))
flying_right = pygame.image.load('graphics/flying_right.PNG').convert_alpha()
flying_right = pygame.transform.scale(flying_right, (flying_right.get_width(), flying_right.get_height()))
flying_left = pygame.image.load('graphics/flying_left.PNG').convert_alpha()
flying_left = pygame.transform.scale(flying_left, (flying_left.get_width(), flying_left.get_height()))
cannon_right = pygame.image.load('graphics/cannon_right.PNG').convert_alpha()
cannon_right = pygame.transform.scale(cannon_right, (cannon_right.get_width(), cannon_right.get_height()))
cannon_left = pygame.image.load('graphics/cannon_left.PNG').convert_alpha()
cannon_left = pygame.transform.scale(cannon_left, (cannon_left.get_width(), cannon_left.get_height()))
cannon_ball = pygame.image.load('graphics/cannon_ball.PNG').convert_alpha()
cannon_ball = pygame.transform.scale(cannon_ball, (14, 14))
grave3_image = pygame.image.load('graphics/grave3.PNG').convert_alpha()
grave3_image = pygame.transform.scale(grave3_image, (64, 32))
heart = pygame.image.load('graphics/lives_icon.PNG')
