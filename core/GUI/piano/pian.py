import random
from core.GUI.gui_pieces import GUIPiece, GUITypes
from core.GUI.piano.piano_keys import PianoKey
from core.configurations import TOTAL_TIME, SOUNDS_COUNT, TIME_FOR_SHOW_ANSWER


class Piano(GUIPiece):

    """
       Class used to represent a Piano.

       @master : GUIPiece
           the parent of the class

       @rlx : double
           the relx of this class

       @rly : double
           the rely of this class

       @rlwidth : double
           the relwidth of this class

       @relheight : double
           the relheight of this class

       @current_octave : int, optional
           the starting octave of the piano

       @octaves : int, optional
            the number of octaves a piano should have. Range [1, 8]

       @parent : bool, optional
            if True, adapts the relative sizes according to master's relative sizes

       Methods
       -------
        switch_key_visibility(check)
            shows/hides the names of each piano key

        set_game_over(method)
            sets the method used when a game is finished

        get_piano()
            returns the GUIPiece that represents the piano

        practice_mode(count, start_method, one_octave_only)
            starts practice mode

        test_mode(count, start_method,one_octave_only)
            starts test mode

        one_octave_up()
            increases the octave of the piano

        one_octave_down()
            decreases the octave of the piano

        trigger()
            triggers the method that shows the answer in test mode

        disable_keyboard()
            disables the piano keys of the piano

        enable_keyboard()
            enables the piano keys of the piano

        disable_sound()
            disables the sound of the piano keys

        set_current_octave(current_octave)
            sets the current octave of the piano
       """
    def __init__(self, master, rlx, rly, rlwidth, rlheight, current_octave = 1, octaves = 3, parent = False, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, GUITypes.FRAME, parent = parent, **kw)
        assert current_octave > 0 and current_octave < 9
        assert octaves > 0 and octaves < 9
        self.keys = []
        self.total_octaves = octaves
        self.current_octave = current_octave
        self.__initiate_keys()



    """
        Switches the visibility of the name of the piano keys

        Parameters
        ----------
        check : bool
    """
    def switch_key_names_visibility(self, check):
        if check:
            for key in self.keys: key.show_key_name()
        else:
            for key in self.keys: key.hide_key_name()

    """
        Sets the method used when a game ends

        Parameters
        ----------
        method : method
    """
    def set_game_over(self, method):
        self.game_over = method

    """
        Returns the gui of the piano
    """
    def get_piano(self):
        return self.gui

    """
        Starts practice mode. A sound is played and after 5 seconds, the key corresponding to the sound is highlighted in red

        Parameters
        ----------
        count : int
            number of sounds per session
        start_method: method
            method used when starting the game. It is used to disable the buttons of the top menu
        one_octave_only: bool
            if True, only sounds from the octave self.current_octave will be played
    """
    def practice_mode(self, count, start_method, one_octave_only = False):
        self.__start_practice(count, self.__get_limits(one_octave_only, start_method))

    """
        Starts test mode. A sound is played. When a player presses a piano key, the answer is shown on the piano

        Parameters
        ----------
        count : int
            number of sounds per session
        start_method: method
            method used when starting the game. It is used to disable the buttons of the top menu
        one_octave_only: bool
            if True, only sounds from the octave self.current_octave will be played
    """
    def test_mode(self, count, start_method, one_octave_only = False):
        self.__start_test(count, self.__get_limits(one_octave_only, start_method))

    """
        Increases the octave of the piano
    """
    def one_octave_up(self):
        if self.current_octave <= 8 - self.total_octaves:
            for key in self.keys: key.one_octave_up()
        self.current_octave = min(self.current_octave + 1, 8)

    """
        Decreases the octave of the piano
    """
    def one_octave_down(self):
        if self.current_octave <= 9 - self.total_octaves:
            for key in self.keys: key.one_octave_down()
        self.current_octave = max(0, self.current_octave -1)

    """
        Triggers the method for showing the answer in test mode.
    """
    def trigger(self):
        self.gui.after(0, self.__trigger_show_answer)

    """
        Enables the piano's keyboard
    """
    def enable_keyboard(self):
        for key in self.keys: key.enable()

    """
        Disables the piano's keyboard
    """
    def disable_keyboard(self):
        for key in self.keys: key.disable()

    """
        Disables the piano keys' playing method
    """
    def disable_sound(self):
        for k in self.keys: k.disable_sound()

    """
        Sets the current octave
    """
    def set_current_octave(self, octave):
        if octave > self.current_octave:
            self.__set_current_octave(lambda: self.one_octave_up(), octave - self.current_octave)
        else:
            self.__set_current_octave(lambda: self.one_octave_down(), self.current_octave - octave)

    def __set_current_octave(self, method, count):
        for x in range(count): method()

    def __random_key(self, limits):
        return self.keys[random.randint(limits[0], limits[1] - 1)]

    def __start_practice(self, count, limits):
        for x in range(0, count):
            self.__random_key(limits).play_and_show_answer(x)
        self.gui.after(count * TOTAL_TIME, self.__game_over)

    def __game_over(self):
        self.game_over()

    def __trigger_show_answer(self):
        self.answers[self.count].change_color_to_red()
        self.gui.after(0, self.__next_trigger)

    def __get_limits(self, one_octave_only: bool, start_method):
        start_method()
        start = 0
        difference = len(self.keys)
        if one_octave_only:
            difference = 12
            if self.current_octave > 9 - self.total_octaves:
                start = self.current_octave % self.total_octaves * difference

        return start, start + difference

    def __next_trigger(self):
        self.count += 1
        if self.count < len(self.answers):
            self.gui.after(TIME_FOR_SHOW_ANSWER, self.__next_test)
        else:
            self.gui.after(TIME_FOR_SHOW_ANSWER,self.__game_over)

    def __start_test(self, count, limits):
        self.answers = []
        self.count = 0
        for key in self.keys:
            key.activate_test_mode()
        for x in range(0, count):
            self.answers.append(self.__random_key(limits))
        self.__next_test()

    def __next_test(self):
        self.answers[self.count].play_random()

    def __initiate_keys(self):
        white_width = 1/(self.total_octaves * 7)
        id = random.randint(0, SOUNDS_COUNT - 1)

        if 9 - self.total_octaves < self.current_octave:
            starting = 9 - self.total_octaves
        else:
            starting = self.current_octave

        whites = self.__initiate_key(starting_octave = starting, octaves=self.total_octaves, keys=["C", "D", "E", "F", "G", "A", "B"], color="White", positions=[0, 1, 2, 3, 4, 5, 6], width = white_width, relxwidth = white_width, start_step = 0, relh = 1, id = id)
        black_width = white_width * 0.7
        blacks = self.__initiate_key(starting_octave = starting, octaves=self.total_octaves, keys=["Cb", "Db", "Fb", "Gb", "Ab"], color="Black", positions=[1, 2, 4, 5, 6], width = black_width, relxwidth = white_width, start_step= white_width * 0.35, relh = 0.6, id = id)

        for i in range(self.total_octaves):
            self.keys.append(self.__pop_first(whites))
            self.keys.append(self.__pop_first(blacks))
            self.keys.append(self.__pop_first(whites))

            self.keys.append(self.__pop_first(blacks))
            self.keys.append(self.__pop_first(whites))
            self.keys.append(self.__pop_first(whites))

            self.keys.append(self.__pop_first(blacks))
            self.keys.append(self.__pop_first(whites))
            self.keys.append(self.__pop_first(blacks))

            self.keys.append(self.__pop_first(whites))
            self.keys.append(self.__pop_first(blacks))
            self.keys.append(self.__pop_first(whites))

    def __pop_first(self, list):
        x = list[0]
        list.remove(x)
        return x

    def __initiate_key(self, starting_octave, octaves, keys, color, positions, width, relxwidth, start_step, relh, id):
        res = []
        for o in range(octaves):
            octave = o * 7
            for index in range(len(positions)):
                relx = relxwidth * (octave + positions[index]) - start_step
                key = PianoKey(self, keys[index], starting_octave + o, color, rlx = relx, rly = 0, rlwidth = width, rlheight = relh, id = id)
                res.append(key)

        return res



