import time
import socket
from GadgetMessage import GameHeartbeat


class TeaAnnouncer:
    """
    The TeaAnnouncer's job is to periodically broadcast the current game status.
    """
    ANNOUNCEMENT_BCAST_ADDR = "192.168.5.255"
    ANNOUNCEMENT_PORT = 10103

    def __init__(self, time_between_heartbeats, current_game_state):
        self.time_of_last_heartbeat = time.time()
        self.time_between_heartbeats = time_between_heartbeats
        self.current_game_state = current_game_state
        self.current_message_id = 0
        self.current_message_count = 0
        self.gadget_id = "ANNOUNCER"

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def update_state(self, new_game_state):
        if new_game_state != self.current_game_state:
            self.current_game_state = new_game_state
            self.current_message_id += 1
            self.current_message_count = 0

    def service(self):
        current_time = time.time()
        if current_time > (self.time_of_last_heartbeat + self.time_between_heartbeats):
            # send heartbeat
            print('game beat')
            heartbeat = GameHeartbeat(gadget_id=self.gadget_id,
                                      message_id=self.current_message_id,
                                      message_count=self.current_message_count,
                                      gameState=self.current_game_state)

            self.socket.sendto(bytearray(heartbeat.encode(), 'utf-8'), (self.ANNOUNCEMENT_BCAST_ADDR,
                                                                        self.ANNOUNCEMENT_PORT))

            self.current_message_count += 1
            self.time_of_last_heartbeat = current_time
