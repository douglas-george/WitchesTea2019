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

        self.wandGuiLines = []
        for attendee in attendees:
            newWand = Wand(attendee=attendee, root=self.root, timeSinceLastHeartbeat=1000.0)

        self.root.mainloop()


class Wand:
    def __init__(self, attendee, root, time_since_last_heartbeat):
        self.gui_line = tkinter.Text(root, height=1, width=10)
        self.gui_line.insert(tkinter.INSERT, attendee)
        self.gui_line.pack()

    def get_row_color(self, time_since_last_heartbeat):
        if time_since_last_heartbeat > 10:








if __name__ == "__main__":
    game = TheDarkPoison()




