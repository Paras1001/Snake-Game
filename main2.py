
import pygame
import random
import os

pygame.mixer.init()

pygame.init()

pygame.mixer.music.load("laden.mp3")
pygame.mixer.music.play()


# Colors define
white = (255, 255, 255)
blue = (0, 0, 204)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
dis_width = 900
dis_height = 600
window = pygame.display.set_mode((dis_width, dis_height))

# Background Image
bgimg = pygame.image.load("back.jpg")
bgimg = pygame.transform.scale(bgimg, (dis_width, dis_height)).convert_alpha()


# Game Title
pygame.display.set_caption("SNAKE GAME")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    window.blit(screen_text, [x, y])


def plot_snake(window, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(window, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        window.fill((233, 210, 229))
        text_screen("Welcome to SNAKE GAME", black, 220, 250)
        text_screen("Press Space Bar To Play", blue, 228, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('theme.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # Check if hiscore file exists
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, dis_width / 2)
    food_y = random.randint(20, dis_height / 2)

    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open("Hiscore.txt", "w") as f:
                f.write(str(hiscore))
            window.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(20, dis_width / 2)
                food_y = random.randint(20, dis_height / 2)
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

            window.fill(white)
            window.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Hiscore: " + str(hiscore), red, 5, 5)
            pygame.draw.rect(window, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('smash.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > dis_width or snake_y < 0 or snake_y > dis_height:
                game_over = True
                pygame.mixer.music.load("smash.mp3")
                pygame.mixer.music.play()
            plot_snake(window, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
