import abc
import math

import pygame

from client.sprites.Sprite import Nave, Vala


class Command(abc.ABC):
    @abc.abstractmethod
    def ejecute(self, nave: Nave):
        pass


class CommandCombined(Command):

    def __init__(self):
        self.__listCommand = []

    def addComand(self, command:Command):
        self.__listCommand.append(command)

    def ejecute(self, nave: Nave):
        for command in self.__listCommand:
            command.ejecute(nave)


class CommandMoveUp(Command):

    def ejecute(self, nave: Nave):
        self.__move_up(nave)

    def __move_up(self, nave: Nave):
        x, y = nave.get_pos()
        nave.changePos((x, y - nave.vel))

class CommandMoveDown(Command):

    def ejecute(self, nave: Nave):
        self.__move_down(nave)

    def __move_down(self, nave: Nave):
        x, y = nave.get_pos()
        nave.changePos((x, y + nave.vel))

class CommandMoveLeft(Command):

    def ejecute(self, nave: Nave):
        self.__move_left(nave)

    def __move_left(self, nave: Nave):
        x, y = nave.get_pos()
        nave.changePos((x - nave.vel, y))

class CommandMoveRight(Command):

    def ejecute(self, nave: Nave):
        self.__move_right(nave)

    def __move_right(self, nave: Nave):
        x, y = nave.get_pos()
        nave.changePos((x + nave.vel, y))

class CommandRotate(Command):

    def ejecute(self, nave: Nave):
        self.__move_rotate(nave)

    def __move_rotate(self, nave: Nave):
        posMouse = pygame.mouse.get_pos()
        posPlayer = nave.get_pos()
        gr = math.degrees(math.atan2(-posMouse[1] + posPlayer[1], posMouse[0] - posPlayer[0])) - 90
        nave.set_gr(int(gr))

class CommandFire(Command):

    def ejecute(self, nave: Nave, game):
        self.__Fire(nave, game)

    def __Fire(self, nave: Nave, game):
        game.valas.append(Vala(nave.get_pos(), nave.get_gr(), nave))