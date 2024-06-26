import pygame
pygame.init()

win = pygame.display.set_mode((1000,500))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 40
vel = 5

run = True

while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        x -= vel

    if keys[pygame.K_d]:
        x += vel

    if keys[pygame.K_w]:
        y -= vel

    if keys[pygame.K_s]:
        y += vel
    
    win.fill((0,0,0))
    pygame.draw.circle(win, (0,250,250), (x, y), width)  
    pygame.display.update() 
    
pygame.quit()