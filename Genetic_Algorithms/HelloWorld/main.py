import pygame
from pygame.locals import *
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
player_image = pygame.image.load('player.png').convert()
background = pygame.image.load('liquid.jpeg').convert()

class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)
    def move(self):
        self.pos = self.pos.move(0, self.speed)
        if self.pos.right > 600:
            self.pos.left = 0

#class Game
#j    def __init__(self, background, player):
 #       self.player = Game

def init():
    player = GameObject(player_image, 113, 2)
    screen.blit(background, (0, 0))

def erase():
    screen.blit(background, player.pos, player.pos)

def move():
    player.move()

def draw():
    screen.blit(player.image, player.pos)
    pygame.display.update()

def main():
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((20, 20), (30, 30)))
    while 1:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                print("exited normally")
                sys.exit()
        erase()
        move()
        draw()

if __name__ == '__main__':
    main()
