import random
import pygame
import sys
from button import ImageButton
from random import randint

clock = pygame.time.Clock()

# Display and icon
pygame.init()
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('shad0wgame')
icon = pygame.image.load('icons/icon.png').convert_alpha()
pygame.display.set_icon(icon)

high_scores = []

# Sounds
collision_sound = pygame.mixer.Sound('sounds/losing_hp.mp3')
shot_sound = pygame.mixer.Sound('sounds/shot_sound.mp3')
bullet_collision_sound = pygame.mixer.Sound('sounds/bullet_collision_sound.mp3')
airdrop_collision_sound = pygame.mixer.Sound('sounds/airdrop_collision_sound.mp3')
music_volume = 0.5

# Player
go_right = [
        pygame.image.load('icons/player_right/player_right_1.png').convert_alpha(),
        pygame.image.load('icons/player_right/player_right_2.png').convert_alpha(),
        pygame.image.load('icons/player_right/player_right_3.png').convert_alpha()
]
go_left = [
    pygame.image.load('icons/player_left/player_left_1.png').convert_alpha(),
    pygame.image.load('icons/player_left/player_left_2.png').convert_alpha(),
    pygame.image.load('icons/player_left/player_left_3.png').convert_alpha()
]

# Enemy
enemy_ghost = pygame.image.load('icons/ghost.png').convert_alpha()
enemy_mummy = pygame.image.load('icons/mummy.png').convert_alpha()
enemy_in_game = []
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 5000)

# Backgrounds
main_menu_background = pygame.image.load('icons/menu_background.png').convert_alpha()
level_menu_background = pygame.image.load('icons/level_menu_background.png').convert_alpha()
records_menu_background = pygame.image.load('icons/records_menu_background.png').convert_alpha()
settings_menu_background = pygame.image.load('icons/settings_menu_background.png').convert_alpha()
end_game_menu_background = pygame.image.load('icons/end_game_menu_background.png').convert_alpha()
background_forest = pygame.image.load('icons/Forest1.jpg').convert_alpha()
background_desert = pygame.image.load('icons/Desert1.jpg').convert_alpha()

# Buttons
play_button = ImageButton(WIDTH/2-(162/2), 80, 162, 42, '', 'icons/play_button.png',
                          'icons/play_button_hovered.png', 'sounds/button_sound.mp3')
records_button = ImageButton(WIDTH/2-(162/2), 140, 162, 42, '', 'icons/records_button.png',
                             'icons/records_button_hovered.png', 'sounds/button_sound.mp3')
exit_button = ImageButton(WIDTH/2-(162/2), 200, 162, 42, '', 'icons/exit_button.png',
                          'icons/exit_button_hovered.png', 'sounds/button_sound.mp3')
back_button = ImageButton(WIDTH/2-(162/2), 200, 162, 42, '', 'icons/back_button.png',
                          'icons/back_button_hovered.png', 'sounds/button_sound.mp3')
forest_button = ImageButton(20, 80, 162, 42, '', 'icons/forest_button.png',
                            'icons/forest_button_hovered.png', 'sounds/button_sound.mp3')
desert_button = ImageButton(400, 80, 162, 42, '', 'icons/desert_button.png',
                            'icons/desert_button_hovered.png', 'sounds/button_sound.mp3')
start_again_button = ImageButton(WIDTH/2-(162/2), 80, 162, 42, '', 'icons/start_again_button.png',
                                 'icons/start_again_button_hovered.png', 'sounds/button_sound.mp3')
main_menu_button = ImageButton(WIDTH/2-(162/2), 140, 162, 42, '', 'icons/main_menu_button.png',
                               'icons/main_menu_button_hovered.png', 'sounds/button_sound.mp3')
settings_button = ImageButton(550, 27, 30, 29, '', 'icons/settings_button.png',
                                'icons/settings_button_hovered.png', 'sounds/button_sound.mp3')
plus_button = ImageButton(335, 130, 42, 42, '', 'icons/plus_button.png',
                                'icons/plus_button_hovered.png', 'sounds/button_sound.mp3')
minus_button = ImageButton(225, 130, 42, 42, '', 'icons/minus_button.png',
                                'icons/minus_button_hovered.png', 'sounds/button_sound.mp3')


def main_menu():
    running = True
    while running:
        screen.blit(main_menu_background, (0, 0))

        for btn in [play_button, records_button, exit_button, settings_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == records_button:
                fade()
                records_menu()

            if event.type == pygame.USEREVENT and event.button == play_button:
                fade()
                level_menu()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                fade()
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                pygame.quit()
                sys.exit()

            for btn in [play_button, records_button, exit_button, settings_button]:
                btn.handle_event(event)


def records_menu():
    running = True
    load_high_scores()
    while running:
        screen.blit(records_menu_background, (0, 0))

        back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(screen)

        font = pygame.font.Font(None, 36)
        for i, score in enumerate(high_scores):
            text = font.render(f'{i + 1}. {score}', True, 'White')
            screen.blit(text, (230, 65 + i * 35))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
                fade()

            back_button.handle_event(event)


def settings_menu():
    global music_volume
    running = True
    while running:
        screen.blit(settings_menu_background, (0, 0))

        for btn in [back_button, plus_button, minus_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        font = pygame.font.Font(None, 36)
        text = font.render(f'Громкость: {music_volume}', True, 'White')
        screen.blit(text, (215, 85))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
                fade()

            if event.type == pygame.USEREVENT and event.button == plus_button and music_volume < 1:
                music_volume = round(music_volume + 0.1, 1)

            if event.type == pygame.USEREVENT and event.button == minus_button and music_volume > 0:
                music_volume = round(music_volume - 0.1, 1)

            for btn in [back_button, plus_button, minus_button]:
                btn.handle_event(event)


def level_menu():
    global current_background
    global current_enemy
    running = True
    while running:
        screen.blit(level_menu_background, (0, 0))

        for btn in [forest_button, desert_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == forest_button:
                current_background = background_forest
                current_enemy = enemy_ghost
                play_music('sounds/forest_music.mp3')
                new_game()

            if event.type == pygame.USEREVENT and event.button == desert_button:
                current_background = background_desert
                current_enemy = enemy_mummy
                play_music('sounds/desert_music.mp3')
                new_game()

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
                fade()

            for btn in [forest_button, desert_button, back_button]:
                btn.handle_event(event)


def new_game():

    # AirDrop
    hp_airdrop = pygame.image.load('icons/hp_airdrop.png').convert_alpha()
    bullet_airdrop = pygame.image.load('icons/bullet_airdrop.png').convert_alpha()
    airdrop_in_game = []
    airdrop_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(airdrop_timer, 5000)
    airdrop_types = [hp_airdrop, bullet_airdrop]
    current_airdrop = random.choice(airdrop_types)

    # Heart
    heart_image = pygame.image.load('icons/heart.png').convert_alpha()
    heart_spacing = 15

    # Bullet
    bullet_max = 5
    bullet = pygame.image.load('icons/bullet.png').convert_alpha()
    bullet_overlay = pygame.image.load('icons/bullet_overlay.png').convert_alpha()
    bullet_spacing = 10
    bullet_in_game = []

    # Lives and scores
    player_lives = 3
    score = 0

    player_animation_count = 0
    background_x = 0

    player_speed = 5
    player_x = 0
    player_y = 220

    is_jump = False
    jump_count = 9

    running = True
    gameplay = True

    while running:

        font = pygame.font.Font(None, 36)
        text_scores = font.render(f'Очки: {score}', True, 'White')

        screen.blit(current_background, (background_x, 0))
        screen.blit(current_background, (background_x + 600, 0))
        screen.blit(text_scores, (10, 10))

        if gameplay:

            for i in range(player_lives):
                screen.blit(heart_image, (400 + i * (heart_spacing + heart_image.get_width()), 10))

            for i in range(bullet_max):
                screen.blit(bullet_overlay, (400 + i * (bullet_spacing + bullet_overlay.get_width()), 265))

            player_rect = go_left[0].get_rect(topleft=(player_x, player_y))

            # Enemy
            if enemy_in_game:
                for (i, elem) in enumerate(enemy_in_game):
                    screen.blit(current_enemy, elem)
                    elem.x -= 5

                    if elem.x < -10:
                        enemy_in_game.pop(i)

                    if player_rect.colliderect(elem):
                        player_lives -= 1
                        collision_sound.play()
                        enemy_in_game.pop(i)

                        if player_lives <= 0:
                            gameplay = False

            # Airdrop
            if airdrop_in_game:
                for (i, elem) in enumerate(airdrop_in_game):
                    screen.blit(current_airdrop, elem)
                    elem.y += 6

                    if elem.y > 240:
                        airdrop_in_game.pop(i)

                    if player_rect.colliderect(elem):
                        airdrop_collision_sound.play()
                        if current_airdrop == hp_airdrop and player_lives < 3:
                            player_lives += 1
                        if current_airdrop == bullet_airdrop and bullet_max < 5:
                            bullet_max += 1
                        airdrop_in_game.pop(i)

            # Check if key get pressed
            keys = pygame.key.get_pressed()

            # Right or left
            if keys[pygame.K_a]:
                screen.blit(go_left[player_animation_count], (player_x, player_y))
            else:
                screen.blit(go_right[player_animation_count], (player_x, player_y))
                score += 1

            if keys[pygame.K_a] and player_x > 10:
                player_x -= player_speed
            elif keys[pygame.K_d] and player_x < 550:
                player_x += player_speed

            # Jump
            if not is_jump:
                if keys[pygame.K_SPACE]:
                    is_jump = True
            else:
                if jump_count >= -9:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2
                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 9

            if player_animation_count == 2:
                player_animation_count = 0
            else:
                player_animation_count += 1

            # Movement of background
            background_x -= 2
            if background_x == -600:
                background_x = 0

            # Bullet
            if bullet_in_game:
                for (i, el) in enumerate(bullet_in_game):
                    screen.blit(bullet, (el.x, el.y))
                    el.x += 3

                    if el.x > 600:
                        bullet_in_game.pop(i)

                    if enemy_in_game:
                        for (index, vrag) in enumerate(enemy_in_game):
                            if el.colliderect(vrag):
                                enemy_in_game.pop(index)
                                bullet_collision_sound.play()
                                bullet_in_game.pop(i)
                                score += 50

        else:
            update_high_scores(score)
            pygame.mixer.music.stop()
            end_game_menu()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == enemy_timer:
                enemy_in_game.append(enemy_ghost.get_rect(topleft=(600, randint(180, 220))))
            if event.type == airdrop_timer:
                current_airdrop = random.choice(airdrop_types)
                airdrop_in_game.append(current_airdrop.get_rect(topleft=(randint(50, 550), 0)))
            if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullet_max > 0:
                bullet_in_game.append(bullet.get_rect(topleft=(player_x, player_y)))
                shot_sound.play()
                bullet_max -= 1

        clock.tick(30)


def end_game_menu():
    running = True
    while running:
        screen.blit(end_game_menu_background, (0, 0))

        for btn in [start_again_button, main_menu_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_again_button:
                running = False
                new_game()

            if event.type == pygame.USEREVENT and event.button == main_menu_button:
                running = False
                fade()
                main_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                pygame.quit()
                sys.exit()

            for btn in [start_again_button, main_menu_button, exit_button]:
                btn.handle_event(event)


def fade():
    running = True
    fade_alpha = 0  # Уровень прозрачности

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.update()
        clock.tick(60)


def play_music(file_name):
    global music_volume
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_volume)


def load_high_scores():
    global high_scores
    try:
        with open('high_scores.txt', 'r') as file:
            high_scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        pass


def save_high_scores():
    with open('high_scores.txt', 'w') as file:
        for score in high_scores:
            file.write(str(score) + '\n')


def update_high_scores(score):
    global high_scores
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:4]
    save_high_scores()


if __name__ == '__main__':
    load_high_scores()
    main_menu()
