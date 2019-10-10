import time
import RPi.GPIO as gpio
from GadgetListenerLink import GadgetListenerLink
from GadgetTransmitterLink import GadgetTransmitterLink


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

        self.relayBoard = RelayBoard()

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

    def test_relays(self):
        for relayId in [RelayBoard.RELAY_1_GPIO, RelayBoard.RELAY_2_GPIO, RelayBoard.RELAY_3_GPIO, RelayBoard.RELAY_4_GPIO, RelayBoard.RELAY_5_GPIO, RelayBoard.RELAY_6_GPIO, RelayBoard.RELAY_7_GPIO, RelayBoard.RELAY_8_GPIO]:
            print(relayId)
            self.relayBoard.turn_relay_on(relayId)
            time.sleep(1)
            self.relayBoard.turn_relay_off(relayId)
            time.sleep(1)

        self.relayBoard.cleanup()


class RelayBoard:
    RELAY_1_GPIO = 4
    RELAY_2_GPIO = 17
    RELAY_3_GPIO = 22
    RELAY_4_GPIO = 10
    RELAY_5_GPIO = 9
    RELAY_6_GPIO = 11
    RELAY_7_GPIO = 5
    RELAY_8_GPIO = 6


    def __init__(self):
        gpio.setmode(gpio.BCM)

        gpio.setup(self.RELAY_1_GPIO, gpio.OUT)
        self.turn_relay_off(self.RELAY_1_GPIO)

        gpio.setup(self.RELAY_2_GPIO, gpio.OUT)
        self.turn_relay_off(self.RELAY_2_GPIO)

        gpio.setup(self.RELAY_3_GPIO, gpio.OUT)
        self.turn_relay_off(self.RELAY_3_GPIO)

        gpio.setup(self.RELAY_4_GPIO, gpio.OUT)
        self.turn_relay_off(self.RELAY_4_GPIO)

        gpio.setup(self.RELAY_5_GPIO, gpio.OUT)
        self.turn_relay_off(self.RELAY_5_GPIO)

        gpio.setup(self.RELAY_6_GPIO, gpio.OUT)
        self.turn_relay_off(self.RELAY_6_GPIO)

        gpio.setup(self.RELAY_7_GPIO, gpio.OUT)
        self.turn_relay_off(self.RELAY_7_GPIO)

        gpio.setup(self.RELAY_8_GPIO, gpio.OUT)
        self.turn_relay_off(self.RELAY_8_GPIO)

    def turn_relay_on(self, relay_gpio):
        gpio.output(relay_gpio, gpio.LOW)

    def turn_relay_off(self, relay_gpio):
        gpio.output(relay_gpio, gpio.HIGH)

    def cleanup(self):
        gpio.cleanup()



if __name__ == "__main__":
    smoker = SmokerClient()

    #smoker.run()

    time.sleep(10)
    
    smoker.test_relays()


