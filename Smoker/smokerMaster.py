import socket


class SmokerMaster():
    def __init__(self):
        pass

    def ConnectToServer(self, ipAddress, port):
        self.hostAddress = ipAddress
        self.hostPort = port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.hostAddress, self.hostPort))
            s.sendall(b'Hello, world')
            data = s.recv(1024)

        print('Received', repr(data))
