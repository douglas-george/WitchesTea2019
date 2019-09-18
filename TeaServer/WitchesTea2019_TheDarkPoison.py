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

        columnWidth = 400
        columnHeight = 750


        # ----------------------- column 0 - wand status lines-------------------------------------
        self.column0 = tkinter.Frame(self.root, relief=tkinter.SUNKEN, borderwidth=25, height=columnHeight, width=columnWidth)
        self.column0.grid_propagate(0)
        self.column0.grid(row=0, column=0)

        # row 0
        self.wandLabel = tkinter.Label(self.column0, text="Wand Status", borderwidth=2, relief="groove", width=48)
        self.wandLabel.grid(row=0, column=0, columnspan=3)

        # remaining rows
        self.wandGuiLines = []
        for index, attendee in enumerate(attendees):
            newWand = GadgetStatus(gadget_name=attendee + "'s Wand" , index=(index + 1), root=self.column0,
                                   time_since_last_heartbeat=100.0)
            self.wandGuiLines.append(newWand)

        # ----------------------- column 1 - empty column -------------------------------------
        self.root.grid_columnconfigure(1, minsize=30)

        # ----------------------- column 2 - Other gadgets -------------------------------------
        self.column2 = tkinter.Frame(self.root, relief=tkinter.SUNKEN, borderwidth=25, height=columnHeight, width=columnWidth)
        self.column2.grid_propagate(0)
        self.column2.grid(row=0, column=2)

        # rows 0 & 1: smoker status line
        self.smokerLabel = tkinter.Label(self.column2, text="Smoker Status", borderwidth=2, relief="groove",
                                         width=48)
        self.smokerLabel.grid(row=0, column=0, columnspan=3)
        self.smokerStatus = GadgetStatus(gadget_name="Smoker", index=1, root=self.column2,
                                         time_since_last_heartbeat=100.0)

        # row 2: empty
        self.column2.grid_rowconfigure(2, minsize=15)

        # rows 3 & 4: Regina in the Fireplace line
        self.ReginaFireplaceLabel = tkinter.Label(self.column2, text="Regina in Fireplace Status",
                                                  borderwidth=2, relief="groove", width=48)
        self.ReginaFireplaceLabel.grid(row=3, column=0, columnspan=3)
        self.ReginaFireplaceStatus = GadgetStatus(gadget_name="Regina", index=4, root=self.column2,
                                                  time_since_last_heartbeat=100.0)

        # row 5: empty
        self.column2.grid_rowconfigure(5, minsize=15)

        # rows 6 & 7: Speakers line
        self.SpeakersLabel = tkinter.Label(self.column2, text="Speaker Status",
                                           borderwidth=2, relief="groove", width=48)
        self.SpeakersLabel.grid(row=7, column=0, columnspan=3)
        self.SpeakerStatus = GadgetStatus(gadget_name="Speakers", index=8, root=self.column2,
                                          time_since_last_heartbeat=100.0)

        # ----------------------- column 3 -------------------------------------
        # empty column
        self.root.grid_columnconfigure(3, minsize=30)

        # ----------------------- column 4 - game status -------------------------------------
        self.column4 = tkinter.Frame(self.root, relief=tkinter.SUNKEN, borderwidth=25, height=columnHeight, width=columnWidth)
        self.column4.grid_propagate(0)
        self.column4.grid(row=0, column=4)

        self.gameStatusLabel = tkinter.Label(self.column4, text="Game Status", borderwidth=2, relief="groove", width=80)
        self.gameStatusLabel.grid(row=0, column=0, columnspan=3)

        self.gameStatusLines = {}
        for index, statusEntry in enumerate(self.game_states):
            newGameState = GameState(state_name=statusEntry, index=(index + 1), root=self.column4)
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




