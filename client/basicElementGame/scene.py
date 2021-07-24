
from abc import ABC,abstractmethod
from pygame.surface import Surface
class Scene(ABC):

    @abstractmethod
    def event(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, surface:Surface):
        pass