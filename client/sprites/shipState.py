
from abc import ABC, abstractmethod

import pygame

from client.sprites.Sprite import Ship


class StateShip(ABC):

    @abstractmethod
    def handle_event(self, ship:Ship, imput:str):
        pass

    @abstractmethod
    def start(self, ship:Ship):
        pass

    @abstractmethod
    def update(self, ship:Ship):
        pass

class StillShip(StateShip):

    def __init__(self):
        self.__coolPower = 50

    def handle_event(self, ship: Ship, imput: str):
        if(imput == 'KILL'):
            return KillShip()
        elif(imput == 'TURBO'):
            if self.__coolPower <= 0:
                return TurboShip()
        return None

    def start(self, ship: Ship):
        ship.changeImage(pygame.image.load('client/assets/sprite_nave.png'))
        ship.set_color(ship.get_color())

    def update(self, ship: Ship):
        if self.__coolPower > 0:
            self.__coolPower -= 1
        else:
            self.__coolPower = 0

    def set_coolPower(self, cool):
        self.__coolPower = cool

class KillShip(StateShip):
    frame_width = 40
    frame_height = 40

    def __init__(self):
        self.__current_frame = 0
        self.__vel_frame = 0.15
        self.__val = 0
        self.image = pygame.image.load('client/assets/explosion.png')

    def handle_event(self, ship: Ship, imput: str):
        return None

    def start(self, ship: Ship):
        pass

    def update(self, ship: Ship):
        if(self.__current_frame <= 6):
            if(self.__val >= 1):
                new_area = pygame.Rect((self.__current_frame * self.frame_width, 0, self.frame_width, self.frame_height))
                ship.changeImage(self.image.subsurface(new_area))
                self.__current_frame += 1
                self.__val = 0
            else:
                self.__val += self.__vel_frame


class TurboShip(StateShip):

    def __init__(self):
        self.augmentSpeed = 8
        self.time = 0

    def handle_event(self, ship: Ship, imput: str):

        if (imput == 'DEFAULT'):
            ship.vel -= self.augmentSpeed
            return StillShip()
        elif (imput == 'UPDATE'):
            if self.time >= 4:
                ship.vel -= self.augmentSpeed
                newState = StillShip()
                return newState
        if (imput == 'KILL'):
            return KillShip()
        return None

    def start(self, ship: Ship):
        ship.vel += self.augmentSpeed

    def update(self, ship: Ship):
        if self.time < 4:
            self.time += 1
        else:
            self.time = 4