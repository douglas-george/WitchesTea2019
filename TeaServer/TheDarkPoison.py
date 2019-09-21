import tkinter
from TeaServer.TeaScript import attendees
from TeaServer.TeaScript import game_states
from TeaServer.GameRunnerGui import GameRunnerGui
from TeaServer.TeaAnnouncer import TeaAnnouncer
from TeaServer.ServerListenerLink import SmokerListener, WandListener


class TheDarkPoison:
    def __init__(self):
        self.gui = GameRunnerGui()
        self.announcer = TeaAnnouncer(time_between_heartbeats=1, current_game_state=game_states[0][0])
        self.smoker_listener = SmokerListener()
        self.wand_listener = WandListener()

    def run(self):
        while True:
            try:
                self.gui.service()
                state_index = self.gui.get_index_of_current_state()
            except tkinter.TclError:
                break

            self.announcer.update_state(new_game_state=game_states[state_index][0])
            self.announcer.service()

            smoker_data = self.smoker_listener.service_smoker()
            if smoker_data is not None:
                smoker_heartbeat_id, smoker_state = smoker_data
                self.gui.smokerStatus.heartbeat_received()

            wand_data = self.wand_listener.service_wands()
            if wand_data is not None:
                message_id, wand_id, wand_state = wand_data
                self.gui.update_wand_status(message_id, wand_id, wand_state)






if __name__ == "__main__":
    tea = TheDarkPoison()

    tea.run()