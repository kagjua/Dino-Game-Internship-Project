"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
import random

def game_score():
    #show game score
    score_surf = game_font.render(f"Score: {score}", False, "Black")
    score_rect = score_surf.get_rect(topleft=(25, 20))
    pygame.draw.rect(screen, "#87ceeb", score_rect)
    pygame.draw.rect(screen, "#87ceeb", score_rect, 10)
    screen.blit(score_surf, score_rect)

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
        if sprite_list:
            for sprite_rect in sprite_list:
                if sprite_rect.bottom == 300:
                    screen.blit(fence_surf, sprite_rect)
                    sprite_rect.x += int(speed)
                elif sprite_rect.bottom == 180:
                    screen.blit(carrot_surf, sprite_rect)
                    sprite_rect.x += int(speed)
            sprite_list = [obstacle for obstacle in sprite_list if obstacle.x > -50]
            return sprite_list
        else:
            return []
        
def collisions(player, sprites):
    global health, last_hit_time
    current_time = pygame.time.get_ticks()
    if current_time - last_hit_time < i_frames:
        return True
    if sprites:
        for sprite_rect in sprites:
            if player.colliderect(sprite_rect):
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


# Game state variables
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -17  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
difficulty = 1
speed = -(difficulty*6) # Change multiplier to change starting speed
health = 3 # Set health
i_frames = 1000
last_hit_time = -i_frames


# Load level assets
SKY_SURF = pygame.image.load("Dino-Game-Internship-Project/graphics/level/bg.png").convert()
GROUND_SURF = pygame.image.load("Dino-Game-Internship-Project/graphics/level/ground.png").convert()
#ground_x_pos = 
# END_SCR = pygame.image.load("graphics")
game_font = pygame.font.Font(pygame.font.get_default_font(), 35)
end_surf = game_font.render("GAME OVER", False, "Black")
end_rect = end_surf.get_rect(center=(400, 200))

enemy_timer = pygame.USEREVENT + 1
enemy_spawn_max = 2000
enemy_spawn = int(random.randint(1500, enemy_spawn_max))
enemy_spawn_interval_step = -25

                      

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
carrot_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/carrot.png").convert_alpha()
carrot_surf = pygame.transform.rotozoom(carrot_surf,270,1)
fence_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/fence.png").convert_alpha()
sprite_rect_list = []

#title screen assets
title_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/level/title.png").convert_alpha()


while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            
            if event.type == enemy_timer and is_playing:
                if random.randint(0,2):
                    sprite_rect_list.append(fence_surf.get_rect(bottomright = (random.randint(900,1000), 300)))
                else:
                    sprite_rect_list.append(carrot_surf.get_rect(bottomright = (random.randint(800,1000), 180)))
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
        score = int(pygame.time.get_ticks()/score_mult) - start 
        if score % 100 == 0:
            difficulty += 0.025
            speed = -(difficulty*6)
            enemy_spawn_interval = min(
                enemy_spawn_interval + enemy_spawn_interval_step,
                enemy_spawn_max,
            )
            pygame.time.set_timer(enemy_timer, enemy_spawn_interval)


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

    # When game is over, display game over message
    else:
        #reset gamestate
        screen.fill("red")
        screen.blit(end_surf,end_rect)
        sprite_rect_list.clear()
        player_rect.bottom = GROUND_Y
        difficulty = 1
        speed = -(difficulty*6)
        enemy_spawn_interval = 1500
        player_rect.x = 25
        health = 3
        last_hit_time = -i_frames

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
