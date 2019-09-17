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
    def __init__(self):
        self.root = tkinter.Tk()

        self.wandFrame = tkinter.Frame(self.root)
        self.wandFrame.grid(row=0, column=0)

        self.wandLabel = tkinter.Label(self.wandFrame, text="Wand Status", borderwidth=2, relief="groove", width=48)
        self.wandLabel.grid(row=0, column=0, columnspan=3)

        self.wandGuiLines = []
        for index, attendee in enumerate(attendees):
            newWand = Wand(attendee=attendee, index=(index + 1), root=self.wandFrame, time_since_last_heartbeat=100.0)

        self.root.mainloop()


class Wand:
    def __init__(self, attendee, index, root, time_since_last_heartbeat):
        self.attendee = attendee
        self.index = index
        self.root = root
        self.time_since_last_heartbeat = time_since_last_heartbeat

        self.wand_name_text = tkinter.Label(root, text=attendee, borderwidth=2, relief="groove", width=15, anchor="nw")
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




