
from client.ui.menu import Menu
from client.basicElementGame.uiElements.basicEventUI import ListeinerEventUI, EventUI
from client.controller.controllerPartida import ControllerPartida
from client.basicElementGame.director import DirectorGame
from client.scenes.partida import Partida


class ControllerMenu(ListeinerEventUI):

    def __init__(self, menu:Menu, director:DirectorGame):
        self.__menu = menu
        self.__menu.get_bt_iniciar().add_listeinerEvent(self)
        self.__director = director

    def handlee_event(self, event: EventUI):
        if event.type == 'click' and event.get_source() == self.__menu.get_bt_iniciar():
            partida = Partida(ControllerPartida(self.__director))
            partida.start()
            self.__director.changeScene(partida)

    def update(self):
        pass