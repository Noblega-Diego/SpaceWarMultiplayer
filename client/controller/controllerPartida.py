from typing import Dict, List

from client.inputController.inputHandler import InputHandle
from client.multiplayer import LocalMultiplayer
from client.network import Network
from client.sprites.Sprite import Ship, Vala
from client.basicElementGame.director import DirectorGame
from client.ui.uiPartida import UiPartida
import pygame

class ControllerPartida:
    def __init__(self, director: DirectorGame):
        self.__director = director
        self.__naves: Dict[str, Ship] = {}
        self.__valas: List[Vala] = []
        self.__naveLocal = Ship()
        self.__naveLocal.changePos((0, 0))
        self.__contol = InputHandle()
        net = Network()
        self.__multiplayer = LocalMultiplayer(self, net)
        self.__gui: UiPartida = UiPartida()
        self.__ultimaNaveDisparada = None
        self.__fxShoot = pygame.mixer.Sound('client/assets/shootLaser.wav')
        self.__fxCollision = pygame.mixer.Sound('client/assets/collision.wav')

    def set_gui(self, gui):
        self.__gui = gui

    def updatePartida(self):

        if self.__multiplayer.isLogin():
            self.updatePLayerInput()

        for vala in self.__valas:
            if vala.get_duracion() == 0:
                self.__valas.remove(vala)

        self.__handleColliderValas()
        for vala in self.get_valas():
            vala.update()
        if (self.__multiplayer.isLogin()):
            for jugador in self.get_naves().values():
                jugador.update()
            self.get_naveLocal().update()


    def __handleColliderValas(self):
        navesTotales = [i for i in self.__naves.values()]
        navesTotales.append(self.__naveLocal)
        for vala in self.__valas:
            for nave in navesTotales:
                if vala.get_nave() != nave and nave.detectCollider(vala):
                    if vala.get_nave() == self.__naveLocal:
                        self.__gui.getStausVarEnemy().change_progres(nave.get_vida())
                        pygame.mixer.Sound.play(self.__fxCollision)
                        pygame.mixer.music.stop()
                    if nave == self.__naveLocal:
                        self.__naveLocal.set_vida(self.__naveLocal.get_vida() - 1)
                        if (self.__naveLocal.get_vida() <= 0):
                            self.__naveLocal.handle_event('KILL')
                            self.__multiplayer.sendObject([{'OP': {
                                'type': 'KILL',
                                'by': int(vala.get_nave().get_Id())
                            }}])
                            self.__multiplayer.quit()
                            from client.ui.menu import Menu
                            from .controllerMenu import ControllerMenu
                            menu = Menu()
                            controller = ControllerMenu(menu, self.__director)
                            self.__director.changeScene(menu)
                    self.__valas.remove(vala)
                    break


    def updatePLayerInput(self):
        self.__contol.handleMouse().ejecute(self.__naveLocal)
        cm_move = self.__contol.handleInput()
        if cm_move:
            cm_move.ejecute(self.__naveLocal)
            self.__multiplayer.sendObject([{'OP': {
                'type': 'MOVE_PLAYER',
                'pos': self.__naveLocal.get_pos(),
                'gr': self.__naveLocal.get_gr(),
                'vida': self.__naveLocal.get_vida(),
            }}])

    def player_fire(self, event):
        if (self.__naveLocal.get_vida() > 0):
            cm_shoot = self.__contol.handleShoot(event)
            if cm_shoot:
                cm_shoot.ejecute(self.__naveLocal, self)
                self.__multiplayer.sendObject([{'OP': {
                    'type': 'SHOOT',
                    'pos': self.__naveLocal.get_pos(),
                    'gr': self.__naveLocal.get_gr()
                }}])
                pygame.mixer.Sound.play(self.__fxShoot)
                pygame.mixer.music.stop()

    def get_valas(self):
        return self.__valas

    def get_naves(self):
        return self.__naves

    def get_naveLocal(self):
        return self.__naveLocal

    def get_multiplayer(self):
        return self.__multiplayer
