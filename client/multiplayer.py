
from .network import Network
import json
from .sprites.Sprite import Vala,Ship
import threading

class LocalMultiplayer(threading.Thread):

    OP_LOGIN = 'LOGIN'
    OP_ADDPLAYER = 'ADDPLAYER'
    OP_MOVE = 'MOVE_PLAYER'
    OP_UPDATEPLAYER = 'UPDATEPLAYER'
    OP_EQUITPLAYER = 'QUITPLAYER'
    OP_SHOOTPLAYER = 'SHOOTPLAYER'
    OP_KILLPLAYER = 'KILLPLAYER'

    def __init__(self, controller, net):
        super().__init__()
        from client.controller.controllerPartida import ControllerPartida
        self.net:Network = net
        self.__controller: ControllerPartida = controller
        self.__login = False
        self.__send = False

    def run(self) -> None:
        self.newConect()
        while self.__login:
            self.handleGetObject(self.__controller.get_naveLocal().get_Id(), self.net.recv())

    def newConect(self):
        data = self.net.connect()
        self.handleGetObject(45, data)

    def sendObject(self, obj):
        return self.net.send(json.dumps(obj))

    def handleGetObject(self, idPlayer, data:str):
        data_json = []
        if data != '':
            if data.find('/end') > 0:
                d = data.split('/end')
                for m in d:
                    if m != '':
                        j = json.loads(m)
                        for k in j:
                            data_json.append(k)
        if(type(data_json) == list):
            for op in data_json:
                if(op['OP']['type'] == self.OP_ADDPLAYER):
                    self.handlePlayeradd(op)
                elif(op['OP']['type'] == self.OP_SHOOTPLAYER):
                    self.handleShootPlayer(op)
                elif(op['OP']['type'] == self.OP_UPDATEPLAYER):
                    player_id = op['OP']['id']
                    player_pos = op['OP']['pos']
                    player_gr = op['OP']['gr']
                    player_vida = op['OP']['vida']
                    self.getPlayer(str(player_id)).changePos((player_pos[0], player_pos[1]))
                    self.getPlayer(str(player_id)).set_vida(player_vida)
                    self.getPlayer(str(player_id)).set_gr(player_gr)
                elif (op['OP']['type'] == self.OP_LOGIN):
                    player_id = str(op['OP']['id'])
                    player_color = op['OP']['color']
                    player_pos = (op['OP']['pos'][0], op['OP']['pos'][1])
                    player_vida = op['OP']['vida']
                    player = self.__controller.get_naveLocal()
                    player.set_Id(player_id)
                    player.changePos(player_pos)
                    player.set_color(player_color)
                    player.set_vida(player_vida)
                    self.__login = True

                elif (op['OP']['type'] == self.OP_KILLPLAYER):
                    player = self.getPlayer(str(op['OP']['id']))
                    player.set_vida(0)
                elif (op['OP']['type'] == self.OP_EQUITPLAYER):
                    p = self.__controller.get_naves().pop(str(op['OP']['id']))

    def handlePlayeradd(self, data):
        id = data['OP']['id']
        color = data['OP']['color']
        pos = data['OP']['pos']
        gr = data['OP']['gr']
        vida = data['OP']['vida']
        player = Ship()
        player.set_Id(str(id))
        player.set_color(color)
        player.changePos((pos[0], pos[1]))
        player.set_gr(gr)
        player.set_vida(vida)
        self.__controller.get_naves()[str(id)] = player

    def handleShootPlayer(self, data):
        id = data['OP']['id']
        pos = data['OP']['pos']
        gr = data['OP']['gr']
        player = self.__controller.get_naves()[str(id)]
        self.__controller.get_valas().append(Vala(pos, gr, player))

    def getPlayer(self, id_player) -> Ship:
        if(self.__controller.get_naveLocal().get_Id() == id_player):
            return self.__controller.get_naveLocal()
        return self.__controller.get_naves()[id_player]

    def isLogin(self):
        return self.__login

    def quit(self):
        self.net.disconnect()
        self.__login = False