
import abc

from client.basicElementGame.scene import Scene


class DirectorGame(abc.ABC):

    def __init__(self):
        self.__scene:Scene = None

    @abc.abstractmethod
    def runGame(self):
        pass

    def changeScene(self,  scene:Scene):
        self.__scene = scene

    def get_scene(self) -> Scene:
        return self.__scene