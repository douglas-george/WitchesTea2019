import socket
from GadgetMessage import GadgetMessage


class GadgetListenerLink:
    """
    The job of the GadgetListenerLink is to listen on a port for broadcasts from the Announcer.
    """

    ANNOUNCEMENT_BCAST_ADDR = "192.168.5.255"
    ANNOUNCEMENT_PORT = 10103

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(0)
        self.socket.bind(('', self.ANNOUNCEMENT_PORT))

        self.message_being_received = GadgetMessage()

    def service_gadget_listener(self):
        try:
            return_data = self.socket.recv(1024).decode("utf-8")
        except BlockingIOError:
            return_data = ""

        if len(return_data) > 0:
            new_message_available, trailing_data = self.message_being_received.decode(new_data=return_data)
            print (new_message_available)


            if new_message_available:
                newMessage = self.message_being_received
                self.message_being_received = GadgetMessage()
                self.message_being_received.decode(new_data=trailing_data)

                return newMessage

        return None


if __name__ == "__main__":
    server = GadgetListenerLink()

    while True:
        newMessage = server.service_gadget_listener()

        if newMessage is not None:
            print(newMessage.encode())


