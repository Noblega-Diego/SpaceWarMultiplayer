import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"  # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = 15555
        self.addr = (self.host, self.port)

    def connect(self):
        res = ''
        try:
            self.client.connect(self.addr)
            while True:
                print('esperando')
                res = self.client.recv(2048).decode('utf-8')
                if res != '':
                    break
        except:
            res = ''
        return res


    def recv(self) -> str:
        return self.client.recv(2048).decode('utf-8')

    def sendRes(self, data) -> str:
        """
        :param data: str
        :return: str
        """
        try:
            self.client.sendall(str.encode('{}/end'.format(data)))
            res = self.recv()
            return res
        except socket.error as e:
            return ''

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.sendall(str.encode('{}/end'.format(data)))
        except socket.error as e:
            self.client.close()

    def disconnect(self):
        self.client.close()