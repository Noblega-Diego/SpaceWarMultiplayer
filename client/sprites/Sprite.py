from typing import Tuple, List
import pygame, math


class Ship(pygame.sprite.Sprite):

    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3

    def __init__(self):
        super().__init__()
        self.vel = 4
        self.__pos: Tuple[int, int] = (0,0)
        self.__id = None
        self.__color = None
        self.image = None
        self.rect = None
        self.__grados = 0
        self.__vida = 50
        from client.sprites.shipState import StateShip, StillShip
        self.__state: StateShip = StillShip()
        self.__state.start(self)
        self.imagedraw = self.image

    def handle_event(self, event):
        state = self.__state.handle_event(self, event)
        if(state != None and state != self.__state):
            self.__state = state
            self.__state.start(self)

    def update(self):
        self.handle_event('UPDATE')
        if (self.get_vida() <= 0):
            self.handle_event('KILL')
        self.__state.update(self)
        self.imagedraw = pygame.transform.rotate(self.image, self.__grados)
        self.rect = self.imagedraw.get_rect()
        self.rect.center = self.__pos

    def draw(self, surface):
        surface.blit(self.imagedraw, self.rect)

    def detectCollider(self, vala):
        mask = pygame.mask.from_surface(self.imagedraw)
        maskVala = pygame.mask.from_surface(vala.image)
        vrect = vala.get_pos()
        oX = vrect[0] - self.rect[0]
        oY = vrect[1] - self.rect[1]
        if mask.overlap(maskVala, (oX,oY)):
            return True
        return False

    def changePos(self, pos:Tuple[int,int]):
        self.__pos = pos

    def changeImage(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos
        self.imagedraw = self.image

    def change_direccion(self, direccion):
        traslate:List[int] = [0,0]
        x, y = self.get_pos()
        if (direccion == self.MOVE_UP):
            traslate = [0, -self.vel]
        elif (direccion == self.MOVE_DOWN):
            traslate = [0, self.vel]
        elif (direccion == self.MOVE_LEFT):
            traslate = [-self.vel, 0]
        elif (direccion == self.MOVE_RIGHT):
            traslate = [self.vel, 0]
        self.changePos((x + traslate[0], y + traslate[1]))

    def set_Id(self, id:str):
        self.__id = id

    def get_Id(self):
        return self.__id

    def get_pos(self):
        return self.__pos

    def set_color(self,color):
        if(color != None):
            self.__color = color
            for x in range(self.image.get_width()):
                for y in range(self.image.get_height()):
                    pixelColor = self.image.get_at((x, y))  # Preserve the alpha value.
                    if pixelColor == (200, 95, 95, 255):
                        self.image.set_at((x, y), color)  # Set the color of the pixel.

    def get_color(self):
        return self.__color

    def get_rect(self):
        return self.rect

    def get_gr(self):
        return self.__grados

    def set_gr(self, gr):
        self.__grados = gr

    def set_vida(self, value):
        self.__vida = value

    def get_vida(self):
        return self.__vida


class Vala(pygame.sprite.Sprite):
    image = pygame.image.load('client/assets/vala.png')
    __velocidad = 8
    def __init__(self, pos, gr, nave:Ship):
        super().__init__()
        self.__pos = pos
        self.__posInicial = pos
        self.__source:Ship = nave
        self.rect = self.image.get_rect()
        self.rect.center = self.__pos
        self.__grados = gr
        self.__duracion = 200
        self.__imagedraw = self.image
        self.__rotate = True
        self.__direction = (0,0)

    def draw(self, surface):
        if (self.__duracion > 0):
            surface.blit(self.__imagedraw, self.rect)

    def get_gr(self):
        return self.__grados

    def set_gr(self, gr):
        self.__rotate = True
        self.__grados = gr

    def get_pos(self):
        return (int(self.__pos[0]), int(self.__pos[1]))

    def set_Pos(self, pos:Tuple[int, int]):
        self.__pos = pos

    def get_nave(self):
        return self.__source

    def update(self):
        if(self.__duracion > 0):
            self.__duracion -= 4
            if (self.__rotate):
                r = self.__velocidad
                y = math.sin(math.radians(self.__grados + 90)) * r
                x = math.cos(math.radians(self.__grados + 90)) * r
                self.__direction = (x, y)
                self.__imagedraw = pygame.transform.rotate(self.image, self.get_gr())
                self.rect = self.__imagedraw.get_rect()
                self.__rotate = False
            x, y = self.__direction
            self.__pos = (self.__pos[0] + x, self.__pos[1] - y)
            self.rect.center = self.__pos

    def get_duracion(self):
        return self.__duracion
