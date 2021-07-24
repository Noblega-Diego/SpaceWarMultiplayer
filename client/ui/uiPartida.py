import pygame.display
from pygame.surface import Surface

from client.basicElementGame.scene import Scene
from client.ui.elementsUiPartida.barraVida import BarraVida
from client.ui.elementsUiPartida.barraVidaEnemy import BarraVida as BarraVidaEnemigo



class UiPartida(Scene):
    __STATUS_BAR = BarraVida((10,10))
    __STATUS_BAR_ENEMIGO = BarraVidaEnemigo((1200-110,10))

    def event(self):
        self.__STATUS_BAR.event()
        self.__STATUS_BAR_ENEMIGO.event()

    def update(self):
        self.__STATUS_BAR.update()
        self.__STATUS_BAR_ENEMIGO.update()

    def draw(self, surface: Surface):
        self.__STATUS_BAR.draw(surface)
        self.__STATUS_BAR_ENEMIGO.draw(surface)

    def getStausVar(self):
        return self.__STATUS_BAR

    def getStausVarEnemy(self):
        return self.__STATUS_BAR_ENEMIGO