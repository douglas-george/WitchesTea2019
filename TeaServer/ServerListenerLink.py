import socket
from GadgetMessage import GadgetMessage


class ServerListenerLink:
    """
    The job of the ServerListenerLink is to listen on a port for incoming data from a gadget.
    """

    GADGET_BCAST_ADDR = "192.168.5.255"

    def __init__(self, gadget_port):
        self.gadget_port = gadget_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(0)
        self.socket.bind(('', self.gadget_port))

        self.message_being_received = GadgetMessage()

    def service_server(self):
        while True:
            try:
                #return_data = self.socket.recv(1024).decode("utf-8")
                return_data, sender_info = self.socket.recvfrom(1024)
                sender_ip, sender_port = sender_info
                return_data = return_data.decode("utf-8")

            except BlockingIOError:
                break

            except UnicodeDecodeError:
                print("Unicode Decode Error from {}".format(sender_ip))
                break

            if len(return_data) > 0:
                new_message_available, trailing_data = self.message_being_received.decode(new_data=return_data)

                if new_message_available:
                    newMessage = self.message_being_received
                    self.message_being_received = GadgetMessage()
                    self.message_being_received.decode(new_data=trailing_data)

                    return newMessage, sender_ip

        return None


class TableListener(ServerListenerLink):
    TABLE_PORT = 10108

    def __init__(self):
        super().__init__(gadget_port=self.TABLE_PORT)

    def service_table(self):
        result = self.service_server()

        if result is not None:
            msg, ip_addr = result
            if (msg.data["MESSAGE_TYPE"] == "GADGET_HEARTBEAT") and (msg.data["GADGET_ID"] == "Table"):
                return (msg.data["MESSAGE_ID"].strip(), msg.data["GADGET_STATE"].strip(), ip_addr)

        return None


class FireplaceListener(ServerListenerLink):
    FIREPLACE_PORT = 10110

    def __init__(self):
        super().__init__(gadget_port=self.FIREPLACE_PORT)

    def service_fireplace(self):
        result = self.service_server()

        if result is not None:
            msg, ip_addr = result
            if (msg.data["MESSAGE_TYPE"] == "GADGET_HEARTBEAT") and (msg.data["GADGET_ID"] == "Fireplace"):
                return (msg.data["MESSAGE_ID"].strip(), msg.data["GADGET_STATE"].strip(), ip_addr)

        return None


class WandListener(ServerListenerLink):
    WAND_PORT = 10109

    def __init__(self):
        super().__init__(gadget_port=self.WAND_PORT)

    def service_wands(self):
        results = self.service_server()

        if results is not None:
            msg, sender_ip = results
            if (msg.data["MESSAGE_TYPE"] == "GADGET_HEARTBEAT"):
                return (msg.data["MESSAGE_ID"].strip(),
                        msg.data["GADGET_ID"].strip(),
                        msg.data["GADGET_STATE"].strip(),
                        msg.data["COMPILE_DATE"].strip(),
                        msg.data["COMPILE_TIME"].strip(),
                        sender_ip)

        return None


class ClickerListener(ServerListenerLink):
    CLICKER_PORT = 10111

    def __init__(self):
        super().__init__(gadget_port=self.CLICKER_PORT)

    def service_clicker(self):
        results = self.service_server()

        if results is not None:
            msg, sender_ip = results
            if (msg.data["MESSAGE_TYPE"] == "GADGET_HEARTBEAT"):
                return (msg.data["MESSAGE_ID"].strip(),
                        msg.data["GADGET_ID"].strip(),
                        msg.data["GADGET_STATE"].strip(),
                        msg.data["COMPILE_DATE"].strip(),
                        msg.data["COMPILE_TIME"].strip(),
                        sender_ip)

        return None


if __name__ == "__main__":
    server = ServerListenerLink(hostIP="192.168.5.177", hostPort=10101)

    while True:
        newMessage = server.service_server()

        if newMessage is not None:
            print(newMessage.encode())


