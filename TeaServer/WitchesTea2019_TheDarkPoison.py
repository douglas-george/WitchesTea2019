from TeaServer.SmokerServer import SmokerServer


class TheDarkPoison():
    def __init__(self):
        pass

    def start(self):
        print('Starting "The Dark Poison"')

        print("Creating Servers...")
        print("\tCreating Smoker Server")
        self.SmokerServer = SmokerServer()




if __name__ == "__main__":
    game = TheDarkPoison()

    game.start()




