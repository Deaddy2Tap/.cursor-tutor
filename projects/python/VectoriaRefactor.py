import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 1900, 950
PLAYER_MIN_X, PLAYER_MAX_X = -25, 1450
PLAYER_MIN_Y, PLAYER_MAX_Y = -25, 800
PLAYER_START_X, PLAYER_START_Y = 100, 785

enemy_slots = [
    (1700, 65),
    (1700, 175),
    (1700, 285),
    (1700, 395),
    (1700, 505),
    (1700, 615),  
    (1700, 725),
    (1700, 835)
]

PLAYER_RADIUS = 110
FSENEMY_RADIUS = 46
AKENEMY_RADIUS = 115
BSENEMY_RADIUS = 120

menu_index = 0
game_run = False
menu_run = True

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("America at its Finest")

# Loading images
bg = pygame.image.load('bg1.png').convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

menubg = pygame.image.load('bg.jpeg').convert()
menubg = pygame.transform.scale(menubg, (SCREEN_WIDTH, SCREEN_HEIGHT))

bullet_vect = pygame.image.load('shoot.png').convert_alpha()
bullet_vect = pygame.transform.scale(bullet_vect, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))

shoot = pygame.image.load('shoot.png').convert_alpha()
shoot = pygame.transform.scale(shoot, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
idle = pygame.image.load('idle.png').convert_alpha()
idle = pygame.transform.scale(idle, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
spin = [pygame.image.load(f'f{i}.png').convert_alpha() for i in range(1, 6)]
spin = [pygame.transform.scale(image, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)) for image in spin]

menuloop = [pygame.image.load(f'menu{i}.png').convert_alpha() for i in range(1, 9)]
menuloop = [pygame.transform.scale(image, (PLAYER_RADIUS * 8, PLAYER_RADIUS * 8)) for image in menuloop]

menuclick = pygame.image.load('menuselected.png').convert_alpha()
menuclick = pygame.transform.scale(menuclick, (PLAYER_RADIUS * 8, PLAYER_RADIUS * 8))

five_shoot = pygame.image.load('57brrr.png').convert_alpha()
five_shoot = pygame.transform.scale(five_shoot, (FSENEMY_RADIUS * 2, FSENEMY_RADIUS * 2))
five_idle = pygame.image.load('57idle.png').convert_alpha()
five_idle = pygame.transform.scale(five_idle, (FSENEMY_RADIUS * 2, FSENEMY_RADIUS * 2))

ak_shoot = pygame.image.load('akbrrr.png').convert_alpha()
ak_shoot = pygame.transform.scale(ak_shoot, (AKENEMY_RADIUS * 2, AKENEMY_RADIUS * 2))
ak_idle = pygame.image.load('akidle.png').convert_alpha()
ak_idle = pygame.transform.scale(ak_idle, (AKENEMY_RADIUS * 2, AKENEMY_RADIUS * 2))

buckshot_shoot = pygame.image.load('buckshotbrrr.png').convert_alpha()
buckshot_shoot = pygame.transform.scale(buckshot_shoot, (BSENEMY_RADIUS * 2, BSENEMY_RADIUS * 2))
buckshot_idle = pygame.image.load('buckshotidle.png').convert_alpha()
buckshot_idle = pygame.transform.scale(buckshot_idle, (BSENEMY_RADIUS * 2, BSENEMY_RADIUS * 2))

# Projectiles
p_proj = pygame.image.load('bullet-9mm.png').convert_alpha()
p_proj = pygame.transform.scale(p_proj, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))

fs_proj = pygame.image.load('bullet-9mmr.png').convert_alpha()
fs_proj = pygame.transform.scale(fs_proj, (FSENEMY_RADIUS * 2, FSENEMY_RADIUS * 2))

ak_proj = pygame.image.load('bullet-7.62NATO.png').convert_alpha()
ak_proj = pygame.transform.scale(ak_proj, (AKENEMY_RADIUS * 2, AKENEMY_RADIUS * 2))

bs_proj = pygame.image.load('bullet-buckshot.png').convert_alpha()
bs_proj = pygame.transform.scale(bs_proj, (BSENEMY_RADIUS * 2, BSENEMY_RADIUS * 2))

# Classes for game elements
class PlayerProjectile(object):
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.damage = 25
        self.speed = 10

class FiveProjectile(object):
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.damage = 25
        self.speed = 10

class AKProjectile(object):
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.damage = 25
        self.speed = 10

class BuckshotProjectile(object):
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.damage = 25
        self.speed = 10

class Player(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 2
        self.wright = False
        self.wleft = False
        self.wup = False
        self.wdown = False
        self.shoot = False
        self.spin = False
        self.spin_index = 0
        self.spin_frame_delay = 12
        self.spin_frame_counter = 0
        self.spin_cooldown = 1500
        self.last_spin_time = -self.spin_cooldown
        self.spin_complete = False

    def move_horizontal(self, keys):
        dx = 0
        if keys[pygame.K_d] and keys[pygame.K_a]:
            dx = 0
        elif keys[pygame.K_d] and self.x < PLAYER_MAX_X:
            dx = self.vel
            self.wright = True
            self.wleft = False
        elif keys[pygame.K_a] and self.x > PLAYER_MIN_X:
            dx = -self.vel
            self.wleft = True
            self.wright = False
        self.x += dx

    def move_vertical(self, keys):
        dy = 0
        if keys[pygame.K_w] and keys[pygame.K_s]:
            dy = 0
        elif keys[pygame.K_s] and self.y < PLAYER_MAX_Y:
            dy = self.vel
        elif keys[pygame.K_w] and self.y > PLAYER_MIN_Y:
            dy = -self.vel
        self.y += dy
    
    def update(self, keys):
        self.move_horizontal(keys)
        self.move_vertical(keys)
        if self.spin:
            self.spin_frame_counter += 1
            if self.spin_frame_counter >= self.spin_frame_delay:
                self.spin_index = (self.spin_index + 1) % len(spin)
                self.spin_frame_counter = 0
                if self.spin_index == 0:
                    self.spin = False
                    self.spin_complete = True

class EnemyFiveSeven(object):
    def __init__(self, slot_index, radius):
        self.x, self.y = enemy_slots[slot_index]
        self.radius = radius
        self.health = 100
        self.max_health = 100
        self.attack_cooldown = 1000
        self.last_attack_time = 0
        self.time_to_move = 3000
        self.is_alive = True

class EnemyBuckshot(object):
    def __init__(self, slot_index, radius):
        self.x, self.y = enemy_slots[slot_index]
        self.radius = radius
        self.health = 100
        self.max_health = 100
        self.attack_cooldown = 1000
        self.last_attack_time = 0
        self.time_to_move = 3000
        self.is_alive = True

class EnemyAK(object):
    def __init__(self, slot_index, radius):
        self.x, self.y = enemy_slots[slot_index]
        self.radius = radius
        self.health = 100
        self.max_health = 100
        self.attack_cooldown = 1000
        self.last_attack_time = 0
        self.time_to_move = 3000
        self.is_alive = True

sing = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_RADIUS)

# Track occupied slots
occupied_slots = set()

# Initialize enemies in random unoccupied slots
while len(occupied_slots) < 3:  # Assuming you have 3 enemy types
    slot_index = random.randint(0, len(enemy_slots) - 1)
    if slot_index not in occupied_slots:
        if len(occupied_slots) == 0:
            five_seven_enemy = EnemyFiveSeven(slot_index, FSENEMY_RADIUS)
        elif len(occupied_slots) == 1:
            ak_enemy = EnemyAK(slot_index, AKENEMY_RADIUS)
        elif len(occupied_slots) == 2:
            buckshot_enemy = EnemyBuckshot(slot_index, BSENEMY_RADIUS)
        occupied_slots.add(slot_index)

def redraw():
    screen.blit(bg, (0, 0))

    if sing.spin:
        current_spin_image = spin[sing.spin_index]
        screen.blit(current_spin_image, (sing.x, sing.y))
    elif sing.shoot:
        bullet_position = (sing.x + sing.radius - bullet_vect.get_width() // 2, 
                           sing.y + sing.radius - bullet_vect.get_height() // 2)
        screen.blit(bullet_vect, bullet_position)
    else:
        screen.blit(idle, (sing.x, sing.y))

    if five_seven_enemy.is_alive:
        screen.blit(five_idle, (five_seven_enemy.x - 17, five_seven_enemy.y - 27))
        
    if ak_enemy.is_alive:
        screen.blit(ak_idle, (ak_enemy.x - 40, ak_enemy.y - 92))
    
    if buckshot_enemy.is_alive:
        screen.blit(buckshot_idle, (buckshot_enemy.x - 40, buckshot_enemy.y - 75))

    for slot_position in enemy_slots:
        pygame.draw.rect(screen, (0, 255, 0), (slot_position[0], slot_position[1], 9, 9)) 

    pygame.display.update()

def handle_events():
    global game_run
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_time - sing.last_spin_time > sing.spin_cooldown and not sing.spin:
                    sing.spin = True
                    sing.last_spin_time = current_time
                    sing.spin_complete = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            sing.shoot = True
            print(f"Projectile spawned at ({sing.x + sing.radius}, {sing.y + sing.radius})")
        if event.type == pygame.MOUSEBUTTONUP:
            sing.shoot = False
        if event.type == pygame.QUIT:
            game_run = False

def draw_menu_images():
    screen.blit(menubg, (0, 0))

    screen.blit(menuloop[menu_index], (490, 40))

    pygame.display.update()

def menu_handler():
    global menu_run, game_run, menu_index
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu_run = False
                game_run = True
            elif event.key == pygame.K_RIGHT:
                menu_index = (menu_index + 1) % len(menuloop)
            elif event.key == pygame.K_LEFT:
                menu_index = (menu_index - 1) % len(menuloop)
        if event.type == pygame.QUIT:
            menu_run = False
            game_run = False

while menu_run:
    clock.tick(144)
    keys = pygame.key.get_pressed()
    menu_handler()
    draw_menu_images()
    pygame.display.update()

while game_run:
    clock.tick(144)
    keys = pygame.key.get_pressed()
    handle_events()
    sing.update(keys)
    redraw()
    pygame.display.update()

pygame.quit()  