from core.GUI.gui_configurations import THREE_BUTTONS_COLOR, THREE_BUTTONS_FONT, THREE_BUTTONS_TEXT_COLOR, create_args
from core.GUI.gui_pieces import GUILabel, LabelWithCheckboxAndNumbersInput, GUIButton
from core.configurations import SOUNDS_COUNT_MAXIMUM, SOUNDS_COUNT_MINIMUM
from core.default_settings import SHOW_KEYS, ONE_OCTAVE_ONLY, SOUNDS_PER_SESSION, STARTING_OCTAVE


class ThreeButtonsLabel(GUILabel):
    """
            Class used to represent the a label with three buttons. Contains:
            save_settings : button used to save the current settings as default settings
            practice : button used to start the practice mode
            test : button used to start the test mode

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
            @check_flag : bool
                the default state of the check button
            @parent : bool, optional
                if True, adapts the relative sizes according to master's relative sizes

            Methods
            -------

            change_piano(piano):
                changes the piano of this class

            disable_buttons():
                disables the buttons of this class

            enable_buttons():
                enables the buttons of this class

    """

    def __init__(self, master, piano, starting_octave_panel, sounds_per_session_panel, rlx, rly, rlwidth, rlheight, parent = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, parent, background = master.get_background_color() ,**kw)
        self.change_piano(piano)
        self.__initiate(starting_octave_panel, sounds_per_session_panel)

    def change_piano(self, piano):
        self.piano = piano
        self.piano.set_game_over(self.__stop_game)

    def disable_buttons(self):
        self.practice.disable()
        self.save_settings.disable()
        self.test.disable()

    def enable_buttons(self):
        self.practice.enable()
        self.save_settings.enable()
        self.test.enable()

    def __initiate(self, starting_octave_panel, sounds_per_session_panel):
        width = 0.33
        space = 0.005
        args = create_args(['background', 'font', 'foreground'], [THREE_BUTTONS_COLOR, THREE_BUTTONS_FONT, THREE_BUTTONS_TEXT_COLOR])
        self.stop = GUIButton(self, 0, 0, width, 1, text="STOP\nGAME",
                         command=lambda: self.__stop_game(), initiate= False, **args)
        self.save_settings = GUIButton(self, 0, 0, width, 1, text = "SAVE\nSETTINGS", command = lambda: self.__save_settings(), **args)
        self.practice = GUIButton(self, width + space, 0, width, 1, text = "PRACTICE",
                                  command= lambda :self.__practice_mode(sounds_per_session_panel.get_sounds_per_session(),
                                                                        starting_octave_panel.get_one_octave_only()), **args)
        self.test = GUIButton(self, (width + space) * 2, 0, width, 1, text = "TEST",
                              command= lambda :self.__test_mode(sounds_per_session_panel.get_sounds_per_session(), starting_octave_panel.get_one_octave_only()), **args)

    def __save_settings(self):
        self.master.save_settings()

    def __stop_game(self):
        self.master.change_piano()
        self.master.enable_buttons()
        self.stop.forget()
        self.save_settings.place()

    def __practice_mode(self, count, one_octave_only):
        self.__prepare_for_game()
        self.piano.practice_mode(count, self.master.disable_buttons, one_octave_only)

    def __prepare_for_game(self):
        self.save_settings.forget()
        self.stop.place()

    def __disable_buttons(self):
        self.practice.disable()
        self.test.disable()

    def __test_mode(self, count, one_octave_only):
        self.__prepare_for_game()
        self.piano.test_mode(count, self.master.disable_buttons, one_octave_only)

class StartingOctavePanel(LabelWithCheckboxAndNumbersInput):
    """
            Class used to represent the Starting octave panel.

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
            @check_flag : bool
                the default state of the check button
            @parent : bool, optional
                if True, adapts the relative sizes according to master's relative sizes

            Methods
            -------

            change_piano(piano):
                configures the up button and the down button to call the new piano when the buttons are pressed

            get_one_octave_only():
                :returns: the checkbutton state of this class

    """

    def __init__(self, master, piano, rlx, rly, rlwidth, rlheight, check_flag = ONE_OCTAVE_ONLY, parent = True, initiate = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, check_flag = check_flag, label_text='Starting octave:',
                         checkbox_text="One octave only", parent = parent, current_value = STARTING_OCTAVE, initiate = initiate, min_method = lambda: piano.one_octave_down(),
                         max_method=lambda: piano.one_octave_up(), **kw)
        if piano.current_octave != self.get_value():
            piano.set_current_octave(self.get_value())

    def change_piano(self, piano):
        self.set_max_method(lambda: piano.one_octave_up())
        self.set_max_method(lambda: piano.one_octave_down())

    def get_one_octave_only(self):
        return self.is_checked()


class SoundsPerSessionPanel(LabelWithCheckboxAndNumbersInput):
    """
            Class used to represent the Sounds per session panel.

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
            @check_flag : bool
                the default state of the check button
            @parent : bool, optional
                if True, adapts the relative sizes according to master's relative sizes

            Methods
            -------

            change_piano(piano):
                sets the check button command to call the given piano, and ensures that the new piano has the key
                visibility according to the value of the check button of this class

            get_sounds_per_session():
                :returns: the value of the input_with_buttons label. Represents the length of one game session

            get_show_keys():
                :returns: the checkbutton state of this class

    """
    def __init__(self, master, piano, rlx, rly, rlwidth, rlheight, check_flag = SHOW_KEYS, parent = True, initiate = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, label_text ="Sounds per session:",
                         check_flag = check_flag, checkbox_text="Show keys", parent = parent, min_value=SOUNDS_COUNT_MINIMUM,
                         max_value=SOUNDS_COUNT_MAXIMUM, current_value = SOUNDS_PER_SESSION, initiate = initiate, **kw)
        self.change_piano(piano)

    def change_piano(self, piano):
        piano.switch_key_names_visibility(self.is_checked())
        self.checkbox_with_label.check_button.configure(command = lambda: piano.switch_key_names_visibility(self.is_checked()))

    def get_sounds_per_session(self):
        return self.input_with_buttons.get_value()

    def get_show_keys(self):
        return self.is_checked()