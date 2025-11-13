import pygame 

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Cascade')
pygame.display.set_allow_screensaver(False)
clock = pygame.time.Clock()
Background_text_font = pygame.font.Font(None, 220)
score_text_font = pygame.font.Font(None, 50)

background_surface = pygame.image.load('assets/background.png').convert_alpha()
ground_surface = pygame.image.load('assets/Ground.png').convert_alpha()
character_surface = pygame.image.load('assets/Character.png').convert_alpha()
background_text = Background_text_font.render('FALLING', True, 'grey')

character_rect =character_surface.get_rect(midbottom = (600, 475))  
score_surf = score_text_font.render('My game', False, 'Black')
score_rect = score_surf.get_rect(center = (600, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        '''if event.type == pygame.MOUSEMOTION:
            if character_rect.collidepoint(event.pos): print("collision")'''

    screen.blit(background_surface, (0, 0))
    screen.blit(ground_surface, (-10, 400))
    screen.blit(background_text, (280, 200))
    screen.blit(score_surf, score_rect)
    
    screen.blit(character_surface, character_rect)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        character_rect.x -= 8
        if character_rect.right <= 0: character_rect.left = 1200

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        character_rect.x += 8
        if character_rect.left >= 1200: character_rect.right = 0

    if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
        pass

    '''mouse_pos = pygame.mouse.get_pos()
    if character_rect.collidepoint(mouse_pos):
        print(pygame.mouse.get_pressed())'''


    pygame.display.update() 
    clock.tick(60)
    