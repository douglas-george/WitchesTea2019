
from TeaServer.ServerListenerLink import ServerListenerLink

class SmokerServer():
    SERVER_PORT = 10101

    def __init__(self):
        self.link = ServerListenerLink(hostPort=self.SERVER_PORT)