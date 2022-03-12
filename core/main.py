import tkinter

from core.GUI.gui_configurations import ROOT_BACKGROUND
from core.GUI.top_menu.top_menu import TopMenu
from core.configurations import TOPMENU_RELHEIGHT

class MainMenu(tkinter.Tk):

    def __init__(self):
        super(MainMenu, self).__init__()
        self.wm_title("Tkinter window")
        self.geometry("1400x700")
        self.configure(background = ROOT_BACKGROUND)
        menu = TopMenu(self, parent = False, rlx=0, rly=0, rlwidth=1, rlheight=TOPMENU_RELHEIGHT)
        menu.place()

if __name__ == "__main__":

    root = MainMenu()
    root.mainloop()
