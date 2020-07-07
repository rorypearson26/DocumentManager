"""File to contain all GUI related elements of document manager"""
import document_manager as doc
import flask
import tkinter as tk
LARGE_FONT = ("Verdana", 12)
HUGE_FONT = ("Verdana", 20)

class DocManagerApp(tk.Tk):
    """Class to initialise the main app"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.attributes("-zoomed", True)
        self.frames = {}
        for F in (HomePage, Projects, DocTypes):
            frame = F(parent=container, frame_name=F)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        """Method to bring the selected frame to the front"""
        frame = self.frames[cont]
        frame.tkraise()
        frame.grid(row=0, column=0, sticky="nsew")

class GenericPage(tk.Frame):
    """Class to define a generic page in the app
    Inputs:
    parent - the container of the app defined in DocManagerApp
    frame_name - the class of the page being defined (e.g HomePage)
    """
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        tk.Frame.__init__(self, self.parent)

        #Set up navigation buttons
        hb = MyButton(frame_name=self, destination=HomePage, text='Homepage', row=1, column=0)
        pb = MyButton(frame_name=self, destination=Projects, text='Projects', row=2, column=0)
        db = MyButton(frame_name=self, destination=DocTypes, text='Document Types', row=3, column=0)
        nav_buttons = [hb, pb, db]
        for button in (nav_buttons):
            MyButton.nav_set_colour(button)
            button.nav_button.grid(row=button.row, column=button.column)

class HomePage(GenericPage):
    def __init__(self, *args, **kwargs):
        GenericPage.__init__(self, *args, **kwargs)
        TitleLab = MyLabel(frame_name=self, font=HUGE_FONT, disp_text='Home Page',
                           row=0, column=2, pady=10)

class Projects(GenericPage):
    def __init__(self, *args, **kwargs):
        GenericPage.__init__(self, *args, **kwargs)
        TitleLab = MyLabel(frame_name=self, font=HUGE_FONT, disp_text='Projects',
                           row=0, column=2, pady=10)

class DocTypes(GenericPage):
    def __init__(self, *args, **kwargs):
        GenericPage.__init__(self, *args, **kwargs)
        TitleLab = MyLabel(frame_name=self, font=HUGE_FONT, disp_text='Document Types',
                           row=0, column=2, pady=10)

class MyButton(tk.Button):
    """Class to define key parameters of each button"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.nav_button = tk.Button(self.frame_name, text=self.text,
                  command=lambda: app.show_frame(self.destination))

    def nav_set_colour(self):
        if (self.frame_name).__class__.__name__ == (self.destination).__name__:
            self.colour = 'green2'
        else:
            self.colour = 'seashell3'
        self.nav_button['bg'] =self.colour

class MyLabel(tk.Label):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.add_label()
    def add_label(self):
        label = tk.Label(self.frame_name, text=self.disp_text, font=self.font)
        label.grid(row=self.row, column=self.column, pady=self.pady)

app = DocManagerApp()
app.mainloop()





