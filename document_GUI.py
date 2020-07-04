"""File to contain all GUI related elements of document manager"""
import document_manager as doc
import tkinter as tk
LARGE_FONT = ("Verdana", 12)

class DocManagerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.attributes("-zoomed", True)
        self.frames = {}
        for F in (HomePage, Projects, DocTypes):
            frame = F(parent=container, frame_name=F, text=str((F).__name__))
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        print((cont).__name__)

        frame.tkraise()
        print('showing frame')

class GenericPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        tk.Frame.__init__(self, self.parent)



        hb = MyButton(frame_name=self, destination=HomePage, text='Homepage', row=0, column=0)
        pb = MyButton(frame_name=self, destination=Projects, text='Projects', row=1, column=0)
        db = MyButton(frame_name=self, destination=DocTypes, text='Document Types', row=2, column=0)
        hb.nav_button.grid(row=hb.row, column=hb.column)
        pb.nav_button.grid(row=pb.row, column=pb.column)
        db.nav_button.grid(row=db.row, column=db.column)
        print('generic page bottom', self.text)

    def add_label(self, disp_text):
        print(disp_text)
        label = tk.Label(self, text=self.text, font=LARGE_FONT)
        label.grid(row=0, column=1)



class HomePage(GenericPage):
    # def __init__(self):
    # #     GenericPage.__init__(self)
    #     #GenericPage.add_label('This is HomePage')
    #     print('this is child')
    pass

class Projects(GenericPage):
    pass

class DocTypes(GenericPage):
    pass

class MyButton(tk.Button):
    """Class to define key parameters of each button"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            #print(key,value)
        self.nav_button = tk.Button(self.frame_name, text=self.text,
                  command=lambda: app.show_frame(self.destination))

    def set_colour(self, page_name):
        if self.page_name == page_name:
            self.colour = 'green2'
        else:
            self.colour = 'seashell3'
app = DocManagerApp()
app.mainloop()




