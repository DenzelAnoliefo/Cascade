import pygame 

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Cascade')
pygame.display.set_allow_screensaver(False)
FPS = pygame.time.Clock()
background_font = pygame.font.Font(None, 150)

background_surface = pygame.image.load('assets/background.png').convert_alpha()
ground_surface = pygame.image.load('assets/Ground.png').convert_alpha()
character_surface = pygame.image.load('assets/Character.png').convert_alpha()
background_text = background_font.render('FALLING', True, 'grey')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))
    screen.blit(ground_surface, (-10, 400))
    screen.blit(background_text, (415, 170))
    
    screen.blit(character_surface, (600, 350))

    pygame.display.update() 
    FPS.tick(60)