import math
import sys
from typing import Dict, Tuple, List

import pygame
from client.network import Network
from client.sprites.Sprite import Nave, Vala
from client.multiplayer import LocalMultiplayer
from client.inputController.inputHandler import InputHandle


class Game:
    def __init__(self):
        pygame.init()
        self.__jugadores:Dict[str, Nave] = {}
        self.__jugadorLocal = Nave()
        self.__jugadorLocal.changePos((0,0))
        self.__size = (1200, 800)
        self.__surface = pygame.display.set_mode(self.__size, vsync=0)
        pygame.display.set_caption('Cliente')
        net = Network()
        self.__multiplayer = LocalMultiplayer(self, net)
        self.__contol = InputHandle()
        self.background = pygame.image.load('client/assets/space.png')
        self.__flag_run = False
        self.__flag_login = False
        self.valas: List[Vala] = []

    def start(self):
        self.__flag_run = True
        self.__run()


    def __run(self):
        clock = pygame.time.Clock()
        self.__multiplayer.start()
        while self.__flag_run:
            clock.tick(30)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.__flag_run = False
                self.player_fire(event)
            if self.__multiplayer.isLogin():
                self.updatePLayerInput()
            for i in self.valas:
                if i.get_duracion() == 0:
                    self.valas.remove(i)

            for vala in self.valas:
                if vala.get_nave() != self.__jugadorLocal:
                    if self.__jugadorLocal.detectCollider(vala):
                        self.valas.remove(vala)
                        self.__jugadorLocal.set_vida(self.__jugadorLocal.get_vida() - 1)
                        if(self.__jugadorLocal.get_vida() <= 0):
                            self.__multiplayer.sendObject([{'OP': {
                                                               'type': 'KILL',
                                                               'by':int(vala.get_nave().get_Id())
                                                           }}])
            self.draw()
            pygame.display.update()
        self.__multiplayer.quit()
        pygame.quit()
        sys.exit()


    def draw(self):
        self.__surface.blit(self.background, (0,0))
        for vala in self.valas:
            vala.update()
            imagedraw = pygame.transform.rotate(vala.image, vala.get_gr())
            rect = imagedraw.get_rect()
            rect.center = vala.get_pos()
            self.__surface.blit(imagedraw, rect)
        if (self.__multiplayer.isLogin()):
            for jugador in self.__jugadores.values():
                if(jugador.get_vida() > 0):
                    jugador.draw(self.__surface)
            if (self.__jugadorLocal.get_vida() > 0):
                self.__jugadorLocal.draw(self.__surface)

    def updatePLayerInput(self):
        self.__contol.handleMouse().ejecute(self.__jugadorLocal)
        cm_move = self.__contol.handleInput()
        if cm_move:
            cm_move.ejecute(self.__jugadorLocal)
            self.__multiplayer.sendObject([{'OP': {
                'type': 'MOVE_PLAYER',
                'pos': self.__jugadorLocal.get_pos(),
                'gr': self.__jugadorLocal.get_gr()
            }}])

    def player_fire(self, event):
        if(self.__jugadorLocal.get_vida() >= 0):
            cm_shoot = self.__contol.handleShoot(event)
            if cm_shoot:
                cm_shoot.ejecute(self.__jugadorLocal, self)
                self.__multiplayer.sendObject([{'OP': {
                                                   'type': 'SHOOT',
                                                   'pos': self.__jugadorLocal.get_pos(),
                                                   'gr': self.__jugadorLocal.get_gr()
                                                   }}])



    def get_players(self):
        return self.__jugadores

    def get_localPlayer(self):
        return self.__jugadorLocal

    def set_localPlayer(self, player):
        self.__jugadorLocal = player
