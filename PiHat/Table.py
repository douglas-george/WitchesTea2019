from PiHat import PiHat


class Table(PiHat):
    TABLE_PORT = 10108

    def __init__(self):
        super().__init__(port=self.TABLE_PORT)

    def service_current_state(self):
        if self.state_change_to_be_serviced:
            print("Servicing new game state: {}".format(self.current_game_state))
            self.state_change_to_be_serviced = False


if __name__ == "__main__":
    table = Table()

    table.run()
