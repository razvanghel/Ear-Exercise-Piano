from core.GUI.gui_configurations import TOP_MENU_BACKGROUND
from core.GUI.gui_pieces import GUIPiece, GUITypes
from core.GUI.piano.pian import Piano
from core.GUI.top_menu.top_menu_pieces import StartingOctavePanel, SoundsPerSessionPanel, ThreeButtonsLabel
from core.configurations import PIANO_RELX, PIANO_RELY, PIANO_RELWIDTH, PIANO_RELHEIGHT
from definitions import ROOT_DIR

SPACING = 0.01
RELY = 0.05
HEIGHT = 1 - 2 * RELY

class TopMenu(GUIPiece):
    """
           Class used to represent the Top Menu's GUI. Contains three objects:
           starting_octave_panel : panel used to set the octave of the piano.
           sounds_per_session_panel : panel used to set the length of the game
           three_buttons_panel : panel used for saving settings and starting the game

           @master : tkinter
               the parent of the class
           @rlx : double
               the relx of this class
           @rly : double
               the rely of this class
           @rlwidth : double
               the relwidth of this class
           @relheight : double
               the relheight of this class
           @parent : bool, optional
                if True, adapts the relative sizes according to master's relative sizes

        Methods
        -------

        get_sounds_per_session()
            :return the length of the game

        get_starting_octave()
            :return the octave of the piano

        disable_buttons()
            disables the buttons that are inside the children of this class

        enable_buttons()
            enables the buttons that are inside the children of this class

        change_piano()
            creates a new piano that will replace the current piano on the GUI

        save_settings()
            saves the game's current settings inside default_settings.py
"""
    def __init__(self, master, rlx, rly, rlwidth, rlheight, parent = False, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, GUITypes.LABEL, parent, background = TOP_MENU_BACKGROUND, **kw)
        self.piano = Piano(master, rlx=PIANO_RELX, rly=PIANO_RELY, rlwidth=PIANO_RELWIDTH, rlheight=PIANO_RELHEIGHT)
        self.__initiate()

    def get_sounds_per_session(self):
        return self.sounds.input_with_buttons.get_value()

    def get_starting_octave(self):
        self.starting_octave.input_with_buttons.get_gui().cget("text")

    def disable_buttons(self):
        self.starting_octave.disable_buttons()
        self.sounds.disable_buttons()
        self.three_buttons.disable_buttons()

    def enable_buttons(self):
        self.starting_octave.enable_buttons()
        self.sounds.enable_buttons()
        self.three_buttons.enable_buttons()

    def change_piano(self):
        self.piano.disable_sound()
        self.piano.gui.destroy()
        piano = Piano(self.master, rlx=PIANO_RELX, rly=PIANO_RELY, rlwidth=PIANO_RELWIDTH, rlheight=PIANO_RELHEIGHT,
                      background="White", current_octave = self.starting_octave.get_value())
        self.starting_octave.change_piano(piano)
        self.sounds.change_piano(piano)
        self.three_buttons.change_piano(piano)

    def save_settings(self):
        vars = ['STARTING_OCTAVE', 'SOUNDS_PER_SESSION', 'ONE_OCTAVE_ONLY', 'SHOW_KEYS']
        vals = [self.starting_octave.input_with_buttons.get_value(), self.sounds.input_with_buttons.get_value(), self.starting_octave.is_checked(), self.sounds.is_checked()]
        lines = [f"{vars[i]} = {vals[i]}\n" for i in range(len(vars))]
        DEFAULT_SETTINGS = f'{ROOT_DIR}/core/default_settings.py'
        with open(DEFAULT_SETTINGS, 'w') as f:
            f.writelines(lines)
            f.close()

    def __initiate(self):
        width_per_widget = (1 - 2 * PIANO_RELX - 2*SPACING)/3

        self.starting_octave = StartingOctavePanel(self, self.piano, PIANO_RELX, RELY, width_per_widget, HEIGHT)

        new_relx = PIANO_RELX + width_per_widget + SPACING
        self.__place_sounds_per_session(new_relx, width_per_widget)

        new_relx += width_per_widget + SPACING
        self.__place_buttons(new_relx, width_per_widget)

    def __place_sounds_per_session(self, relx, width):
        self.sounds = SoundsPerSessionPanel(self, piano = self.piano, rlx= relx, rly= RELY, rlwidth= width, rlheight= HEIGHT, parent = self, background='Grey')

    def __place_buttons(self, relx, width):
        self.three_buttons = ThreeButtonsLabel(self, self.piano, self.starting_octave, self.sounds, rlx= relx, rly= RELY, rlwidth= width, rlheight= HEIGHT)
