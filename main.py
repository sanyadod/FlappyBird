import pygame
import random

pygame.init()
clock = pygame.time.Clock()  #create an object to help track time

pygame.display.set_caption('Flappy bird -Sanya')
screen = pygame.display.set_mode((288, 512))


def rotateBird(b):
    new_bird = pygame.transform.rotozoom(b,-birdY * 3, 1) #rotate image
    return new_bird


bg = pygame.image.load('img/bg.png')
base = pygame.image.load('img/base.png' )
baseX = 0


def scores():
    font = pygame.font.Font('img/04B_19.TTF', 25)
    text = font.render(f'Score:{str(sc)}', True, (255, 255, 255))
    textRect = text.get_rect(center=(144, 50))
    screen.blit(text, textRect)


def highScores():
    font = pygame.font.Font('img/04B_19.TTF', 25)
    text = font.render(f'High score:{str(highscore)}', True, (255, 255, 255))
    textRect = text.get_rect(center=(144, 400))
    screen.blit(text, textRect)


highscore = 0
# pipe
pipeBottom = pygame.image.load('img/pipe.png')
pipeTop = pygame.image.load('img/pipe2.png')
pipeList = []
PIPE = pygame.USEREVENT  #creates the pipe as event
pygame.time.set_timer(PIPE, 1200)  # new pipe create 1.2 sec

# bird
bird1 = pygame.image.load('img/bird1.png')
bird2 = pygame.image.load('img/bird2.png')
bird3 = pygame.image.load('img/bird3.png')
birdFrames = [bird1, bird2, bird3]
birdIndex = 0

#  for animation
BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)  # to post a custom event at specific time interval
bird = birdFrames[birdIndex]

# variable for bird
birdY = 0  # y coordinate of the bird
birdRect = bird.get_rect(center=(100, 200))  # put rectangle around it to detect collision and for rotation
gravity = 0.15  # variable created to make the bird  move down

wing = pygame.mixer.Sound('sound/wing.wav')
miss = pygame.mixer.Sound('sound/miss.wav')
point = pygame.mixer.Sound('sound/point.wav')

sc = 0

# home screen
homeScreen = pygame.image.load('img/homescreen.png')
homeScreenRect = homeScreen.get_rect(center=(144, 250))
run = True
game_active = True
while run:
    # event loop
    for event in pygame.event.get():
        # to end the screen
        if event.type == pygame.QUIT:
            run = False
        # to move the bird up when user presses space bar or up key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                birdY = 0
                birdY -= 4
                wing.play()

            #  to restart game
            if event.key == pygame.K_SPACE and game_active == False:
                sc = 0
                game_active = True
                pipeList.clear()
                birdRect.center = (100, 266)
                bird_y = 0

        #  creates a list of pipes with various dimensions
        if event.type == PIPE:
            pipe_y = random.randint(200, 400)
            pipeList.append([pipeBottom.get_rect(midtop=(700, pipe_y)),
                             pipeTop.get_rect(midbottom=(700, pipe_y - 175))])  # adds a list of new pipes

        #  bird flap
        if event.type == BIRD_FLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0

            bird = birdFrames[birdIndex]

    # paste background
    screen.blit(bg, (0, 0))

    if game_active == True:
        # paste the moving bird
        birdY += gravity
        rotated_bird = rotateBird(bird)
        birdRect.centery += birdY
        screen.blit(rotateBird(bird), birdRect)

        #  collision of bird with pipes
        for p in pipeList:
            if birdRect.colliderect(p[0]) or birdRect.colliderect(p[1]):
                miss.play()
                game_active = False

        #  to make the pipes move horizontally
        for p in pipeList:
            p[0].centerx -= 5
            p[1].centerx -= 5
            screen.blit(pipeBottom, p[0])
            screen.blit(pipeTop, p[1])

            #  scoring
            if p[0].centerx == 100:
                sc += 1
                point.play()

        # if bird hits the floor or if bird goes high up
        if birdRect.top < -12 or birdRect.bottom >= 438:
            miss.play()
            game_active = False

    # move the base
    baseX -= 1
    screen.blit(base, (baseX, 440))
    screen.blit(base, (baseX + 200, 440))
    if baseX < -200:
        baseX = 0

    # for home screen
    if game_active == False:
        if sc > highscore:
            highscore = sc
        screen.blit(homeScreen, homeScreenRect)
        highScores()

    # to update screen
    clock.tick(60)  # max 60 fps
    scores()
    pygame.display.update()  # put everything after while loop and put in display screen
pygame.quit()
