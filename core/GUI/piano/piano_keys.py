import random
from datetime import datetime
import pyaudio
import soundfile
from pygame import mixer
from core.GUI.gui_pieces import GUIButton, GUILabel
from core.configurations import TIME_TO_GUESS, TIME_FOR_SHOW_ANSWER, SOUNDS_COUNT
from definitions import ROOT_DIR

TOTAL_WAITING = TIME_TO_GUESS + TIME_FOR_SHOW_ANSWER

class PianoKey(GUIButton):

    """
        Class used to represent a piano key.

           @master : GUIPiece
                the parent of the class
           @note : str
                the note of this key
           @octave : int
                the octave of this key
           @rlx : double
                the relx of this class
           @rly : double
                the rely of this class
           @rlwidth : double
                the relwidth of this class
           @relheight : double
                the relheight of this class
           @id : int
                 the id of the sound to be played
           @parent : bool, optional
                 if True, adapts the relative sizes according to master's relative sizes

        Methods
        -------
        activate_test_mode()
            Activates test mode

        get_path()
            Returns the path of the sounds played by this key

        one_octave_up()
            Increases the octave of this key

        one_octave_down()
            Decreases the octave of this key

        get_key()
            Returns the gui piece of this key

        get_color()
            Returns the color of this key

        play_and_show_answer(times)
            Plays this key's sound and after times ms, triggers the method used to show the answer in practice mode

        change_color_to_red()
            Changes the color of this key to red, then to wait after 2 seconds

        play()
            play the sound associated with self.id

        play_random()
            play a sound with a random id

        show_key_name()
            shows the name of the note

        hide_key_name()
            hides the name of the note

        disable_sound()
            disables the sound of this class

        enable_sound()
            enables the sound of this class
    """
    def __init__(self, master, note, octave, color, rlx, rly, rlwidth, rlheight, id, parent = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, parent = parent, background= color, command = lambda: self.play(), **kw)
        self.note = note
        self.color = color
        self.id = id
        self.octave = octave
        self.sounds = 'sounds'
        self.__set_key_name()
        mixer.init()

    def activate_test_mode(self):
        self.gui.config(command=lambda: self.__trigger_show_answer())

    def get_path(self):
        return f'{ROOT_DIR}/sounds/'

    def one_octave_up(self):
        self.__change_octave(self.octave+1)

    def one_octave_down(self):
        self.__change_octave(self.octave-1)

    def get_name(self):
        return f"{self.note}{self.octave}"

    def get_key(self):
        return self.gui

    def get_color(self):
        return self.color

    def log(self, message):
        print(f"{message}: {datetime.now()}")

    def play_and_show_answer(self, times: int):
        s = TOTAL_WAITING * times
        self.gui.after(s, self.__play_and_change_color_to_red)

    def change_color_to_red(self):
        self.log("Changing color to red")
        self.master.disable_keyboard()
        self.gui.config(bg ='red')
        self.gui.after(TIME_FOR_SHOW_ANSWER - 500, self.__change_color_to_default)

    def play(self):
        self.__play(self.id)

    def play_random(self):
        if self.id != None:
            self.__play(random.randint(0, SOUNDS_COUNT-1))

    def show_key_name(self):
        self.key_name.place()

    def hide_key_name(self):
        self.key_name.forget()

    def disable_sound(self):
        self.id = None

    def enable_sound(self):
        self.sound_on = True

    def __lt__(self, other):
        return self.get_name() < other.get_name()

    def __gt__(self, other):
        return self.get_name() > other.get_name()

    def __play(self, id):
        path = f"{ROOT_DIR}\\sounds\\{self.note} id {id} octave_{self.octave}.mp3"
        self.log(f"playing note {self.note}{self.octave} id-{id} ")
        mixer.music.load(path)
        mixer.music.play()

    def __trigger_show_answer(self):
        self.master.trigger()

    def __play_and_change_color_to_red(self):
        self.play_random()
        self.gui.after(TIME_TO_GUESS, self.change_color_to_red)

    def __change_color_to_default(self):
        self.log("Changing color to default")
        self.gui.config(bg = self.color)
        self.master.enable_keyboard()

    def __change_color(self, color):
        self.gui.config(bg = color)

    def __set_key_name(self):
        rely = 0.92
        width = .6
        relx = (1-width)/2
        self.key_name = GUILabel(self, rlx= relx, rly= rely, rlwidth= width, rlheight=1 - rely - 0.01, text=f"{self.get_name()}", initiate = False)
        self.key_name.gui.config(font='Helvetica 9 bold', foreground='red', background = self.color)

    def __change_octave(self, octave):
        self.octave = octave
        self.key_name.gui.config(text = f'{self.get_name()}')
