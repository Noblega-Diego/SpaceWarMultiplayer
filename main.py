
from client.game import Game
from client.ui.menu import Menu
from client.controller.controllerMenu import ControllerMenu
def main():
    game = Game()
    menu = Menu()
    controllerMenu = ControllerMenu(menu,game)
    game.changeScene(menu)
    game.start()

if (__name__ == "__main__"):
    main()


