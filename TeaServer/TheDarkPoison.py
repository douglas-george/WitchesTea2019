import tkinter
from TeaServer.TeaScript import attendees
from TeaServer.TeaScript import game_states
from TeaServer.GameRunnerGui import GameRunnerGui
from TeaServer.TeaAnnouncer import TeaAnnouncer
from TeaServer.ServerListenerLink import TableListener, WandListener, FireplaceListener
import time


class TheDarkPoison:
    def __init__(self):
        self.gui = GameRunnerGui()
        self.announcer = TeaAnnouncer(time_between_heartbeats=0.1, current_game_state=game_states[0][0])
        self.table_listener = TableListener()
        self.fireplace_listener = FireplaceListener()
        self.wand_listener = WandListener()

        self.warmup_time = None

    def run(self):
        while True:
            try:
                self.gui.service()
                state_index = self.gui.get_index_of_current_state()
            except tkinter.TclError:
                break

            self.announcer.update_state(new_game_state=game_states[state_index][0])
            self.announcer.service()

            table_data = self.table_listener.service_table()
            if table_data is not None:
                table_heartbeat_id, table_state, sender_ip = table_data
                self.gui.table_status.update_hw_info(ip_addr=sender_ip, compile_date=None, compile_time=None)
                self.gui.table_status.heartbeat_received()
                self.gui.table_status.update_row_status(table_state)

                if (table_state == "SNAKE_DONE"):
                    self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)

            fireplace_data = self.fireplace_listener.service_fireplace()
            if fireplace_data is not None:
                fireplace_heartbeat_id, fireplace_state, sender_ip = fireplace_data
                self.gui.ReginaFireplaceStatus.update_hw_info(ip_addr=sender_ip, compile_date=None, compile_time=None)
                self.gui.ReginaFireplaceStatus.heartbeat_received()
                self.gui.ReginaFireplaceStatus.update_row_status(fireplace_state)

            wand_data = self.wand_listener.service_wands()
            if wand_data is not None:
                message_id, wand_id, wand_state, compile_date, compile_time, sender_ip = wand_data
                self.gui.update_wand_status(message_id, wand_id, wand_state, compile_date, compile_time, sender_ip)

            if (game_states[self.gui.get_index_of_current_state()][0] == "FOGGER_WARMUP"):
                if self.warmup_time is None:
                    self.warmup_time = time.time()
                elif time.time() > (self.warmup_time + 15):
                    self.gui.update_current_state(index_of_new_state=self.gui.index_of_current_state + 1)
            else:
                self.warmup_time = None








if __name__ == "__main__":
    tea = TheDarkPoison()

    tea.run()