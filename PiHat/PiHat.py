import time
from GadgetListenerLink import GadgetListenerLink
from GadgetTransmitterLink import GadgetTransmitterLink
import RPi.GPIO as GPIO
import serial


class PiHat:
    relayPinMapping = {8: 2,
                       7: 3,
                       6: 4,
                       5: 5,
                       4: 6,
                       3: 7,
                       2: 8,
                       1: 9}

    BLINK_STATE_UNINITIALIZED = 0
    BLINK_STATE_WARM_TWINKLE = 1
    BLINK_STATE_RED_SNAKE = 2
    BLINK_STATE_RED_SNAKE_DONE = 3
    BLINK_STATE_RED_FIRE = 4
    BLINK_STATE_GREEN_FIRE = 5
    BLINK_STATE_OFF = 6
    BLINK_STATE_LOW_RED_FIRE = 7

    def __init__(self, port, client_id):
        self.port = port
        self.listener_link = GadgetListenerLink()
        self.transmitter_link = GadgetTransmitterLink(gadget_port=self.port,
                                                      heartbeat_rate=1.0,
                                                      client_id=client_id)
        self.processed_message_ids = set()
        self.current_game_state = None
        self.state_change_to_be_serviced = False

        self.time_of_last_game_update = time.time()
        self.time_of_last_heartbeat_warning = time.time()

        self.current_gadget_state = "I dunno"

        GPIO.setmode(GPIO.BCM)

        for relayIndex in self.relayPinMapping:
            GPIO.setup(self.relayPinMapping[relayIndex], GPIO.OUT)
            self.SetRelay(relayIndex, False)

        self.com = serial.Serial(port='/dev/serial0', baudrate=115200)

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
                print("Warning!! It has been {} seconds since I last heard a heartbeat!".format(
                    round(time_since_last_heartbeat, 1)))
                self.time_of_last_heartbeat_warning = time.time()

    def get_piHat_state(self):
        self.com.write("?".encode())
        response = self.com.read(self.com.inWaiting())
        if len(response) > 0:
            return int(response[-1])
        else:
            return None

    def set_piHat_state(self, new_state):
        for i in range(10):
            self.com.write(chr(new_state).encode())
            time.sleep(1.0)
            read_state = self.get_piHat_state()

            if read_state == new_state:
                break
            else:
                print("state change error: '{}' != '{}'".format(new_state, read_state))

    def SetRelay(self, relayIndex, on):
        if on:
            GPIO.output(self.relayPinMapping[relayIndex], GPIO.LOW)
        else:
            GPIO.output(self.relayPinMapping[relayIndex], GPIO.HIGH)

    def run(self):
        while True:
            self.transmitter_link.service(current_state=self.current_gadget_state)
            self.check_for_heartbeat()
            self.service_current_state()
