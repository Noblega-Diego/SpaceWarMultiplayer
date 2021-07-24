import abc
import math

import pygame

from client.sprites.Sprite import Ship, Vala


class Command(abc.ABC):
    @abc.abstractmethod
    def ejecute(self, nave: Ship):
        pass


class CommandCombined(Command):

    def __init__(self):
        self.__listCommand = []

    def addComand(self, command:Command):
        self.__listCommand.append(command)

    def ejecute(self, nave: Ship):
        for command in self.__listCommand:
            command.ejecute(nave)


class CommandMoveUp(Command):

    def ejecute(self, nave: Ship):
        self.__move_up(nave)

    def __move_up(self, nave: Ship):
        nave.change_direccion(nave.MOVE_UP)

class CommandMoveDown(Command):

    def ejecute(self, nave: Ship):
        self.__move_down(nave)

    def __move_down(self, nave: Ship):
        nave.change_direccion(nave.MOVE_DOWN)

class CommandMoveLeft(Command):

    def ejecute(self, nave: Ship):
        self.__move_left(nave)

    def __move_left(self, nave: Ship):
        nave.change_direccion(nave.MOVE_LEFT)

class CommandMoveRight(Command):

    def ejecute(self, nave: Ship):
        self.__move_right(nave)

    def __move_right(self, nave: Ship):
        nave.change_direccion(nave.MOVE_RIGHT)

class CommandSpeedUp(Command):

    def ejecute(self, nave: Ship):
        nave.handle_event('TURBO')

class CommandRotate(Command):

    def ejecute(self, nave: Ship):
        self.__move_rotate(nave)

    def __move_rotate(self, nave: Ship):
        posMouse = pygame.mouse.get_pos()
        posPlayer = nave.get_pos()
        gr = math.degrees(math.atan2(-posMouse[1] + posPlayer[1], posMouse[0] - posPlayer[0])) - 90
        nave.set_gr(int(gr))

class CommandFire(Command):

    def ejecute(self, nave: Ship, controller):
        self.__Fire(nave, controller)

    def __Fire(self, nave: Ship, controller):
        controller.get_valas().append(Vala(nave.get_pos(), nave.get_gr(), nave))