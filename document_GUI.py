"""File to contain all GUI related elements of document manager"""
import document_manager as doc
import tkinter as tk
LARGE_FONT = ("Verdana", 12)

class DocManagerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        #container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.attributes("-zoomed", True)
        self.frames = {}
        for F in (HomePage, Projects, DocTypes):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        print((cont).__name__)
        frame.tkraise()

        
    def make_buttons(self):
        hb = MyButton(['Home', 0, 0, HomePage], self)
        pb= MyButton(['Projects', 1, 0, Projects], self)
        db = MyButton(['Document Types', 2, 0, DocTypes], self)
        hb.nav_button.grid(row=hb.row, column=hb.column)
        pb.nav_button.grid(row=pb.row, column=pb.column)
        db.nav_button.grid(row=db.row, column=db.column)




class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.grid(row=0, column=1)
        controller.make_buttons()
        print('I am HEREEE')
        # label.pack(pady=10, padx=10)
        # button = tk.Button(self, text="Visit Projects",
        #                    command=lambda: controller.show_frame(Projects))
        # button.pack()
        #
        # button2 = tk.Button(self, text="Visit Document Types:",
        #                     command=lambda: controller.show_frame(DocTypes))
        # button2.pack()

class Projects(HomePage, tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Projects!!!", font=LARGE_FONT)
        label.grid(row=0, column=0)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.grid(row=1, column=0)

        button2 = tk.Button(self, text="Document Types",
                            command=lambda: controller.show_frame(DocTypes))
        button2.grid(row=2, column=0)





class DocTypes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Document Types!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = tk.Button(self, text="Projects",
                            command=lambda: controller.show_frame(Projects))
        button2.pack()

class MyButton(tk.Button):
    """Class to define key parameters of each button"""
    def __init__(self, args, controller):
        self.text = args[0]
        self.row = args[1]
        self.column = args[2]
        self.page_name = args[3]
        self.set_colour(args[3])
        self.nav_button = tk.Button(controller, text=self.text,
                  command=lambda: controller.show_frame(self.page_name))

    def set_colour(self, page_name):
        if self.page_name == page_name:
            self.colour = 'green2'
        else:
            self.colour = 'seashell3'





app = DocManagerApp()
app.mainloop()

