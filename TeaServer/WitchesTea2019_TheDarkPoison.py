import tkinter
from TeaServer.SmokerServer import SmokerServer

attendees = ["Dennis", "Delta",
             "Bill", "Kali", "Jaron", "Ammon", "Devor",
             "Marika", "Alexis", "Amber", "Isaac",
             "Jessica", "Doug", "Gabriel",
             "Joe", "Barbara", "Carl",
             "Alice", "Jeff", "Braeden", "Carter", "Tanner", "Coleman", "Brynlee",
             "Sam", "Erin", "Sariah", "Emma", "Hyrum",
             "Courtney", "Hannah", "Luke"]


class TheDarkPoison:
    game_states = ("WAITING_TO_START",
                   "AT_ATTENTION",
                   "SMOKING",
                   "REGINA'S WARNING",
                   "WANDS AT THE READY")


    def __init__(self):
        self.root = tkinter.Tk()

        # ----------------------- column 0 -------------------------------------
        # wand status lines
        self.wandFrame = tkinter.Frame(self.root)
        self.wandFrame.grid(row=0, column=0)

        self.wandLabel = tkinter.Label(self.wandFrame, text="Wand Status", borderwidth=2, relief="groove", width=48)
        self.wandLabel.grid(row=0, column=0, columnspan=3)

        self.wandGuiLines = []
        for index, attendee in enumerate(attendees):
            newWand = GadgetStatus(gadget_name=attendee + "'s Wand" , index=(index + 1), root=self.wandFrame,
                                   time_since_last_heartbeat=100.0)
            self.wandGuiLines.append(newWand)

        # empty row
        self.root.grid_rowconfigure(1, minsize=15)

        # smoker status line
        self.smokerFrame = tkinter.Frame(self.root)
        self.smokerFrame.grid(row=2, column=0)
        self.smokerLabel = tkinter.Label(self.smokerFrame, text="Smoker Status", borderwidth=2, relief="groove",
                                         width=48)
        self.smokerLabel.grid(row=0, column=0, columnspan=3)
        self.smokerStatus = GadgetStatus(gadget_name="Smoker", index=1, root=self.smokerFrame,
                                         time_since_last_heartbeat=100.0)

        # empty row
        self.root.grid_rowconfigure(3, minsize=15)

        # Regina in the Fireplace line
        self.ReginaFireplaceFrame = tkinter.Frame(self.root)
        self.ReginaFireplaceFrame.grid(row=4, column=0)
        self.ReginaFireplaceLabel = tkinter.Label(self.ReginaFireplaceFrame, text="Regina in Fireplace Status",
                                                  borderwidth=2, relief="groove", width=48)
        self.ReginaFireplaceLabel.grid(row=0, column=0, columnspan=3)
        self.ReginaFireplaceStatus = GadgetStatus(gadget_name="Regina", index=1, root=self.ReginaFireplaceFrame,
                                                  time_since_last_heartbeat=100.0)

        # empty row
        self.root.grid_rowconfigure(5, minsize=15)

        # Speakers line
        self.SpeakersFrame = tkinter.Frame(self.root)
        self.SpeakersFrame.grid(row=6, column=0)
        self.SpeakersLabel = tkinter.Label(self.SpeakersFrame, text="Speaker Status",
                                           borderwidth=2, relief="groove", width=48)
        self.SpeakersLabel.grid(row=0, column=0, columnspan=3)
        self.SpeakerStatus = GadgetStatus(gadget_name="Speakers", index=1, root=self.SpeakersFrame,
                                          time_since_last_heartbeat=100.0)

        # ----------------------- column 1 -------------------------------------
        self.root.grid_columnconfigure(1, minsize=30)

        # ----------------------- column 2 -------------------------------------
        self.gameStatusFrame = tkinter.Frame(self.root)
        self.gameStatusFrame.grid(row=0, column=2)

        self.gameStatusLabel = tkinter.Label(self.gameStatusFrame, text="Game Status", borderwidth=2, relief="groove", width=80)
        self.gameStatusLabel.grid(row=0, column=0, columnspan=3)

        self.gameStatusLines = {}
        for index, statusEntry in enumerate(self.game_states):
            newGameState = GameState(state_name=statusEntry, index=(index + 1), root=self.gameStatusFrame)
            self.gameStatusLines[statusEntry] = newGameState


        self.root.mainloop()


class GameState:
    def __init__(self, state_name, index, root):
        self.state_name = state_name
        self.index = index
        self.root = root

        self.state_name_text = tkinter.Label(root, text=state_name, borderwidth=2, relief="groove", width=45,
                                            anchor="nw")
        self.state_name_text.grid(row=self.index, column=0)


class GadgetStatus:
    def __init__(self, gadget_name, index, root, time_since_last_heartbeat):
        self.gadget_name = gadget_name
        self.index = index
        self.root = root
        self.time_since_last_heartbeat = time_since_last_heartbeat

        self.wand_name_text = tkinter.Label(root, text=gadget_name, borderwidth=2, relief="groove", width=15, anchor="nw")
        self.wand_name_text.grid(row=self.index, column=0)

        self.wand_status_text = tkinter.Label(root, text="uninitialized", borderwidth=2, relief="groove", width=15, anchor="nw")
        self.wand_status_text.grid(row=self.index, column=1)

        self.wand_time_text = tkinter.Label(root, text=round(time_since_last_heartbeat, 0), borderwidth=2, relief="groove", width=15, anchor="nw")
        self.wand_time_text.grid(row=self.index, column=2)

        self.update_row_color()

    def update_heartbeat(self, time_since_last_heartbeat):
        self.time_since_last_heartbeat = time_since_last_heartbeat
        self.wand_time_text.config({"text": round(time_since_last_heartbeat, 0)})
        self.update_row_color()

    def update_row_color(self):
        if self.time_since_last_heartbeat < 2:
            newColor = "green"
        elif self.time_since_last_heartbeat < 10:
            newColor = "yellow"
        else:
            newColor = "red"

        self.wand_name_text.config({"background": newColor})
        self.wand_status_text.config({"background": newColor})
        self.wand_time_text.config({"background": newColor})

    def update_row_status(self, new_status):
        self.wand_status_text.config({"text": new_status})




if __name__ == "__main__":
    game = TheDarkPoison()




