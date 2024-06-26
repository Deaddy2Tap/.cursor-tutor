import pygame

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1900, 950
PLAYER_MIN_X, PLAYER_MAX_X = -25, 1705
PLAYER_MIN_Y, PLAYER_MAX_Y =400, 800
PLAYER_START_X, PLAYER_START_Y = 100, 785
PLAYER_RADIUS = 110
flicker_state = True

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
shoot = pygame.image.load('vector_R_fire.png').convert_alpha()
shoot = pygame.transform.scale(shoot, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))
reload = [pygame.image.load('vector_r0.png'), pygame.image.load('vector_r1.png'), pygame.image.load('vector_r2.png'), pygame.image.load('vector_r3.png'), pygame.image.load('vector_r4.png')]
reload = pygame.transform.scale(shoot, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2))


display_bg = True

# Player Class
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
        self.reload = False
        self.dash_duration = 15
        self.dash_cooldown = 60
        self.dash_timer = 0
        self.is_dashing = False
    
    def move_horizontal(self, keys):
        if not self.is_dashing:
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
        if not self.is_dashing:
            dy = 0
            if keys[pygame.K_w] and keys[pygame.K_s]:
                dy = 0
            elif keys[pygame.K_s] and self.y < PLAYER_MAX_Y:
                dy = self.vel
            elif keys[pygame.K_w] and self.y > PLAYER_MIN_Y:
                dy = -self.vel
            self.y += dy

    def dash(self)
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
        self.move_vertical(keys)
        self.update_dash()

class proj(object):
    def _init_(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    
    def draw(screen):
        pygame.draw.circle(screen, proj.color, (proj.x, proj.y), proj.radius )

# Player Class Instance
sing = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_RADIUS)

#Redraw Window per Frame
def redraw():
    global flicker_state
    if display_bg:
        screen.blit(bg, (0, 0))

    if sing.shoot:
        if pygame.mouse.get_pressed()[0]:
            if flicker_state:
                screen.blit(shoot, (sing.x, sing.y))
            else:
                screen.blit(wrighta, (sing.x, sing.y))
                flicker_state = not flicker_state

    pygame.display.update()

def handle_events():
    global run, display_bg
    
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            sing.shoot = True
        if event.type == pygame.MOUSEBUTTONUP:
            sing.shoot = False
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.K_SPACE:
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