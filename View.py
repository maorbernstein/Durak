import Game
import pygame
import os, sys

class GameView:
    def __init__(self):
        pygame.init()
        self.width = 640
        self.height = 480
        self.screen = pygame.display.set_mode((self.width, self.height))
    def Loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

if __name__ == "__main__":
    gv = GameView()
    gv.Loop()
