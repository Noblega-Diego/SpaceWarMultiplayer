import pygame
from pygame.rect import Rect
from client.basicElementGame.uiElements.basicEventUI import ElementUI

class BarraVida(ElementUI):
    def __init__(self, pos):
        super().__init__()
        self.__width = 400
        self.__rectBack = Rect(pos[0], pos[1], self.__width, 10)
        self.__rectProgres = Rect(pos[0], pos[1], self.__width, 10)
        self.__pos = pos

    def event(self):
        pass


    def update(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, (100,100,100), self.__rectBack)
        pygame.draw.rect(surface, (100,200,200), self.__rectProgres)


    def change_progres(self, value):
        status = (value * self.__width) / 100
        self.__rectProgres.width = status


    def set_pos(self, pos):
        self.__pos = pos
