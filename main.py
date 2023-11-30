import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Obstacle Avoidance Game")

# Set up colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
shadow_color = (0, 0, 0, 100)  # Adding an alpha component for transparency

# Player attributes
player_radius = 25
player_x = width // 2
player_y = height - 2 * player_radius
player_speed = 5

# Obstacle attributes
obstacle_speed = 5
obstacle_frequency = 25
obstacles = []

# Different types of obstacles
obstacle_types = ['circle', 'rectangle', 'triangle']
obstacle_colors = {
    'circle': red,
    'rectangle': (0, 255, 0),
    'triangle': (0, 0, 255)
}

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for displaying score
font = pygame.font.Font(None, 36)

score = 0

def draw_player(x, y):
    pygame.draw.circle(screen, blue, (x, y), player_radius)

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle['color'], obstacle['rect'])

def draw_shadows(obstacles):
    for obstacle in obstacles:
        shadow_rect = obstacle['rect'].copy()
        shadow_rect.y = height - player_radius
        pygame.draw.rect(screen, shadow_color, shadow_rect)

def display_score(score):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, [10, 10])

def show_game_over(score):
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    prompt_text = font.render("Press 'r' to restart or 'q' to quit.", True, (0, 0, 255))
    screen.blit(game_over_text, [width // 2 - 70, height // 2 - 50])
    screen.blit(score_text, [width // 2 - 40, height // 2])
    screen.blit(prompt_text, [width // 2 - 140, height // 2 + 50])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_radius > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_radius < width:
        player_x += player_speed

    # Create obstacles
    if random.randrange(obstacle_frequency) == 0:
        obstacle_type = random.choice(obstacle_types)
        obstacle_x = random.randrange(width - player_radius)
        obstacle_y = -player_radius
        obstacle_size = player_radius * 2
        obstacles.append({'rect': pygame.Rect(obstacle_x, obstacle_y, obstacle_size, obstacle_size),
                          'type': obstacle_type,
                          'color': obstacle_colors[obstacle_type]})

    # Move obstacles
    for obstacle in obstacles:
        obstacle['rect'].y += obstacle_speed

    # Check for collisions
    for obstacle in obstacles:
        if (
            math.sqrt((player_x - obstacle['rect'].centerx)**2 + (player_y - obstacle['rect'].centery)**2) <
            player_radius + max(obstacle['rect'].width, obstacle['rect'].height) / 2
        ):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            score = 0
                            obstacles = []
                            player_x = width // 2
                            player_y = height - 2 * player_radius
                            break
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

                screen.fill(black)
                show_game_over(score)
                pygame.display.flip()

    # Remove off-screen obstacles
    obstacles = [obstacle for obstacle in obstacles if obstacle['rect'].centery < height]

    # Increase score for each obstacle passed
    score += len(obstacles)

    # Clear the screen with a dark background
    screen.fill(black)

    # Draw shadows
    draw_shadows(obstacles)

    # Draw player and obstacles
    draw_player(player_x, player_y)
    draw_obstacles(obstacles)

    # Display score
    display_score(score)

    # Display the updated screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
