import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Cascade')
pygame.display.set_allow_screensaver(False)
clock = pygame.time.Clock()
Background_text_font = pygame.font.Font(None, 220)
score_text_font = pygame.font.Font(None, 50)
game_over_font = pygame.font.Font(None, 80)

# Load assets
background_surface = pygame.image.load('assets/background.png').convert_alpha()
ground_surface = pygame.image.load('assets/Ground.png').convert_alpha()
character_surface = pygame.image.load('assets/Character.png').convert_alpha()
background_text = Background_text_font.render('FALLING', True, 'grey')

character_rect = character_surface.get_rect(midbottom=(600, 475))
character_gravity = 0

# Music
game_music = pygame.mixer.Sound('sounds/GameMusic.mp3')
game_music.set_volume(0.4)
if not pygame.mixer.get_busy():
    game_music.play(loops = -1)

# Collect sound
collect_sound = pygame.mixer.Sound('sounds/Collect.mp3')
collect_sound.set_volume(0.5)

# Falling object settings
red_shapes = ['circle', 'square', 'triangle']
green_shapes = ['circle', 'square', 'triangle']
sizes = {'small': 20, 'medium': 40, 'large': 60}  # Size in pixels
green_ratio = 1  # for every 3 red, 1 green
fall_objects = []  # active objects

# Timers
spawn_timer = 0
spawn_delay = 2000  # milliseconds
fall_speed = 2
time_elapsed = 0

# Game state
score = 0
game_active = True
start_time = time.time()

# Create falling object
def create_falling_object():
    color = 'red' if random.randint(1, 4) != 1 else 'green'  # 3:1 red to green
    shape = random.choice(red_shapes if color == 'red' else green_shapes)
    size_type = random.choice(list(sizes.keys()))
    size = sizes[size_type]
    x = random.randint(0, 1200 - size)

    points = 0
    if color == 'green':
        if size_type == 'small':
            points = 2
        elif size_type == 'medium':
            points = 7
        else:
            points = 25

    return {'rect': pygame.Rect(x, -size, size, size),
            'color': color,
            'shape': shape,
            'size_type': size_type,
            'points': points,
            'fade': False}  # for green fade

# Draw shapes
def draw_object(obj):
    if obj['shape'] == 'circle':
        pygame.draw.ellipse(screen, pygame.Color(obj['color']), obj['rect'])
    elif obj['shape'] == 'square':
        pygame.draw.rect(screen, pygame.Color(obj['color']), obj['rect'])
    elif obj['shape'] == 'triangle':
        x, y, size = obj['rect'].x, obj['rect'].y, obj['rect'].width
        points = [(x + size // 2, y), (x, y + size), (x + size, y + size)]
        pygame.draw.polygon(screen, pygame.Color(obj['color']), points)

# Check collision
def check_collision(character_rect, obj_rect):
    return character_rect.colliderect(obj_rect)

# Display score and time
def display_score_time():
    score_surf = score_text_font.render(f'Score: {score}', False, 'black')
    score_rect = score_surf.get_rect(topleft=(10, 10))
    screen.blit(score_surf, score_rect)

    elapsed_time = int(time.time() - start_time)
    time_surf = score_text_font.render(f'Time: {elapsed_time}s', False, 'black')
    time_rect = time_surf.get_rect(topright=(1190, 10))
    screen.blit(time_surf, time_rect)

# Game over screen
def game_over_screen():
    pygame.mixer.Sound.stop(game_music)  # stop music
    screen.blit(background_surface, (0, 0))
    screen.blit(ground_surface, (-10, 400))
    game_over_surf = game_over_font.render('GAME OVER', True, 'red')
    game_over_rect = game_over_surf.get_rect(center=(600, 200))
    screen.blit(game_over_surf, game_over_rect)

    final_score_surf = score_text_font.render(f'Score: {score}', False, 'black')
    final_score_rect = final_score_surf.get_rect(center=(600, 300))
    screen.blit(final_score_surf, final_score_rect)

    elapsed_time = int(time.time() - start_time)
    final_time_surf = score_text_font.render(f'Time: {elapsed_time}s', False, 'black')
    final_time_rect = final_time_surf.get_rect(center=(600, 350))
    screen.blit(final_time_surf, final_time_rect)

    restart_surf = score_text_font.render('Click anywhere to restart', False, 'green')
    restart_rect = restart_surf.get_rect(center=(600, 470))
    screen.blit(restart_surf, restart_rect)

# Main game loop
while True:
    dt = clock.tick(60)
    if game_active:
        time_elapsed += dt
        spawn_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active and event.type == pygame.MOUSEBUTTONDOWN:
            # Reset game
            score = 0
            fall_objects.clear()
            fall_speed = 2
            spawn_delay = 2000
            time_elapsed = 0
            start_time = time.time()
            character_rect.midbottom = (600, 475)
            character_gravity = 0
            game_active = True
            if not pygame.mixer.get_busy():
                game_music.play(loops = -1)  # resume music

    if game_active:
        # Increase difficulty gradually
        if time_elapsed % 4000 < dt:
            fall_speed += 0.4
            spawn_delay = max(200, spawn_delay - 100)

        # Spawn new objects
        if spawn_timer >= spawn_delay:
            fall_objects.append(create_falling_object())
            spawn_timer = 0

        # Draw background and ground
        screen.blit(background_surface, (0, 0))
        screen.blit(ground_surface, (-10, 400))
        screen.blit(background_text, (280, 200))
        display_score_time()

        # Player movement
        character_gravity += 1
        character_rect.y += character_gravity
        if character_rect.bottom >= 475: character_rect.bottom = 475
        screen.blit(character_surface, character_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character_rect.x -= 8
            if character_rect.right <= 0: character_rect.left = 1200

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character_rect.x += 8
            if character_rect.left >= 1200: character_rect.right = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and character_rect.bottom == 475:
            character_gravity = -17

        # Update falling objects
        for obj in fall_objects[:]:
            if obj['fade']:
                obj['rect'].y -= 10  # fade away
                if obj['rect'].bottom < 0:
                    fall_objects.remove(obj)
                continue

            obj['rect'].y += fall_speed
            draw_object(obj)

            if check_collision(character_rect, obj['rect']):
                if obj['color'] == 'green':
                    score += obj['points']
                    obj['fade'] = True
                    collect_sound.play()
                else:  # red collision ends game
                    game_active = False

            if obj['rect'].top > 600:
                fall_objects.remove(obj)

    else:
        game_over_screen()

    pygame.display.update()

