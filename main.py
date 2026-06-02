"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
#import random

def game_score():
    #show game score
    score_surf = game_font.render(f"Score: {score}", False, "Black")
    score_rect = score_surf.get_rect(topleft=(25, 20))
    pygame.draw.rect(screen, "#87ceeb", score_rect)
    pygame.draw.rect(screen, "#87ceeb", score_rect, 10)
    screen.blit(score_surf, score_rect)

def egg_anim():
    #egg walking animations
    global egg_surf, egg_index
    egg_index += difficulty/25
    if egg_index >= len(egg_walk):
        egg_index = 0
    egg_surf = egg_walk[int(egg_index)]

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


# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
score_mult = 50 #decrease/increase to increase/decrese score speed
start = int(pygame.time.get_ticks()/score_mult)
difficulty = 1


# Game state variables
is_playing = True  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
grav = -15
JUMP_GRAVITY_START_SPEED = -17  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
difficulty = 1

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/bg.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
#ground_x_pos = 
# END_SCR = pygame.image.load("graphics")
game_font = pygame.font.Font(pygame.font.get_default_font(), 35)
end_surf = game_font.render("GAME OVER", False, "Black")
end_rect = end_surf.get_rect(center=(400, 200))


# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk_3 = pygame.image.load("graphics/player/player_walk_3.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2, player_walk_3]
player_index = 0
player_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

carrot_surf = pygame.image.load("graphics/ingame/carrot.png").convert_alpha()
carrot_rect = player_surf.get_rect(bottomleft = (400, GROUND_Y))

egg_walk_1 = pygame.image.load("graphics/ingame/egg_1.png").convert_alpha()
egg_walk_2 = pygame.image.load("graphics/ingame/egg_2.png").convert_alpha()
egg_walk = [egg_walk_1, egg_walk_2]
egg_index = 0
egg_surf = egg_walk[egg_index]
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))

#title screen assets
title_surf = pygame.image.load("graphics/level/title.png").convert_alpha()


enemy_timer = pygame.USEREVENT + 1

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

        else:
            # When player wants to play again by pressing SPACE

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                egg_rect.left = 800
                start = int(pygame.time.get_ticks()/score_mult)

    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))


        #adjust enemy speed over time
        
        score = int(pygame.time.get_ticks()/score_mult) - start 
        if score % 150 == 0:
            difficulty += .1

        # Adjust egg's horizontal location then blit it
        egg_rect.x -= 5*difficulty
        if egg_rect.right <= 0:
            egg_rect.left = 800
        egg_anim()
        screen.blit(egg_surf, egg_rect)

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        player_anim()
        screen.blit(player_surf, player_rect)
        game_score()

        # carrot blitting
        screen.blit(carrot_surf, carrot_rect)

        # When player collides with enemy, game ends
        if egg_rect.colliderect(player_rect):
            is_playing = False
            difficulty = 1 

        #if carrot_rect.collidedict(player_rect):



    # When game is over, display game over message
    else:
        screen.fill("red")
        screen.blit(end_surf,end_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
