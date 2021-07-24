
from .basicEventUI import ElementUI
import pygame
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.event import Event
class Button(ElementUI):
    def __init__(self, pos = None, size = None):
        super().__init__()
        self.__pos = pos
        self.__size = size
        self.__rect = Rect(pos[0], pos[1], size[0], size[1])
        self.__color = (122,122,121)

    def event(self, event:Event):
        if event != None:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                mousePos = pygame.mouse.get_pos()
                if(self.__rect.collidepoint(mousePos)):
                    self._lunchEvent('click')

    def update(self):
        pass

    def draw(self, surface: Surface):
        pygame.draw.rect(surface,self.__color, self.__rect)

    def set_pos(self, pos):
        self.__pos = pos

    def set_size(self, size):
        self.__size = size

    def _lunchEvent(self, type):
        super()._lunchEvent(type)
