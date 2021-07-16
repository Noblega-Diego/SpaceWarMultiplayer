import pygame
from .command import Command
import client.inputController.command as command


class InputHandle:
    __cm_up: Command
    __cm_down: Command
    __cm_left: Command
    __cm_right: Command
    __cm_rotate: Command
    __cm_fire: command.CommandFire

    def __init__(self):
        self.__cm_up = command.CommandMoveUp()
        self.__cm_down = command.CommandMoveDown()
        self.__cm_left = command.CommandMoveLeft()
        self.__cm_right = command.CommandMoveRight()
        self.__cm_rotate = command.CommandRotate()
        self.__cm_fire = command.CommandFire()

    def handleInput(self) -> Command:
        keys = pygame.key.get_pressed()
        com = command.CommandCombined()
        if keys[pygame.K_w]: com.addComand(self.__cm_up)
        if keys[pygame.K_s]: com.addComand(self.__cm_down)
        if keys[pygame.K_a]: com.addComand(self.__cm_left)
        if keys[pygame.K_d]: com.addComand(self.__cm_right)
        return com

    def handleMouse(self) -> Command:
        return self.__cm_rotate

    def handleShoot(self, event) -> command.CommandFire:
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            return self.__cm_fire
        return None