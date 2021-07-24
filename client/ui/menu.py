from client.basicElementGame.scene import Scene
from client.basicElementGame.uiElements.basicEventUI import ListeinerEventUI, EventUI
from client.basicElementGame.uiElements.button import Button
import pygame



class Menu(Scene):
    __IMAGE_BACKGROUND = pygame.transform.scale(pygame.image.load('client/assets/imageMenu.jpg'), (1200,800))
    __bt_iniciar: Button = None

    def __init__(self):
        self.__initElements()

    def event(self):
        for event in pygame.event.get():
            self.__bt_iniciar.event(event)

    def update(self):
        self.__bt_iniciar.update()

    def draw(self, surface):
        surface.blit(self.__IMAGE_BACKGROUND, (0,0))
        self.__bt_iniciar.draw(surface)

    def __initElements(self):
        self.__bt_iniciar = Button((10,20), (100,30))


    def get_bt_iniciar(self):
        return self.__bt_iniciar
