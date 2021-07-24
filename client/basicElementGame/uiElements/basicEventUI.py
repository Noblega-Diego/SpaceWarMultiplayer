from typing import List
from abc import ABC, abstractmethod
from pygame.rect import Rect


class EventUI():
    def __init__(self, source, type):
        self.__source = source
        self.type = type

    def get_source(self):
        return self.__source

    def get_type(self):
        return self.type


class ListeinerEventUI(ABC):
    @abstractmethod
    def handlee_event(self, event: EventUI):
        pass


class ElementUI():
    def __init__(self):
        self.__listeinertsEvent: List[ListeinerEventUI] = []

    def event(self):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

    def _lunchEvent(self, type):
        for listeiner in self.__listeinertsEvent:
            listeiner.handlee_event(EventUI(self, type))

    def add_listeinerEvent(self, listeiner: ListeinerEventUI):
        self.__listeinertsEvent.append(listeiner)

    def get_listeinersEvent(self):
        return self.__listeinertsEvent
