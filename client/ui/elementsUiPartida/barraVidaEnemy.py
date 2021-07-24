import pygame
from pygame.rect import Rect
from client.basicElementGame.uiElements.basicEventUI import ElementUI

class BarraVida(ElementUI):
    def __init__(self, pos):
        super().__init__()
        self.__width = 100
        self.__statusProgres = 0
        self.__rectBack = Rect(pos[0], pos[1],self.__width, 5)
        self.__rectProgres = Rect(pos[0], pos[1], self.__statusProgres, 5)
        self.__pos = pos
        self.isdraw = True

    def event(self):
        pass

    def update(self):
        self.__rectProgres.center = (self.__pos[0]+self.__rectProgres.width/2 - self.__rectBack.width/2,self.__pos[1])
        self.__rectProgres.width = self.__statusProgres
        self.__rectBack.center = self.__pos

    def draw(self, surface):
        if self.isdraw:
            pygame.draw.rect(surface, (100,100,100), self.__rectBack)
            pygame.draw.rect(surface, (200,0,0), self.__rectProgres)

    def change_progres(self, value):
        self.__statusProgres = (value * self.__width)/100

    def set_pos(self, pos):
        self.__pos = pos
