import tkinter
import time
from TeaServer.TeaScript import attendees
from TeaServer.TeaScript import game_states


class GameRunnerGui:
    def __init__(self):
        self.root = tkinter.Tk()

        self.index_of_current_state = 0

        columnWidth = 475
        columnHeight = 750

        # ----------------------- column 0 - wand status lines-------------------------------------
        self.column0 = tkinter.Frame(self.root, relief=tkinter.SUNKEN, borderwidth=25, height=columnHeight, width=columnWidth)
        self.column0.grid_propagate(0)
        self.column0.grid(row=0, column=0)

        # row 0
        self.wandLabel = tkinter.Label(self.column0, text="Wand Status", borderwidth=2, relief="groove", width=60)
        self.wandLabel.grid(row=0, column=0, columnspan=4)

        # remaining rows
        self.wandGuiLines = []
        for index, attendee in enumerate(attendees):
            newWand = GadgetStatus(gadget_name=attendee, gadget_suffix="'s Wand", index=(index + 1), root=self.column0,
                                   time_of_last_heartbeat=time.time())
            self.wandGuiLines.append(newWand)

        # ----------------------- column 1 - empty column -------------------------------------
        self.root.grid_columnconfigure(1, minsize=30)

        # ----------------------- column 2 - Other gadgets, current state description -------------------------------------
        self.column2 = tkinter.Frame(self.root, relief=tkinter.SUNKEN, borderwidth=25, height=columnHeight, width=columnWidth)
        self.column2.grid_propagate(0)
        self.column2.grid(row=0, column=2)

        # rows 0 & 1: smoker status line
        self.smokerLabel = tkinter.Label(self.column2, text="Smoker Status", borderwidth=2, relief="groove",
                                         width=60)
        self.smokerLabel.grid(row=0, column=0, columnspan=4)
        self.smokerStatus = GadgetStatus(gadget_name="Smoker", gadget_suffix="", index=1, root=self.column2,
                                         time_of_last_heartbeat=time.time())

        # row 2: empty
        self.column2.grid_rowconfigure(2, minsize=15)

        # rows 3 & 4: Regina in the Fireplace line
        self.ReginaFireplaceLabel = tkinter.Label(self.column2, text="Regina in Fireplace Status",
                                                  borderwidth=2, relief="groove", width=60)
        self.ReginaFireplaceLabel.grid(row=3, column=0, columnspan=4)
        self.ReginaFireplaceStatus = GadgetStatus(gadget_name="Regina Fireplace", gadget_suffix="", index=4, root=self.column2,
                                                  time_of_last_heartbeat=time.time())

        # row 5: empty
        self.column2.grid_rowconfigure(5, minsize=15)

        # rows 6 & 7: Speakers line
        self.SpeakersLabel = tkinter.Label(self.column2, text="Speaker Status",
                                           borderwidth=2, relief="groove", width=60)
        self.SpeakersLabel.grid(row=7, column=0, columnspan=4)
        self.SpeakerStatus = GadgetStatus(gadget_name="Speakers", gadget_suffix="", index=8, root=self.column2,
                                          time_of_last_heartbeat=time.time())

        # rows 8,9: empty
        self.column2.grid_rowconfigure(8, minsize=45)
        self.column2.grid_rowconfigure(9, minsize=45)


        # rows 10 & 11: Current State Description
        self.CurrentStateLabel = tkinter.Label(self.column2, text="Current State Description",
                                               borderwidth=2, relief="groove", width=60)
        self.CurrentStateLabel.grid(row=10, column=0, columnspan=4)

        self.CurrentStateDescription = tkinter.Text(self.column2, height=12, width=50)

        self.CurrentStateDescription.insert(tkinter.END, """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""")

        self.CurrentStateDescription.grid(row=11, column=0, columnspan=4)

        # row 12: empty
        self.column2.grid_rowconfigure(12, minsize=45)

        # rows 13 & 14: Next State Description
        self.NextStateLabel = tkinter.Label(self.column2, text="Next State Description",
                                               borderwidth=2, relief="groove", width=60)
        self.NextStateLabel.grid(row=13, column=0, columnspan=4)

        self.NextStateDescription = tkinter.Text(self.column2, height=12, width=50)

        self.NextStateDescription.insert(tkinter.END, """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum""")

        self.NextStateDescription.grid(row=14, column=0, columnspan=4)

        # ----------------------- column 3 -------------------------------------
        # empty column
        self.root.grid_columnconfigure(3, minsize=30)

        # ----------------------- column 4 - game status and control -------------------------------------
        self.column4 = tkinter.Frame(self.root, relief=tkinter.SUNKEN, borderwidth=25, height=columnHeight, width=columnWidth)
        self.column4.grid_propagate(0)
        self.column4.grid(row=0, column=4)

        self.gameStatusLabel = tkinter.Label(self.column4, text="Game Status", borderwidth=2, relief="groove", width=60)
        self.gameStatusLabel.grid(row=0, column=0, columnspan=3)

        self.gameStatusLines = []
        for index, statusEntry in enumerate(game_states):
            name_of_state = statusEntry[0]
            newGameState = GameState(state_name=name_of_state, index=(index + 1), root=self.column4, status=GameState.GAME_STATE_PENDING)
            self.gameStatusLines.append(newGameState)

        self.column4.grid_rowconfigure(len(self.gameStatusLines) + 2, minsize=60)

        self.backButton = tkinter.Button(self.column4, bd=2, command=self.back_button, text="Go Back", anchor="nw")
        self.backButton.grid(row=len(self.gameStatusLines) + 3, column=0)

        self.startStopButton = tkinter.Button(self.column4, bd=2, command=self.go_stop_button, text="Go!!!", anchor="nw")
        self.startStopButton.grid(row=len(self.gameStatusLines) + 3, column=1)
        self.goButtonEnabled = True

        self.forwardButton = tkinter.Button(self.column4, bd=2, command=self.forward_button, text="Go Forward", anchor="nw")
        self.forwardButton.grid(row=len(self.gameStatusLines) + 3, column=2)

        self.update_current_state(index_of_new_state=0)

    def service(self):
        for wandGuiLine in self.wandGuiLines:
            wandGuiLine.update_time_box()
            wandGuiLine.update_row_color()

        self.smokerStatus.update_row_color()
        self.smokerStatus.update_time_box()

        self.ReginaFireplaceStatus.update_row_color()
        self.ReginaFireplaceStatus.update_time_box()

        self.SpeakerStatus.update_row_color()
        self.SpeakerStatus.update_time_box()

        self.root.update()

    def back_button(self):
        self.update_current_state(index_of_new_state=self.index_of_current_state - 1)

    def go_stop_button(self):
        if self.goButtonEnabled:
            self.startStopButton.config(text="Pause...")
            self.goButtonEnabled = False

            self.backButton.config(state="disabled")
            self.forwardButton.config(state="disabled")

        else:
            self.startStopButton.config(text="Go!!!")
            self.goButtonEnabled = True

            self.backButton.config(state="normal")
            self.forwardButton.config(state="normal")

    def forward_button(self):
        self.update_current_state(index_of_new_state=self.index_of_current_state + 1)

    def update_current_state(self, index_of_new_state):
        if index_of_new_state < 0:
            self.index_of_current_state = 0
        elif index_of_new_state >= len(game_states):
            self.index_of_current_state = len(game_states) - 1
        else:
            self.index_of_current_state = index_of_new_state

        for i, gameStatusLine in enumerate(self.gameStatusLines):
            if i < self.index_of_current_state:
                gameStatusLine.update_status(new_status=GameState.GAME_STATE_PENDING)
            elif i == self.index_of_current_state:
                gameStatusLine.update_status(new_status=GameState.GAME_STATE_ACTIVE)
            else:
                gameStatusLine.update_status(new_status=GameState.GAME_STATE_DONE)

        self.CurrentStateDescription.delete('1.0', tkinter.END)
        self.NextStateDescription.delete('1.0', tkinter.END)

        self.CurrentStateDescription.insert(tkinter.END, game_states[self.index_of_current_state][1])
        if (self.index_of_current_state + 1) < len(game_states):
            self.NextStateDescription.insert(tkinter.END, game_states[self.index_of_current_state + 1][1])
        else:
            self.NextStateDescription.insert(tkinter.END, "")

    def get_index_of_current_state(self):
        return self.index_of_current_state

    def update_wand_status(self, message_id, wand_id, wand_state, wand_ip):
        if wand_id not in attendees:
            print("got unidentified wand heartbeat {}, {}, {}".format(message_id, wand_id, wand_state))
            return

        for wandGuiLine in self.wandGuiLines:
            if wandGuiLine.gadget_name == wand_id:
                wandGuiLine.heartbeat_received()
                wandGuiLine.update_row_status(new_status=wand_state)
                wandGuiLine.update_ip_address(wand_ip)
                break



class GameState:
    GAME_STATE_DONE = "DONE"
    GAME_STATE_ACTIVE = "ACTIVE"
    GAME_STATE_PENDING = "PENDING"

    def __init__(self, state_name, index, root, status):
        self.state_name = state_name
        self.index = index
        self.root = root
        self.status = status

        self.state_name_text = tkinter.Label(root, text=state_name, borderwidth=2, relief="groove", width=58,
                                            anchor="nw")
        self.state_name_text.grid(row=self.index, column=0, columnspan=3)

        self.format_row_based_on_status()

    def update_status(self, new_status):
        self.status = new_status
        self.format_row_based_on_status()

    def format_row_based_on_status(self):

        if self.status == self.GAME_STATE_DONE:
            self.state_name_text.config({"background": "#96EAFF", "foreground": "#20ABDA"})

        elif self.status == self.GAME_STATE_ACTIVE:
            self.state_name_text.config({"background": "#00FF0A"})

        else:
            self.state_name_text.config({"background": "#FFFFA0"})


class GadgetStatus:
    def __init__(self, gadget_name, gadget_suffix, index, root, time_of_last_heartbeat):
        self.gadget_name = gadget_name
        self.gadget_suffix = gadget_suffix
        self.index = index
        self.root = root
        self.gadget_ip = "Unknown"
        self.time_of_last_heartbeat = time_of_last_heartbeat

        self.gadget_name_text = tkinter.Label(root, text=(gadget_name + gadget_suffix), borderwidth=2, relief="groove", width=15, anchor="nw")
        self.gadget_name_text.grid(row=self.index, column=0)

        self.gadget_ip_text = tkinter.Label(root, text=self.gadget_ip, relief="groove", width=15, anchor="nw")
        self.gadget_ip_text.grid(row=self.index, column=1)

        self.gadget_status_text = tkinter.Label(root, text="uninitialized", borderwidth=2, relief="groove", width=11, anchor="nw")
        self.gadget_status_text.grid(row=self.index, column=2)

        self.gadget_last_heard_from_text = tkinter.Label(root, text=round(time_of_last_heartbeat, 0), borderwidth=2, relief="groove", width=15, anchor="nw")
        self.gadget_last_heard_from_text.grid(row=self.index, column=3)

        self.update_row_color()

    def heartbeat_received(self):
        self.time_of_last_heartbeat = time.time()

    def update_row_color(self):
        time_since_last_heartbeat = time.time() - self.time_of_last_heartbeat

        if time_since_last_heartbeat < 2:
            newColor = "green"
        elif time_since_last_heartbeat < 10:
            newColor = "yellow"
        else:
            newColor = "red"

        self.gadget_name_text.config({"background": newColor})
        self.gadget_ip_text.config({"background": newColor})
        self.gadget_status_text.config({"background": newColor})
        self.gadget_last_heard_from_text.config({"background": newColor})

    def update_row_status(self, new_status):
        self.gadget_status_text.config({"text": new_status})

    def update_ip_address(self, ip_addr):
        self.gadget_ip = ip_addr
        self.gadget_ip_text.config({"text": self.gadget_ip})

    def update_time_box(self):
        time_since_last_heartbeat = time.time() - self.time_of_last_heartbeat
        self.gadget_last_heard_from_text.config({"text": round(time_since_last_heartbeat, 0)})


if __name__ == "__main__":
    game = GameRunnerGui()




