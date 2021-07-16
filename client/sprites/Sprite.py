from typing import Tuple
import pygame, math


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.vel = 4
        self.__pos = (0,0)
        self.__id = None
        self.__color = None
        self.image = pygame.image.load('client/assets/sprite_nave.png')
        self.imagedraw = self.image
        self.rect = self.image.get_rect()
        self.grd = 0
        self.__vida = 10

    def changePos(self, pos:Tuple[int,int]):
        self.__pos = pos
        self.rect.center = self.__pos

    def set_Id(self, id:str):
        self.__id = id

    def get_Id(self):
        return self.__id

    def get_pos(self):
        return self.__pos

    def set_color(self,color):
        self.__color = color

    def get_color(self):
        return self.__color

    def get_rect(self):
        return self.rect

    def get_gr(self):
        return self.grd

    def set_gr(self, gr):
        self.grd = gr
        self.imagedraw = pygame.transform.rotate(self.image, self.grd)
        self.rect = self.imagedraw.get_rect()
        self.rect.center = self.__pos


    def set_vida(self, value):
        self.__vida = value

    def get_vida(self):
        return self.__vida

    def draw(self, surface):
        surface.blit(self.imagedraw, self.rect)

    def detectCollider(self, vala):
        mask = pygame.mask.from_surface(self.imagedraw)
        maskVala = pygame.mask.from_surface(vala.image)
        vrect = vala.get_pos()
        oX = vrect[0] - self.rect[0]
        oY = vrect[1] - self.rect[1]
        if mask.overlap(maskVala, (oX,oY)):
            print('colision')
            return True
        return False

class Vala(pygame.sprite.Sprite):
    image = pygame.image.load('client/assets/vala.png')

    def __init__(self, pos, gr, nave:Nave):
        super().__init__()
        self.__pos = pos
        self.__posInicial = pos
        self.__nave:Nave = nave
        self.__color = None
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos
        self.grd = gr
        self.__duracion = 200

    def get_gr(self):
        return self.grd

    def set_gr(self, gr):
        self.grd = gr

    def get_pos(self):
        return (int(self.__pos[0]), int(self.__pos[1]))

    def set_Pos(self, pos:Tuple[int,int]):
        self.__pos = pos
        self.rect.center = self.__pos

    def get_nave(self):
        return self.__nave

    def update(self):
        self.__duracion -= 4
        if self.__duracion < 0:
            self.__duracion = 0
        r = 8
        y = math.sin(math.radians(self.grd + 90))*r
        x = math.cos(math.radians(self.grd + 90))*r
        self.__pos = (self.__pos[0] + x, self.__pos[1] - y)
        self.rect.center = self.__pos

    def get_duracion(self):
        return self.__duracion
