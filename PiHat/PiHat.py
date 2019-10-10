import time
from GadgetListenerLink import GadgetListenerLink
from GadgetTransmitterLink import GadgetTransmitterLink


class PiHat:
    def __init__(self, port):
        self.port = port
        self.listener_link = GadgetListenerLink()
        self.transmitter_link = GadgetTransmitterLink(gadget_port=self.port,
                                                      heartbeat_rate=1.0,
                                                      client_id="Table")
        self.processed_message_ids = set()
        self.current_game_state = None
        self.state_change_to_be_serviced = False

        self.time_of_last_game_update = time.time()
        self.time_of_last_heartbeat_warning = time.time()

        self.current_gadget_state = "UNKNOWN"

    def check_for_heartbeat(self):
        msg = self.listener_link.service_gadget_listener()
        if msg is None:
            pass
        elif msg.data["MESSAGE_TYPE"] == "GAME_HEARTBEAT":
            self.time_of_last_game_update = time.time()

            if msg.data["MESSAGE_ID"] not in self.processed_message_ids:
                self.processed_message_ids.add(msg.data["MESSAGE_ID"])

                if msg.data["GAME_STATE"] != self.current_game_state:
                    self.current_game_state = msg.data["GAME_STATE"]
                    self.state_change_to_be_serviced = True

        time_since_last_heartbeat = time.time() - self.time_of_last_game_update
        if time_since_last_heartbeat > 5.0:
            time_since_last_heartbeat_warning = time.time() - self.time_of_last_heartbeat_warning
            if time_since_last_heartbeat_warning > 5.0:
                print("Warning!! It has been {} seconds since I last heard a heartbeat!".format(round(time_since_last_heartbeat, 1)))
                self.time_of_last_heartbeat_warning = time.time()

    def run(self):
        while True:
            self.transmitter_link.service(current_state=self.current_gadget_state)
            self.check_for_heartbeat()
            self.service_current_state()
