#Setup
import pygame
import sys
import random
from levels import levels

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏃‍♂️ Code Adventure")

WHITE, BLACK = (255, 255, 255), (0, 0, 0)
SKY_BLUE, GREEN = (135, 206, 250), (34, 139, 34)
BROWN, YELLOW, RED = (139, 69, 19), (255, 255, 0), (255, 0, 0)
GOLD = (255, 215, 0)
medium_font = pygame.font.SysFont("comicsans", 30)
font=pygame.font.SysFont("none",28)
question_font = pygame.font.SysFont(None, 36)

correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
win_sound = pygame.mixer.Sound("sounds/win.mp3")

coin_image = pygame.image.load("pictures/coin.png").convert_alpha()
coin_image = pygame.transform.scale(coin_image, (20, 20))

enemy_img = pygame.image.load("pictures/enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (60, 60))

# Original size for character in the game
original_size = (70, 84)
# Larger size for the start screen
larger_size = (100, 120)

player_img = pygame.image.load("pictures/character.png")
player_img_start = pygame.transform.scale(player_img, larger_size)
player_img_game = pygame.transform.scale(player_img, original_size)
# character size for quiz screen
big_character_img = pygame.image.load("pictures/character_big.png")
big_character_img = pygame.transform.scale(big_character_img, (450, 500))
player_velocity_y = 0
jump_power = 16
gravity = 0.8
ground_y = HEIGHT - 60

#final flag animation
flag_imgs = [pygame.image.load("pictures/flag1.png"), pygame.image.load("pictures/flag2.png")]
for i in range(len(flag_imgs)):
    flag_imgs[i] = pygame.transform.scale(flag_imgs[i], (40, 40))

# clouds
clouds = [{"x": random.randint(0, WIDTH), "y": random.randint(20, 150), "speed": random.uniform(0.3, 1)} for _ in range(5)]
cloud_img = pygame.image.load("pictures/cloud.png")
cloud_img = pygame.transform.scale(cloud_img, (120, 80))

current_level = 0

def load_level():
    global platforms, question_boxes, asked_questions, player_x, player_y, finish_line
    global enemies, moving_platforms
    level = levels[current_level]
    platforms = level["platforms"]
    enemies = level.get("enemies", [])
    moving_platforms = level.get("moving_platforms", [])
    question_boxes = [pygame.Rect(p.x + p.width//2 - 20, p.y - 40, 40, 40) for p in platforms]
    asked_questions[:] = [False] * len(platforms)
    player_x, player_y = 100, ground_y - original_size[1]
    finish_line = pygame.Rect(WIDTH - 100, ground_y - 100, 20, 100)

#GAME STATE
player_x, player_y = 100, ground_y - original_size[1]
is_jumping = False
asked_questions = []
enemies = []
moving_platforms = []
boss_question_triggered = False
boss_question_answered = False
load_level()

show_question = False
attempts = 2  # Max 2 attempts per question
current_question = None
reached_finish = False
confetti = []
message = ""
message_color = WHITE
message_timer = 0
flag_frame = 0


def show_message(text, color, duration=90):
    global message, message_color, message_timer
    message, message_color, message_timer = text, color, duration

def draw_question_box(rect):
    pygame.draw.rect(screen, YELLOW, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

def display_question(q):
    screen.fill(SKY_BLUE)
    screen.blit(big_character_img, (375, 100))
    question_text = question_font.render(q["question"], True, BLACK)
    screen.blit(question_text, (50, 150))
    for i, opt in enumerate(q["options"]):
        opt_text = question_font.render(f"{i + 1}. {opt}", True, BLACK)
        screen.blit(opt_text, (70, 200 + i * 30))

def draw_button(text, x, y):
    rect = pygame.Rect(x, y, 180, 40)
    pygame.draw.rect(screen, GREEN, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    txt = font.render(text, True, BLACK)
    screen.blit(txt, (x + 20, y + 10))
    return rect

# Function to draw coins
def draw_coins(coins):
    for coin in coins:
        screen.blit(coin_image, coin.topleft)

# Function to collect coins
def collect_coins(player_rect, coins, collected_coins):
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            coins.remove(coin)  # Remove the coin when collected
            collected_coins += 1  # Increase the score
    return collected_coins

def start_screen():
    char_x = WIDTH // 2 - 50  # Centering the character
    char_y = ground_y - larger_size[1]  # Adjusting position based on larger size
    char_direction = 1
    char_speed = 2

    while True:
        screen.fill(SKY_BLUE)

        for cloud in clouds:
            screen.blit(cloud_img, (cloud["x"], cloud["y"]))
            cloud["x"] += cloud["speed"]
            if cloud["x"] > WIDTH:
                cloud["x"] = -100
                cloud["y"] = random.randint(20, 150)

        # Ground
        pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, 60))
        
        #font styles
        heading_font = pygame.font.Font(r'font/Super Pixel Personal Use.ttf', 48)  
        tagline_font = pygame.font.SysFont('Arial', 36)  
        button_font = pygame.font.SysFont('Arial', 30) 

        # Game Title
        title = heading_font.render("Python Patrol", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title, title_rect)

        # Tagline
        tagline = tagline_font.render("Jump into code. Level up your skills.", True, BLACK)
        tagline_rect = tagline.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 50))
        screen.blit(tagline, tagline_rect)

        # Animate character
        char_x += char_speed * char_direction
        if char_x <= 100 or char_x >= WIDTH - 100 - larger_size[0]:
            char_direction *= -1
        screen.blit(player_img_start, (char_x, char_y))

        # Start Button
        start_button_width = 200
        start_button_height = 60
        start_button = pygame.Rect(WIDTH // 2 - start_button_width // 2, HEIGHT // 3 + 100, start_button_width, start_button_height)

        # Draw the start button with white box and black text in the center
        pygame.draw.rect(screen, WHITE, start_button)  # White background for the button
        start_text = button_font.render("Start", True, BLACK)  # Black text for the button
        start_text_rect = start_text.get_rect(center=start_button.center)  # Center the text inside the button
        screen.blit(start_text, start_text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return

        pygame.display.update()
        clock.tick(60)

def win_screen():
    char_x = WIDTH // 2 - 50  # Centering the character
    char_y = ground_y - larger_size[1]  # Adjusting position based on larger size
    char_direction = 1
    char_speed = 2
    screen.fill(SKY_BLUE)

    for cloud in clouds:
            screen.blit(cloud_img, (cloud["x"], cloud["y"]))
            cloud["x"] += cloud["speed"]
            if cloud["x"] > WIDTH:
                cloud["x"] = -100
                cloud["y"] = random.randint(20, 150)

    # Ground
    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, 60))

    title = font.render("🎉 You Won the Game! 🎉", True, GREEN)
    button_text = font.render("Play Again", True, WHITE)

    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    
    # Animate character
    char_x += char_speed * char_direction
    if char_x <= 100 or char_x >= WIDTH - 100 - larger_size[0]:
        char_direction *= -1
    screen.blit(player_img_start, (char_x, char_y))

    pygame.draw.rect(screen, RED, button_rect)
    screen.blit(title, title_rect)
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False  # exit win screen
                    

# MAIN LOOP
start_screen()
running = True
collected_coins = 0 
while running:
    screen.fill(SKY_BLUE)

    player_rect = pygame.Rect(player_x, player_y, original_size[0], original_size[1])

    # Draw coins (only if level >= 2)
    if current_level >= 1:  # Level 2 and onward
        collected_coins = collect_coins(player_rect, levels[current_level]["coins"], collected_coins)
        draw_coins(levels[current_level]["coins"])

    # Draw enemies (Level 3+)
    if current_level >= 2:
        for enemy in enemies:
            screen.blit(enemy_img, enemy.topleft)  # Use the enemy image
            buffer = 10
            adjusted_enemy = enemy.inflate(-buffer, -buffer)
            if player_rect.colliderect(adjusted_enemy):
                show_message("Hit by enemy! Restarting...", RED, duration=120)
                wrong_sound.play()
                pygame.time.set_timer(pygame.USEREVENT + 1, 1500)

    # Move clouds
    for cloud in clouds:
        screen.blit(cloud_img, (cloud["x"], cloud["y"]))
        cloud["x"] += cloud["speed"]
        if cloud["x"] > WIDTH:
            cloud["x"] = -100
            cloud["y"] = random.randint(20, 150)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT + 1:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer
            load_level()
            reached_finish = False
            show_question = False
            attempts = 2

        if show_question and event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_4:
                selected = event.key - pygame.K_1
                if selected == current_question['answer']:
                    player_x += 20
                    show_message("Correct!", GREEN)
                    correct_sound.play()
                    asked_questions[current_index] = True
                    show_question = False
                    attempts = 2  # reset for next question
                else:
                    attempts -= 1
                    if attempts <= 0:
                        show_message("You lost! Restarting...", RED, duration=120)
                        wrong_sound.play()
                        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # delay restart
                    else:
                        show_message(f"Wrong! {attempts} attempts left.", RED)
                        wrong_sound.play()

        if reached_finish and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if next_btn.collidepoint((mx, my)):
                if current_level < len(levels) - 1:
                    current_level += 1
                    reached_finish = False
                    load_level()
                else:
                    win_screen()
                    current_level = 0
                    collected_coins = 0
                    reached_finish = False
                    load_level()
                    start_screen()
            elif replay_btn.collidepoint((mx, my)):
                reached_finish = False
                load_level()

    if not show_question and not reached_finish:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_x -= 5
        if keys[pygame.K_RIGHT]: player_x += 5
        if keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = -jump_power
            is_jumping = True

        player_velocity_y += gravity
        player_y += player_velocity_y
        player_rect = pygame.Rect(player_x, player_y, *original_size)

        if player_y >= ground_y - original_size[1]:
            player_y = ground_y - original_size[1]
            player_velocity_y = 0
            is_jumping = False

        for platform in platforms:
            if player_rect.colliderect(platform) and player_velocity_y > 0:
                if player_rect.bottom - platform.top < 20:
                    player_y = platform.top - original_size[1]
                    player_velocity_y = 0
                    is_jumping = False

        pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, 60))
        for p in platforms:
            pygame.draw.rect(screen, BROWN, p)

        # Move and draw moving platforms (Level 4+)
        if current_level >= 3:
            moving_platforms = levels[current_level].get("moving_platforms", [])
            for mp in moving_platforms:
                rect = mp['rect']

                # Move the platform
                if mp['direction'] == "horizontal":
                    rect.x += mp['speed']
                    if rect.x < mp['min'] or rect.x > mp['max']:
                        mp['speed'] *= -1
                elif mp['direction'] == "vertical":
                    rect.y += mp['speed']
                    if rect.y < mp['min'] or rect.y > mp['max']:
                        mp['speed'] *= -1

                # Draw the moving platform
                pygame.draw.rect(screen, BROWN, rect)

                # Add to collision platforms list
                platforms.append(rect)

                # Check if player is on top of the moving platform
                if player_rect.colliderect(rect) and player_velocity_y >= 0:  # Player is on top of the platform
                    if player_rect.bottom <= rect.top + 5:  # Small threshold to prevent 'sticking' to the platform
                        player_y = rect.top - original_size[1]  # Set the player on top of the platform
                        # Move the player with the platform
                        if mp['direction'] == "horizontal":
                            player_x += mp['speed']
                        elif mp['direction'] == "vertical":
                            player_y += mp['speed']

                        player_velocity_y = 0
                        is_jumping = False

        for i, qb in enumerate(question_boxes):
            if not asked_questions[i]:
                draw_question_box(qb)
                if player_rect.colliderect(qb):
                    show_question = True
                    current_index = i
                    current_question = levels[current_level]["questions"][i]

        pygame.draw.rect(screen, BLACK, finish_line)
        flag_img = flag_imgs[flag_frame // 30 % 2]
        screen.blit(flag_img, (finish_line.x - 10, finish_line.y - 40))
        flag_frame += 1

        if player_rect.colliderect(finish_line):
            if all(asked_questions):  # all questions answered
                reached_finish = True
                win_sound.play()
                show_message("You Win!", YELLOW, 180)
                confetti = [{"x": random.randint(0, WIDTH), "y":random.randint(-HEIGHT, 0), "color": random.choice([RED, YELLOW, GREEN, WHITE])} for _ in range(50)]
            else:
                show_message("Answer all questions to finish!", RED)
                # Push the player back slightly to prevent re-colliding immediately
                player_x -= 20

        screen.blit(player_img_game, (player_x, player_y))

    elif reached_finish:
        pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, 60))
        for p in platforms: pygame.draw.rect(screen, BROWN, p)
        screen.blit(player_img_game, (player_x, player_y))
        screen.blit(flag_imgs[flag_frame // 30 % 2], (finish_line.x - 10, finish_line.y - 40))
        flag_frame += 1

        for c in confetti:
            pygame.draw.circle(screen, c["color"], (c["x"], int(c["y"])), 4)
            c["y"] += random.uniform(2, 5)
            if c["y"] > HEIGHT:
                c["y"] = 0
                c["x"] = random.randint(0, WIDTH)
        if current_level == len(levels) - 1:
            win_screen()  # Show win screen directly
        else:
            next_btn = draw_button("Next Level", WIDTH//2 - 100, 300)
            replay_btn = draw_button("Replay Level", WIDTH//2 - 100, 360)

    else:
        display_question(current_question)

    if message_timer > 0:
        msg_surface = medium_font.render(message, True, message_color)
        msg_rect = msg_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(msg_surface, msg_rect)
        message_timer -= 1

    # Display collected coins
    coin_count_text = font.render(f"Coins: {collected_coins}", True, BLACK)
    screen.blit(coin_count_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()