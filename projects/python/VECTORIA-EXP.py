import pygame

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1900, 950
PLAYER_MIN_X, PLAYER_MAX_X = -25, 1705
PLAYER_START_X, PLAYER_START_Y = 100, 785
PLAYER_RADIUS = 110

# Initialize Pygame
pygame.init()

# Clock Init
clock = pygame.time.Clock()

# Screen Render
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("America at its Finest")

# Load and scale background
bg = pygame.image.load('bg2.png').convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load player sprites with transparency handling
wrighta = pygame.image.load('vector_R_idle.png').convert_alpha()
wrighta = pygame.transform.scale(wrighta, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
wlefta = pygame.image.load('vector_L_idle.png').convert_alpha()
wlefta = pygame.transform.scale(wlefta, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
rshoot = pygame.image.load('vector_R_fire.png').convert_alpha()
rshoot = pygame.transform.scale(rshoot, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
lshoot = pygame.image.load('vector_L_fire.png').convert_alpha()
lshoot = pygame.transform.scale(lshoot, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
rreload = [pygame.image.load('vector_r0.png'), pygame.image.load('vector_r1.png'), pygame.image.load('vector_r2.png'), pygame.image.load('vector_r3.png'), pygame.image.load('vector_r4.png')]
rreload = pygame.transform.scale(lshoot, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
lreload = [pygame.image.load('vector_l0.png'), pygame.image.load('vector_l1.png'), pygame.image.load('vector_l2.png'), pygame.image.load('vector_l3.png'), pygame.image.load('vector_l4.png')]
lreload = pygame.transform.scale(lshoot, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))

display_bg = True

class proj(object):
    def _init_(self,x,y,radius,color,):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 15
    
    def draw(screen):
        pygame.draw.circle(screen, proj.color, (proj.x, proj.y), proj.radius )\
        
# Player Class
class Player(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 2
        self.wright = False
        self.wleft = False
        self.rshoot = False
        self.lshoot = False
        self.rreload = False
        self.lreload = False
        self.dash_duration = 15
        self.dash_cooldown = 60
        self.dash_timer = 0
        self.is_dashing = False
    
    def shoot_projectile(self):
        if self.wright:
            proj = proj(self.x + self.radius, self.y, 5, (255, 0, 0))  # Example color: red
        elif self.wleft:
            proj = proj(self.x - self.radius, self.y, 5, (0, 0, 255))  # Example color: blue
        return proj
    
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

    def dash(self):
        if not self.is_dashing and self.dash_timer == 0:
            self.vel *= 7
            self.is_dashing = True

    def update_dash(self):
        if self.is_dashing:
            self.dash_timer += 1
            if self.dash_timer >= self.dash_duration:
                self.vel /= 7
                self.is_dashing = False
                self.dash_timer = 0

    def update(self, keys):
        self.move_horizontal(keys)
        self.update_dash()

# Player Class Instance
sing = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_RADIUS)
def shoot_projectile(self):
        if self.wright:
            proj = proj(self.x + self.radius, self.y, 5, (255, 0, 0))
        elif self.wleft:
            proj = proj(self.x - self.radius, self.y, 5, (0, 0, 255))
        return proj

flicker_state = True

def redraw():
    global flicker_state
    if display_bg:
        screen.blit(bg, (0, 0))

    if sing.wright:
        if sing.rshoot:
            if pygame.mouse.get_pressed()[0]:
                if flicker_state:
                    screen.blit(rshoot, (sing.x, sing.y))
                else:
                    screen.blit(wrighta, (sing.x, sing.y))
                flicker_state = not flicker_state
            else:
                screen.blit(wrighta, (sing.x, sing.y))
        else:
            screen.blit(wrighta, (sing.x, sing.y))
    elif sing.wleft:
        if sing.lshoot:
            if pygame.mouse.get_pressed()[0]:
                if flicker_state:
                    screen.blit(lshoot, (sing.x, sing.y))
                else:
                    screen.blit(wlefta, (sing.x, sing.y))
                flicker_state = not flicker_state
            else:
                screen.blit(wlefta, (sing.x, sing.y))
        else:
            screen.blit(wlefta, (sing.x, sing.y))
    pygame.display.update()

def handle_events():
    global run, display_bg
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if sing.wright:
                sing.rshoot = True
                sing.lshoot = False
                sing.shoot_projectile()
            elif sing.wleft:
                sing.rshoot = False
                sing.lshoot = True
                sing.shoot_projectile()
        if event.type == pygame.MOUSEBUTTONUP:
            sing.rshoot = False
            sing.lshoot = False
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                display_bg = not display_bg
            elif event.key == pygame.K_SPACE:
                sing.dash()
            
# Main Game Loop
run = True
while run:
    clock.tick(144)
    keys = pygame.key.get_pressed()
    handle_events()
    sing.update(keys)
    redraw()

# Quit Pygame
pygame.quit()