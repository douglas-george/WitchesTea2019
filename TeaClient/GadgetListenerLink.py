import socket
from GadgetMessage import GadgetMessage


class GadgetListenerLink:
    """
    The job of the GadgetListenerLink is to listen on a port for broadcasts from the Announcer.
    """

    ANNOUNCEMENT_BCAST_ADDR = "255.255.255.255"
    ANNOUNCEMENT_PORT = 10102

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ANNOUNCEMENT_BCAST_ADDR, self.ANNOUNCEMENT_PORT))

        self.message_being_received = GadgetMessage()

    def service_gadget_listener(self):
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
    server = GadgetListenerLink()

    while True:
        newMessage = server.service_gadget_listener()

        if newMessage is not None:
            print(newMessage.encode())


