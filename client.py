import pygame
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500), 0, 32)

color_white = (255, 255, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

   
        if pygame.key.get_pressed()[pygame.K_w]:
            print("Forward")
        elif pygame.key.get_pressed()[pygame.K_s]:
            print("Reverse")
        elif pygame.key.get_pressed()[pygame.K_a]:
            print("Left")
        elif pygame.key.get_pressed()[pygame.K_d]:
            print("Right")
    
    
    screen.fill(color_white)
    pygame.display.flip()