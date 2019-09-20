import time
from TeaClient.GadgetListenerLink import GadgetListenerLink
from TeaClient.GadgetTransmitterLink import GadgetTransmitterLink


class SmokerClient():
    WAITING_FOR_START_COMMAND = "WAITING FOR START"
    START_PUMP = "START PUMP"
    PUMPING = "PUMPING"
    TURN_OFF_PUMP = "TURN OFF PUMP"
    ALL_DONE = "ALL DONE"

    PUMP_RUN_TIME_SECONDS = 15

    SMOKER_PORT = 10108

    def __init__(self):
        self.listener_link = GadgetListenerLink()
        self.transmitter_link = GadgetTransmitterLink(gadget_port=self.SMOKER_PORT,
                                                      heartbeat_rate=1.0,
                                                      client_id="SMOKER")
        self.processed_message_ids = set()
        self.state = self.WAITING_FOR_START_COMMAND

    def run(self):
        while True:
            self.transmitter_link.service(current_state=self.state)

            if self.state == self.WAITING_FOR_START_COMMAND:
                msg = self.listener_link.service_gadget_listener()

                if msg is None:
                    continue
                elif msg.data["MESSAGE_TYPE"] == "GAME_HEARTBEAT":
                    if msg.data["MESSAGE_ID"] not in self.processed_message_ids:
                        self.processed_message_ids.add(msg.data["MESSAGE_ID"])

                        if msg.data["GAME_STATE"] == "SMOKING":
                            print("This is what I live for!!!!!!!!!!!!!!!!!!!!!")
                            self.state = self.START_PUMP
                        else:
                            print("Got a game state I don't worry about: {}".format(msg.data["GAME_STATE"]))

                    # print(msg.encode())
                else:
                    print("Got a message type I don't handle: {}".format(msg.data["MESSAGE_TYPE"]))

                time.sleep(0.25)

            elif self.state == self.START_PUMP:
                print("Starting pump.")
                # TODO, turn on pump

                self.pump_start_time = time.time()
                self.state = self.PUMPING

                print("Pumping...")

            elif self.state == self.PUMPING:
                if time.time() > (self.pump_start_time + self.PUMP_RUN_TIME_SECONDS):
                    print("...Pumping complete.")
                    self.state = self.TURN_OFF_PUMP

            elif self.state == self.TURN_OFF_PUMP:
                print("Turning off pump...")
                # TODO, turn off pump
                self.state = self.ALL_DONE
                print("...Pump is off.")

            else:
                time.sleep(.25)



if __name__ == "__main__":
    smoker = SmokerClient()

    smoker.run()


