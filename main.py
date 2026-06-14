"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
import random

global score
def game_score():
    #show game score
    score_surf = game_font.render(f"Score: {score}", False, "Black")
    score_rect = score_surf.get_rect(topleft=(25, 20))
    screen.blit(score_surf, score_rect)

def draw_health_bar():
    #show player health as a shrinking bar
    bar_width = 200
    bar_height = 30
    bar_x = 575
    bar_y = 20
    health_ratio = max(health, 0) / max_health
    current_width = int(bar_width * health_ratio)
    background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
    current_rect = pygame.Rect(bar_x, bar_y, current_width, bar_height)
    pygame.draw.rect(screen, "darkred", background_rect)
    pygame.draw.rect(screen, "limegreen", current_rect)
    pygame.draw.rect(screen, "black", background_rect, 2)

def player_anim():
    #all player animations
    global player_surf, player_index
    if player_rect.bottom < GROUND_Y:
        player_surf = player_jump
    else:
        player_index += 0.25
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

def sprite_movement(sprite_list):
    #spawns correct sprite based on y-level
        if sprite_list:
            for sprite_rect in sprite_list:
                if sprite_rect.bottom == 300:
                    screen.blit(fence_surf, sprite_rect)
                    sprite_rect.x += int(speed)
                elif sprite_rect.bottom == 180:
                    screen.blit(robo_surf, sprite_rect)
                    sprite_rect.x += int(speed)
                elif sprite_rect.bottom == 301:
                    screen.blit(gold_surf, sprite_rect)
                    sprite_rect.x += int(speed)
                else:
                    screen.blit(carrot_surf, sprite_rect)
                    sprite_rect.x += int(speed)
            sprite_list = [obstacle for obstacle in sprite_list if obstacle.x > -50]
            return sprite_list
        else:
            return []
        
def collisions(player, sprites):
    global health, last_hit_time, gold_score
    current_time = pygame.time.get_ticks()
    if current_time - last_hit_time < i_frames:
        return True
    if sprites:
        for sprite_rect in sprites:
            if player.colliderect(sprite_rect):
                sprite_rect.left = -1000
                if sprite_rect.bottom == 190:
                    health += 1
                    last_hit_time = current_time
                elif sprite_rect.bottom == 301:
                    gold_score += 50
                    last_hit_time = current_time
                else:
                    health -= 1
                    last_hit_time = current_time
                    if health <= 0:
                        return False
                    return True
    return True

# Initialize Pygame and create a window
pygame.init()
frame_width = 800
frame_height = 400
screen = pygame.display.set_mode((frame_width, frame_height))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
score_mult = 50 #decrease/increase to increase/decrese score speed
start = int(pygame.time.get_ticks()/score_mult)
high_score = 0
score = 0
gold_score = 0
last_difficulty_milestone = 0  # Track the last 100-point threshold processed


# Game state variables
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -17  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
difficulty = 1
speed = -(difficulty*6) # Change multiplier to change starting speed
health = 3 # Set health
max_health = health
i_frames = 500 # how long i-frames last
last_hit_time = -i_frames # checks for when last hit


# Load level assets
SKY_SURF = pygame.image.load("Dino-Game-Internship-Project/graphics/level/bg.png").convert()
GROUND_SURF = pygame.image.load("Dino-Game-Internship-Project/graphics/level/ground.png").convert()
#ground_x_pos = 
# END_SCR = pygame.image.load("graphics")
game_font = pygame.font.Font(pygame.font.get_default_font(), 35)

#sprite spawn timers
enemy_timer = pygame.USEREVENT + 1
enemy_spawn_max = 2000
enemy_spawn = int(random.randint(1500, enemy_spawn_max))
enemy_spawn_rate_step = -25
enemy_spawn_rate = enemy_spawn
pygame.time.set_timer(enemy_timer, enemy_spawn_rate)
carrot_timer = pygame.USEREVENT + 2
carrot_spawn_min = 4000
carrot_spawn_max = 8000
carrot_spawn_rate = random.randint(carrot_spawn_min, carrot_spawn_max)
pygame.time.set_timer(carrot_timer, carrot_spawn_rate)

# Load sprite assets
player_walk_1 = pygame.image.load("Dino-Game-Internship-Project/graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("Dino-Game-Internship-Project/graphics/player/player_walk_2.png").convert_alpha()
player_walk_3 = pygame.image.load("Dino-Game-Internship-Project/graphics/player/player_walk_3.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2, player_walk_3]
player_index = 0
player_jump = pygame.image.load("Dino-Game-Internship-Project/graphics/player/player_jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

#enemy sprites
robo_carrot_1 = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/robo_carrot_1.png").convert_alpha()
robo_carrot_2 = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/robo_carrot_2.png").convert_alpha()
robo_carrot_3 = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/robo_carrot_3.png").convert_alpha()
robo_fly = [robo_carrot_1, robo_carrot_2, robo_carrot_3]
robo_index = 0
robo_surf = robo_fly[robo_index]
carrot_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/carrot.png").convert_alpha()
fence_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/fence.png").convert_alpha()
gold_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/bar.png").convert_alpha()
sprite_rect_list = []


#title screen assets
title_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/level/title.png").convert_alpha()
title_rect = title_surf.get_rect(center=(400,200))

#set robot carrot event
robo_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(robo_animation_timer, 500)

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            #pick between enemies
            if event.type == enemy_timer:
                spawner = random.randint(1,9)
                if spawner <= 4:
                    sprite_rect_list.append(fence_surf.get_rect(bottomright = (random.randint(900,1000), 300)))
                elif spawner <= 8:
                    sprite_rect_list.append(robo_surf.get_rect(bottomright = (random.randint(800,1000), 180)))
                else:
                    sprite_rect_list.append(gold_surf.get_rect(bottomright = (random.randint(800,1000), 301)))

            if event.type == carrot_timer and health < max_health and random.randint(1,5) == 1:
                sprite_rect_list.append(carrot_surf.get_rect(bottomright = (random.randint(800,1000), 190)))
                    
            #robot carrot animation time
            if event.type == robo_animation_timer:
                if robo_index < 2:
                    robo_index += 1
                else:
                    robo_index = 0
                robo_surf = robo_fly[robo_index]
                robo_surf = pygame.transform.rotate(robo_surf, 270)
                
        else:
            # When player wants to play again by pressing SPACE or M1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                is_playing = True
                start = int(pygame.time.get_ticks()/score_mult)

    if is_playing:
        # Blit the level assets
        SKY_SURF.scroll(-1, 0 , pygame.SCROLL_REPEAT)
        GROUND_SURF.scroll(int(speed),0,pygame.SCROLL_REPEAT)
        screen.blit(SKY_SURF)
        screen.blit(GROUND_SURF, (0, GROUND_Y))

        #collisions
        is_playing = collisions(player_rect, sprite_rect_list)
        
        #player movement
        keys = pygame.key.get_pressed()
        if  (keys[pygame.K_SPACE]
            or keys[pygame.K_w] 
            or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
            players_gravity_speed = JUMP_GRAVITY_START_SPEED
        if keys[pygame.K_d] and player_rect.right < frame_width:
            player_rect.x += 5
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= 5
        if keys[pygame.K_s]:
            if player_rect.bottom > GROUND_Y:
                JUMP_GRAVITY_START_SPEED = -10
        
        #adjust enemy speed over time
        time_score = int(pygame.time.get_ticks()/score_mult) - start 
        score = time_score + gold_score
        # Check if score has crossed a new 100-point milestone (catches jumps too)
        current_milestone = (score // 100) * 100
        if current_milestone > last_difficulty_milestone and score <= 1500:
            difficulty += 0.025
            speed = -(difficulty*6)
            enemy_spawn_rate = min(
                enemy_spawn_rate + enemy_spawn_rate_step,
                enemy_spawn_max,
            )
            pygame.time.set_timer(enemy_timer, enemy_spawn_rate)
            last_difficulty_milestone = current_milestone


        # Adjust sprite horizontal location then blit it
        sprite_rect_list = sprite_movement(sprite_rect_list)

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        player_anim()
        screen.blit(player_surf, player_rect)
        game_score()
        draw_health_bar()

    else:
        #blit title screen
        high_score = max(high_score, score)
        screen.fill("black")
        screen.blit(title_surf, title_rect)
        high_score_surf = game_font.render(f"High Score: {high_score}  Latest Score: {score}", False, "White")
        high_score_rect = high_score_surf.get_rect(center=(400, 50))
        screen.blit(high_score_surf, high_score_rect)
        play_again_surf = game_font.render("Use WASD and Space to play", False, "White")
        play_again_rect = play_again_surf.get_rect(center=(400, 350))
        screen.blit(play_again_surf, play_again_rect)
    
        #reset game state
        sprite_rect_list.clear()
        player_rect.bottom = GROUND_Y
        difficulty = 1
        speed = -(difficulty*6)
        enemy_spawn_rate = 1500
        pygame.time.set_timer(enemy_timer, enemy_spawn_rate)
        pygame.time.set_timer(carrot_timer, carrot_spawn_rate)
        player_rect.x = 25
        health = 3
        last_hit_time = -i_frames
        gold_score = 0
        last_difficulty_milestone = 0

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()