from PiHat import PiHat


class Fireplace(PiHat):
    FIREPLACE_PORT = 10110

    def __init__(self):
        super().__init__(port=self.FIREPLACE_PORT)

    def service_current_state(self):
        if self.state_change_to_be_serviced:
            print("Servicing new game state: {}".format(self.current_game_state))
            self.state_change_to_be_serviced = False


if __name__ == "__main__":
    fireplace = Fireplace()

    fireplace.run()
