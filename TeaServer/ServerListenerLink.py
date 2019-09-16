import socket
from GadgetMessage import GadgetMessage


class ServerListenerLink:
    """
    The job of the ServerListenerLink is to listen on a port for incoming data from a gadget.
    """
    def __init__(self, hostIP, hostPort):
        self.hostIP = hostIP
        self.hostPort = hostPort

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.hostIP, self.hostPort))

        self.message_being_received = GadgetMessage()

    def service_server(self):
        return_data = self.socket.recv(1024).decode("utf-8")

        if len(return_data) > 0:
            new_message_available, trailing_data = self.message_being_received.decode(new_data=return_data)

            if new_message_available:
                newMessage = self.message_being_received
                self.message_being_received = GadgetMessage()
                self.message_being_received.decode(new_data=trailing_data)

                return newMessage

        return None


if __name__ == "__main__":
    server = ServerListenerLink(hostIP="192.168.5.177", hostPort=10101)

    while True:
        newMessage = server.service_server()

        if newMessage is not None:
            print(newMessage.encode())


