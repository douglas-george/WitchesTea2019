import socket
import time
from GadgetMessage import GadgetHeartbeat

class ClientLink():
    def __init__(self, hostAddress, hostPort, heartbeatRate, clientId):
        self.hostAddress = hostAddress
        self.hostPort = hostPort
        self.heartbeatRate = heartbeatRate
        self.clientId = clientId

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
    client = ClientLink(hostAddress="192.168.5.177", hostPort=10101, heartbeatRate=5.0, clientId="Smoker")

    while True:
        client.service_client()



