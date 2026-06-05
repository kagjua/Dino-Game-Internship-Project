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
                sprite_rect.x -= 5*difficulty
                if sprite_rect.bottom == 300:
                    screen.blit(fence_surf, sprite_rect)
                elif sprite_rect.bottom == 210:
                    screen.blit(carrot_surf, sprite_rect)
            sprite_list = [obstacle for obstacle in sprite_list if obstacle.x > -50]
            return sprite_list
        else:
            return []
        
def collisions(player, sprites):
    if sprites:
        for sprite_rect in sprites:
            if player.colliderect(sprite_rect):
                return False
    return True

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
score_mult = 50 #decrease/increase to increase/decrese score speed
start = int(pygame.time.get_ticks()/score_mult)
difficulty = 1


# Game state variables
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
grav = -15
JUMP_GRAVITY_START_SPEED = -17  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
difficulty = 1

# Load level assets
SKY_SURF = pygame.image.load("Dino-Game-Internship-Project/graphics/level/bg.png").convert()
GROUND_SURF = pygame.image.load("Dino-Game-Internship-Project\graphics\level\ground.png").convert()
#ground_x_pos = 
# END_SCR = pygame.image.load("graphics")
game_font = pygame.font.Font(pygame.font.get_default_font(), 35)
end_surf = game_font.render("GAME OVER", False, "Black")
end_rect = end_surf.get_rect(center=(400, 200))


# Load sprite assets
player_walk_1 = pygame.image.load("Dino-Game-Internship-Project/graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("Dino-Game-Internship-Project/graphics/player/player_walk_2.png").convert_alpha()
player_walk_3 = pygame.image.load("Dino-Game-Internship-Project/graphics/player/player_walk_3.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2, player_walk_3]
player_index = 0
player_jump = pygame.image.load("Dino-Game-Internship-Project/graphics/player/player_jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

#non player sprites
carrot_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/carrot.png").convert_alpha()
carrot_surf = pygame.transform.rotozoom(carrot_surf,270,1)

fence_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/ingame/fence.png").convert_alpha()


sprite_rect_list = []



#title screen assets
title_surf = pygame.image.load("Dino-Game-Internship-Project/graphics/level/title.png").convert_alpha()


enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
            
            if event.type == enemy_timer and is_playing:
                if random.randint(0,2):
                    sprite_rect_list.append(fence_surf.get_rect(bottomright = (random.randint(800,1000), 300)))
                else:
                    sprite_rect_list.append(carrot_surf.get_rect(bottomright = (random.randint(800,1000), 210)))
        else:
            # When player wants to play again by pressing SPACE

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                start = int(pygame.time.get_ticks()/score_mult)

    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))

        #collisions
        is_playing = collisions(player_rect, sprite_rect_list)
        #adjust enemy speed over time
        
        score = int(pygame.time.get_ticks()/score_mult) - start 
        if score % 150 == 0:
            difficulty += .1

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
        screen.fill("red")
        screen.blit(end_surf,end_rect)
        sprite_rect_list.clear()
        player_rect.bottom = GROUND_Y
        difficulty = 1

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
