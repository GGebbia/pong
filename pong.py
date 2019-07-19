import pygame, sys
from pygame.locals import *
from math import sin, cos, pi
import random


FPS = 60
WINDOWWIDTH = 600
WINDOWHEIGHT = 430
SQUARESIZE = 10

RADIUS = 40
ANGLE = 0


# R G B
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
BGCOLOR = BLACK

# Dividir el jugador en dos partes tal que en función de la última pared con el que ha chocado la bola, el angulo
# resultante con el jugador sea mayor o menor.

# Aumentar la velocidad de la bola cada vez que choca con un jugador.
# Aumentar / disminuir velocidad bola en funcion de la region de choque.


def perimeter(center, radius):
    per_points = []
    for angle in range(360):
        x, y = (center[0] + radius * cos(angle * pi / 180), center[1] + radius * sin(angle * pi / 180))
        per_points.append(pygame.Rect(x, y, 1, 1))
    return per_points


class Ball:

    def __init__(self):
        self.center = [WINDOWWIDTH // 2, WINDOWHEIGHT // 2]
        self.radius = 10
        poss_angles = list(range(31)) + list(range(150, 211)) + list(range(330, 360))

        self.angle = random.choice(poss_angles) * 2 * pi / 360

        self.mod = 5
        self.vel = [self.mod * cos(self.angle), self.mod * sin(self.angle)]

    def percollide(self):
        self.percol = perimeter(self.center, self.radius)

    def speedup(self):
        self.mod*= 1.05
        self.vel = [self.mod * cos(self.angle), self.mod * sin(self.angle)]

    def update(self):
        self.show()
        self.move()
        self.percollide()

    def move(self):
        self.center[0] += round(self.vel[0])
        self.center[1] += round(self.vel[1])

    def show(self):
        circle = pygame.draw.circle(DISPLAYSURF, WHITE, self.center, self.radius)


class Player:

    def __init__(self, player=1):
        self.width = 10
        self.height = 50
        self.x = 30
        self.y = (WINDOWHEIGHT - self.height) // 2
        self.speed = 5
        self.player = player

        if player == 1:
            self.x = 30
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else:
            self.x = WINDOWWIDTH - self.width - 30
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        if self.player == 1:
            keys = pygame.key.get_pressed()
            wallup, walldown = borders()
            if keys[pygame.K_w]:
                if self.y > wallup.height + self.speed:
                    self.y -= self.speed
                else:
                    self.y = wallup.height
            if keys[pygame.K_s]:
                if self.y < walldown[1] - self.height - self.speed:
                    self.y += self.speed
                else:
                    self.y = walldown[1] - self.height
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else:
            keys = pygame.key.get_pressed()
            wallup, walldown = borders()
            if keys[pygame.K_UP]:
                if self.y > wallup.height + self.speed:
                    self.y -= self.speed
                else:
                    self.y = wallup.height
            if keys[pygame.K_DOWN]:
                if self.y < walldown[1] - self.height - self.speed:
                    self.y += self.speed
                else:
                    self.y = walldown[1] - self.height
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def show(self):
        pygame.draw.rect(DISPLAYSURF, WHITE, self.rect)

    def update(self):

        self.move()
        self.show()


class Collisions:

    def __init__(self):
        self.wallup, self.walldown = borders()

    def collide(self, player1, player2, ball):

        points = ball.percol
        if player1.rect.collidelist(points)!= -1 or player2.rect.collidelist(points) != -1:
            #ball.speedup()
            ball.vel[0] = -ball.vel[0]
        if self.wallup.collidelist(points)!= -1 or self.walldown.collidelist(points) != -1:
            #ball.speedup()
            ball.vel[1] = -ball.vel[1]

    def update(self,  player1, player2, ball):
        self.collide(player1, player2, ball)


def quitgame():
    pygame.quit()
    sys.exit()


def borders():
    global DISPLAYSURF
    wallup = pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(0, 0, WINDOWWIDTH, 10))
    walldown = pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(0,  WINDOWHEIGHT - 10 , WINDOWWIDTH, 10))
    return [wallup, walldown]


def mid_line():
    for i in range(0, WINDOWHEIGHT , 20):
        pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect((WINDOWWIDTH - SQUARESIZE) // 2, i, SQUARESIZE, SQUARESIZE))


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, ANGLE

    # Initialization
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pong')

    player1 = Player(1)
    player2 = Player(2)

    ball = Ball()

    collisions = Collisions()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quitgame()

        DISPLAYSURF.fill((0, 0, 0))

        borders()
        mid_line()


        ball.update()
        collisions.update(player1, player2, ball)
        player1.update()
        player2.update()


        if ball.percol[1][0] < 0 or ball.percol[0][0] > WINDOWWIDTH:
            ball = Ball()
        pygame.display.flip ()
        FPSCLOCK.tick(FPS)


main()
