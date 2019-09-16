
from TeaServer.ServerLink import ServerLink

class SmokerServer():
    SERVER_PORT = 10101

    def __init__(self):
        self.link = ServerLink(hostPort=self.SERVER_PORT)