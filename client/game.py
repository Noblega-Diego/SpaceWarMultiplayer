
import sys
import pygame
import client.basicElementGame.director as Director

class Game(Director.DirectorGame):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.__size = (1200, 800)
        self.__surface = pygame.display.set_mode(self.__size, vsync=0)
        pygame.display.set_caption('Cliente')

    def start(self):
        self.__flag_run = True
        self.runGame()

    def runGame(self):
        clock = pygame.time.Clock()
        while self.__flag_run:
            clock.tick(30)
            for event in pygame.event.get(pygame.QUIT):
                if (event.type == pygame.QUIT):
                    self.__flag_run = False
            if self.get_scene():
                self.get_scene().event()
                self.get_scene().update()
                self.get_scene().draw(self.__surface)
            pygame.display.update()
        pygame.quit()
        sys.exit()

