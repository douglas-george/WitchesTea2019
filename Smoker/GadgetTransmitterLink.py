import socket
import time
from GadgetMessage import GadgetHeartbeat


class GadgetTransmitterLink:
    """
    The GadgetTransmitterLink's job is to transmit a gadget's messages to a ServerListenerLink
    """

    GADGET_BCAST_ADDR = "192.168.5.255"

    def __init__(self, gadget_port, heartbeat_rate, client_id):
        self.gadget_port = gadget_port
        self.heartbeatRate = heartbeat_rate
        self.clientId = client_id

        self.timeOfLastHeartbeat = time.time()
        self.heartbeatId = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_heartbeat_if_needed(self, current_state):
        currentTime = time.time()
        if currentTime > (self.timeOfLastHeartbeat + self.heartbeatRate):
            heartbeat = GadgetHeartbeat(gadget_id=self.clientId, heartbeat_id=self.heartbeatId, gadget_state=current_state)

            self.socket.sendto(bytearray(heartbeat.encode(), 'utf-8'), (self.GADGET_BCAST_ADDR, self.gadget_port))

            self.timeOfLastHeartbeat = currentTime
            self.heartbeatId += 1

    def service(self, current_state):
        self.send_heartbeat_if_needed(current_state)


if __name__ == "__main__":
    client = GadgetTransmitterLink(host_address="192.168.5.177", host_port=10101, heartbeat_rate=5.0, client_id="Smoker")

    while True:
        client.service()



