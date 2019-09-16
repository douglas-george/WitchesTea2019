import socket
import time
from GadgetMessage import GadgetHeartbeat


class GadgetTransmitterLink:
    """
    The GadgetTransmitterLink's job is to transmit a gadget's messages to a ServerListenerLink
    """
    def __init__(self, host_address, host_port, heartbeat_rate, client_id):
        self.hostAddress = host_address
        self.hostPort = host_port
        self.heartbeatRate = heartbeat_rate
        self.clientId = client_id

        self.timeOfLastHeartbeat = time.time()
        self.heartbeatId = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_heartbeat_if_needed(self):
        currentTime = time.time()
        if currentTime > (self.timeOfLastHeartbeat + self.heartbeatRate):
            heartbeat = GadgetHeartbeat(gadget_id=self.clientId, heartbeat_id=self.heartbeatId)

            self.socket.sendto(bytearray(heartbeat.encode(), 'utf-8'), (self.hostAddress, self.hostPort))

            self.timeOfLastHeartbeat = currentTime
            self.heartbeatId += 1

    def service_client(self):
        self.send_heartbeat_if_needed()


if __name__ == "__main__":
    client = GadgetTransmitterLink(host_address="192.168.5.177", host_port=10101, heartbeat_rate=5.0, client_id="Smoker")

    while True:
        client.service_client()



