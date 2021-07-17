import random
import socket
import threading
import json
from typing import Dict, Tuple

class Player():
    def __init__(self):
        self.__pos = None
        self.__id = None
        self.__color = None
        self.__gr = None

    def changePos(self, pos:Tuple[int,int]):
        self.__pos = pos

    def set_Id(self, id:str):
        self.__id = id

    def get_pos(self):
        return self.__pos

    def get_id(self):
        return self.__id

    def set_color(self,color):
        self.__color = color

    def get_color(self):
        return self.__color

    def set_gr(self, gr):
        self.__gr = gr

    def get_gr(self):
        return self.__gr


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addres = ('localhost', 15555)

sock.bind(server_addres) #le damos el puerto y la direccion ip


user_type = Tuple[socket.socket,Player]

list_sockets:Dict[int,user_type] = {}
list_conexionesProcess = []

def atenderCliente(conexion, id):
    color = (random.randint(10,240),random.randint(10,240),random.randint(10,240))
    list_sockets[id][1].set_Id(id)
    list_sockets[id][1].set_color(color)
    list_sockets[id][1].changePos((0,0))
    list_sockets[id][1].set_gr(0)
    mess_login = [{'OP':{
        'type':'LOGIN',
        'id': list_sockets[id][1].get_id(),
        'color':list_sockets[id][1].get_color(),
        'pos':list_sockets[id][1].get_pos(),
        'gr':list_sockets[id][1].get_gr()
    }}]
    for id_user, user in list_sockets.items():
        if(id_user != id):
            op_sendUser = {'OP': {
                'type': 'ADDPLAYER',
                'id': id,
                'color': list_sockets[id][1].get_color(),
                'pos': list_sockets[id][1].get_pos(),
                'gr': list_sockets[id][1].get_gr()
            }}
            user[0].sendall('{}/end'.format(json.dumps([op_sendUser])).encode('utf-8')) # enviamos el nuevo jugador a los demas usuarios
            op_newUser = {'OP': {
                'type': 'ADDPLAYER',
                'id': id_user,
                'color': user[1].get_color(),
                'pos': user[1].get_pos(),
                'gr': user[1].get_gr()
            }}
            mess_login.append(op_newUser)
    conexion.sendall('{}/end'.format(json.dumps(mess_login)).encode('utf-8'))
    try:
        while True:
            data:str = conexion.recv(2048).decode('utf-8')
            json_data = []
            res = []
            if data.find('/end') >= 1:
                dall = data.split('/end')
                for j in dall:
                    if j != '':
                        print('{}>{}'.format(id,j))
                        l = json.loads(j)
                        for g in l:
                            json_data.append(g)
                for d in json_data:
                    if(d['OP']['type'] == 'MOVE_PLAYER'):
                        pos = d['OP']['pos']
                        gr = d['OP']['gr']
                        list_sockets[id][1].changePos((pos[0],pos[1]))
                        list_sockets[id][1].set_gr(gr)
                        res = [{'OP':{
                            'type': 'UPDATEPLAYER',
                            'id': id,
                            'pos': list_sockets[id][1].get_pos(),
                            'gr': list_sockets[id][1].get_gr()
                        }}]
                        for id_user, user in list_sockets.items():
                            if(id_user != id):
                                user[0].sendall('{}/end'.format(json.dumps(res)).encode('utf-8'))
                    elif (d['OP']['type'] == 'SHOOT'):
                        pos = d['OP']['pos']
                        gr = d['OP']['gr']
                        list_sockets[id][1].changePos((pos[0], pos[1]))
                        list_sockets[id][1].set_gr(gr)
                        r = [{'OP': {
                            'type': 'SHOOTPLAYER',
                            'id': id,
                            'pos': list_sockets[id][1].get_pos(),
                            'gr': list_sockets[id][1].get_gr()
                        }}]
                        for id_user, user in list_sockets.items():
                            if (id_user != id):
                                user[0].sendall('{}/end'.format(json.dumps(r)).encode('utf-8'))
                    elif (d['OP']['type'] == 'KILL'):
                        r = [{'OP': {
                            'type': 'KILLPLAYER',
                            'id': id,
                        }}]
                        for id_user, user in list_sockets.items():
                            if (id_user != id):
                                user[0].sendall('{}/end'.format(json.dumps(r)).encode('utf-8'))
            conexion.sendall('{}/end'.format(json.dumps(res)).encode('utf-8'))
    except:
        print('mensaje no enviado')
    finally:
        print('conexion finalizada: {}'.format(id))
        conexion.close()
        it = list_sockets.pop(id)

        res = [{'OP': {
            'type': 'QUITPLAYER',
            'id': id
        }}]
        for id_user, user in list_sockets.items():
            if (id_user != id):
                user[0].sendall('{}/end'.format(json.dumps(res)).encode('utf-8'))





sock.listen(1) #En espera a una conexion
increment = 10000
while True:
    print('Esperando conexion')
    try:
        conexion, client_adress = sock.accept()
        print('conectado con :', client_adress)
        id = increment
        connect = threading.Thread(target=atenderCliente, args=[conexion, id])
        list_sockets[id] = (conexion, Player())
        list_conexionesProcess.append(connect)
        increment += 1
        connect.start()
    except:
        sock.close()
        break

