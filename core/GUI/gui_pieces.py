import tkinter
from enum import Enum
from tkinter import Frame, Label, Checkbutton, Button
from core.GUI.gui_configurations import *

class GUITypes(Enum):
    LABEL = 0,
    FRAME = 1,
    CHECKBUTTON = 2,
    BUTTON = 3,
    TEXT = 4


class GUIPiece():
    """
            Class used to represent the a widget.

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

            @type : GUITypes
                the default state of the check button

            @parent : bool, optional
                if True, adapts the relative sizes according to master's relative sizes

            @initiate : bool, optional
                if True, calls the method place()

            Methods
            -------
            def configure(cnf = None, **kw):
                configures this widget

            def get_background_color(self):
                :returns: the background color of this widget

            def get(key):
                :returns: the value of the given key. E.g. get('background') returns this widget's background color

            def destroy(self):
                destroys this widget

            def forget(self):
                removes this widget from the screen

            def get_gui(self):
                :returns: this widget

            def set_text(self, text):
                sets the text to this widget

            def set_gui(self, gui):
                sets the widget of this class

            def place(self):
                places the widget on the screen

    """

    def __init__(self, master, rlx, rly, rlwidth, rlheight, type, parent = False, initiate = True, **kw):

        self.master = master
        self.relx = rlx
        self.rely = rly
        self.relwidth = rlwidth
        self.relheight = rlheight

        if type == GUITypes.LABEL:
            self.gui = Label()
        elif type == GUITypes.FRAME:
            self.gui = Frame()
        elif type == GUITypes.CHECKBUTTON:
            self.gui = Checkbutton()
        elif type == GUITypes.BUTTON:
            self.gui = Button()
        else:
            raise AttributeError("Please select a GUIType.")

        #adapt the relative sizes
        self.parent = parent
        if parent:
            if self.relx!=0:
                self.relx = rlx * master.relwidth + master.relx
            else:
                self.relx = master.relx

            if self.rely!=0:
                self.rely = rly * master.relheight + master.rely
            else:
                self.rely = master.rely

            self.relwidth = rlwidth * master.relwidth
            self.relheight = rlheight * master.relheight

        self.configure(**kw)

        if initiate:
            self.place()

    def configure(self, cnf = None, **kw):
        self.gui.config(cnf, **kw)

    def get_background_color(self):
        return self.get('background')

    def get(self, key: str):
        return self.gui[key]

    def destroy(self):
        self.gui.destroy()

    def forget(self):
        self.gui.place_forget()

    def get_gui(self):
        return self.gui

    def set_text(self, text):
        self.get_gui().config(text = text)

    def set_gui(self, gui):
        self.gui = gui

    def place(self):
        self.gui.place(relx = self.relx, rely = self.rely, relwidth = self.relwidth, relheight = self.relheight)


class GUILabel(GUIPiece):
    def __init__(self, master, rlx, rly, rlwidth, rlheight, parent = True, initiate = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, type = GUITypes.LABEL, parent = parent, initiate = initiate, **kw)


class LabelWithCheckboxAndNumbersInput(GUILabel):
    """
               Class used to represent the a label that contains:
               text_label : label used to show a message
               checkbox_with_label : label with a checkbox
               input_with_buttons : label that contains two buttons that increment/decrement a value

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

               @checkbox_text : str
                   the text of the checkbutton

               @check_flag : bool
                   the default state of the checkbutton

               @current_value : int
                   the default value of the input label

               @min_method : method, optional
                   the method used when down button is pressed

               @max_method : method, optional
                   the method used when up button is pressed

               @parent : bool, optional
                   if True, adapts the relative sizes according to master's relative sizes

               @initiate : bool, optional
                   if True, calls the method place()

               @min_value : int, optional
                   the minimum value that can be reached by input label

               @max_value : int, optional
                   the maximum value that can be reached by input label

               Methods
               -------
               disable_buttons()
                    disables the buttons of this class' children

               enable_buttons()
                    enables the buttons of this class' children

               set_min_method(method)
                    sets the method used to be called by the down button

               set_max_method(method)
                    sets the method used to be called by the up button

               is_checked()
                    :returns: bool the value  of the check button

               get_value()
                    :returns: the value of the input label
    """
    def __init__(self, master, rlx, rly, rlwidth, rlheight, label_text, checkbox_text, check_flag, current_value, min_method = None, max_method = None, parent = True, initiate = True, min_value = 1, max_value = 8, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, parent = parent, initiate = initiate, **kw)
        rlwidth = 0.85
        percentage = 0.75
        self.__initialise_label(label_text, rlwidth, percentage)
        self.__initialise_checkbox_with_text(rlwidth, percentage, 1 - percentage, checkbox_text, check_flag)
        self.__initialise_input(rlwidth, current_value, min_value, max_value, min_method, max_method)

    def disable_buttons(self):
        self.checkbox_with_label.disable()
        self.input_with_buttons.disable()

    def enable_buttons(self):
        self.checkbox_with_label.enable()
        self.input_with_buttons.enable()

    def set_min_method(self, method):
        self.input_with_buttons.min_method = method

    def set_max_method(self, method):
        self.input_with_buttons.max_method = method

    def is_checked(self):
        return self.checkbox_with_label.is_checked()

    def get_value(self):
        return self.input_with_buttons.get_value()

    def __initialise_label(self, text, relwidth, relheight):
        args = create_args(['background', 'font', 'foreground'], [TOP_LABEL_COLOR, TOP_LABEL_FONT, TOP_LABEL_TEXT_COLOR])
        self.text_label = GUILabel(self, 0, 0, relwidth, relheight, text = text, **args)

    def __initialise_checkbox_with_text(self, relwidth, rely, relheight, text, check_flag):
        self.checkbox_with_label = LabelWithCheckboxAndText(self, 0, rely, relwidth, relheight, check_flag = check_flag ,checkbox_text = text, background= 'grey')

    def __initialise_input(self, relx, current_value, min, max, min_method, max_method):
        self.input_with_buttons = InputWithButtons(self, relx, 0, (1-relx), 1, current_value = current_value, min_value= min ,max_value = max, min_method=min_method, max_method=max_method)


class InputWithButtons(GUILabel):
    """
               Class used to represent the a label that contains:
               button_up : button that increments self.value
               input : label that shows self.value
               button_down : button that decrements self.value

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

               @current_value : int
                   the default value of the input label

               @min_value : method
                   the minimum value that the input label can have

               @max_value : method
                   the maximum value that the input label can have

               @min_method : method, optional
                   the method used when down button is pressed

               @max_method : method, optional
                   the method used when up button is pressed

               @parent : bool, optional
                   if True, adapts the relative sizes according to master's relative sizes

               @initiate : bool, optional
                   if True, calls the method place()

               Methods
               -------
               disable()
                    disables the buttons of this class

               enable()
                    enables the buttons of this class

               get_value()
                    :returns: the value of the input label
    """

    def __init__(self, master, rlx, rly, rlwidth, rlheight, min_value, max_value, current_value, min_method = None, max_method = None, parent = True, initiate = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, parent = parent, initiate = initiate, background = BUTTON_UP_AND_DOWN_COLOR, **kw)
        assert min_value <= current_value and current_value <= max_value
        self.value = current_value
        self.max_value = max_value
        self.min_value = min_value
        self.min_method = min_method
        self.max_method = max_method
        self.__initialise()

    def get_value(self):
        return self.value

    def disable(self):
        self.button_down.disable()
        self.button_up.disable()

    def enable(self):
        self.button_up.enable()
        self.button_down.enable()

    def __go_up(self):
        if self.value < self.max_value:
            self.value += 1
            self.__update_label()
            if self.max_method != None:
                self.max_method()

    def __go_down(self):
        if self.value > self.min_value:
            self.value -= 1
            self.__update_label()
            if self.min_method != None:
                self.min_method()

    def __update_label(self):
        self.label.get_gui().config(text=f"{self.value}")

    def __initialise(self):
        height_percentage = 0.15
        relx = 0.1
        self.label = GUILabel(self, relx, height_percentage, 1 - relx * 2, (1 - 2*height_percentage), text= f"{self.value}",
                              **create_args(['background','foreground', 'font'], [VALUE_BACKGROUND_COLOR, VALUE_TEXT_COLOR, VALUE_FONT]))
        args = create_args(['background', 'foreground', 'font'], [BUTTON_UP_AND_DOWN_COLOR, VALUE_TEXT_COLOR, 'Helvetica 12 bold'])
        self.button_up = GUIButton(self, 0, 0, 1, height_percentage, text = '/\\', command = lambda: self.__go_up(), **args)
        self.button_down = GUIButton(self, 0, 1 - height_percentage, 1, height_percentage, text = '\\/', command = lambda: self.__go_down(), **args)


class LabelWithCheckboxAndText(GUILabel):
    """
               Class used to represent the a label that contains:
               checkbutton : a check button
               label : label that represents the text connected to the check button

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
                   the default state of the checkbutton

               @checkbox_text : str
                   the text of the checkbutton

               @parent : bool, optional
                   if True, adapts the relative sizes according to master's relative sizes

               @initiate : bool, optional
                   if True, calls the method place()

               Methods
               -------
               disable()
                    disables the buttons of this class

               enable()
                    enables the buttons of this class

               is_checked()
                    :returns: True if value button is checked.

               check()
                    changes the state of the check button
    """

    def __init__(self, master, rlx, rly, rlwidth, rlheight, check_flag, checkbox_text, parent = True, initiate = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, parent = parent, initiate = initiate, **kw)
        start_relx = 0.1
        self.check = tkinter.IntVar()
        self.check.set(0 + check_flag == True)
        self.__initialise_label(start_relx, checkbox_text)
        self.__initialise_button(start_relx)

    def is_checked(self):
        return self.check.get() == 1

    def check(self):
        self.check_button.check_the_button()

    def disable(self):
        self.check_button.disable()

    def enable(self):
        self.check_button.enable()

    def __initialise_label(self, relx, text):
        self.label = GUILabel(self, relx, 0, (1-relx), 1, background = CHECKBOX_TEXT_LABEL_BACKGROUND, foreground = CHECKBOX_TEXT_COLOR, font = CHECKBOX_TEXT_FONT, text = text)

    def __initialise_button(self, width_percentage):
        self.check_button = GUICheckbutton(self, 0, 0, width_percentage, 1, variable = self.check, onvalue = 1, offvalue = 0, background = self.label.get_background_color())


class GUIButton(GUIPiece):
    """
               Class used to represent the a button

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

               @type : GUITypes, optional
                   the type of the button. Possible types: GUITypes.BUTTON, GUITypes.CHECKBUTTON.

               @parent : bool, optional
                   if True, adapts the relative sizes according to master's relative sizes

               @initiate : bool, optional
                   if True, calls the method place()

               Methods
               -------
               disable()
                    sets the state of the button to disabled

               enable()
                    sets the state of the button to normal
    """

    def __init__(self, master, rlx, rly, rlwidth, rlheight, type = GUITypes.BUTTON, parent = True, initiate = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, type = type, parent = parent, initiate = initiate, **kw)

    def disable(self):
        self.get_gui()['state'] = 'disabled'

    def enable(self):
        self.get_gui()['state'] = 'normal'


class GUICheckbutton(GUIButton):
    """
               Class used to represent the a checkbutton

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

               @type : GUITypes, optional
                   the type of the button. Possible types: GUITypes.BUTTON, GUITypes.CHECKBUTTON.

               @parent : bool, optional
                   if True, adapts the relative sizes according to master's relative sizes

               @initiate : bool, optional
                   if True, calls the method place()

               Methods
               -------
               check_the_buttons()
                    changes the state of the button
    """

    def __init__(self, master, rlx, rly, rlwidth, rlheight, check_flag = False, parent = True, initiate = True, **kw):
        super().__init__(master, rlx, rly, rlwidth, rlheight, type = GUITypes.CHECKBUTTON, parent = parent,
                         initiate = initiate, command = lambda: self.check_the_button(), **kw)
        self.check = check_flag

    def check_the_button(self):
        self.check = not self.check