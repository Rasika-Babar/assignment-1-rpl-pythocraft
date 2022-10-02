import math
import random

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('ninja background.jpg')

# Sound
mixer.music.load("background music.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("NINJA WARRIOR")
icon = pygame.image.load('leonardo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('ninja (1).png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
appleImg = pygame.image.load('apple (1).png')
appleX = 370
appleY = 480
appleX = random.randint(0, 736)
appleY = random.randint(50, 150)
appleX_change = 0.6
appleY_change = 15

# Enemy
appleImg = []
appleX = []
appleY = []
appleX_change = []
appleY_change = []
num_of_apples = 6

for i in range(num_of_apples):
    appleImg.append(pygame.image.load('apple (1).png'))
    appleX.append(random.randint(0, 736))
    appleY.append(random.randint(50, 150))
    appleX_change.append(4)
    appleY_change.append(40)

    # Bullet

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

    starImg = pygame.image.load('star (1).png')
    starX = 0
    starY = 480
    starX_change = 0
    starY_change = 10
    star_state = "ready"

    # Score

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    testY = 10

    # Game Over
    over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def apple(x, y, i):
    screen.blit(appleImg[i], (x, y))


def fire_star(x, y):
    global star_state
    star_state = "fire"
    screen.blit(starImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if star_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    starX = playerX
                    fire_star(starX, starY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_apples):

        # Game Over
        if appleY[i] > 440:
            for j in range(num_of_apples):
                appleY[j] = 2000
            game_over_text()
            break

        appleX[i] += appleX_change[i]
        if appleX[i] <= 0:
            appleX_change[i] = 0.8
            appleY[i] += appleY_change[i]
        elif appleX[i] >= 736:
            appleX_change[i] = -1
            appleY[i] += appleY_change[i]

        # Collision
        collision = isCollision(appleX[i], appleY[i], starX, starY)
        if collision:
            explosionSound = mixer.Sound("explosion1.wav")
            explosionSound.play()
            starY = 480
            star_state = "ready"
            score_value += 1
            appleX[i] = random.randint(0, 736)
            appleY[i] = random.randint(50, 150)

        apple(appleX[i], appleY[i], i)

    # Bullet Movement
    if starY <= 0:
        starY = 480
        star_state = "ready"

    if star_state is "fire":
        fire_star(starX, starY)
        starY -= starY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
