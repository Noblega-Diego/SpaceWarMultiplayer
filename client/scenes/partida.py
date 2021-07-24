import pygame

from client.basicElementGame.scene import Scene
from client.ui.uiPartida import UiPartida

class Partida(Scene):

    __GUI = UiPartida()

    def __init__(self, controllerPartida):
        self.__background = pygame.image.load('client/assets/space.png')
        from client.controller.controllerPartida import ControllerPartida
        self.__controller:ControllerPartida = controllerPartida
        self.__controller.set_gui(self.__GUI)

    def event(self):
        for event in pygame.event.get():
            self.__controller.player_fire(event)
        self.__controller.updatePLayerInput()
        self.__GUI.event()

    def update(self):
        self.__controller.updatePartida()
        self.__GUI.update()

    def draw(self, surface):
        surface.blit(self.__background, (0, 0))
        for vala in self.__controller.get_valas():
            vala.draw(surface)
        if (self.__controller.get_multiplayer().isLogin()):
            for jugador in self.__controller.get_naves().values():
                jugador.draw(surface)
            self.__controller.get_naveLocal().draw(surface)
            self.__GUI.getStausVar().change_progres(self.__controller.get_naveLocal().get_vida())
        self.__GUI.draw(surface)

    def start(self):
        self.__controller.get_multiplayer().start()

    def get_GUI(self):
        return self.__GUI
