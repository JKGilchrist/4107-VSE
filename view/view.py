import tkinter as tk

class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        self.parent.geometry("1000x1000")
        self.parent.title("Spring Search Engine")

        # Title
        tk.Label(self.parent,
                 text="Spring",
                 justify=tk.LEFT,
                 padx=20,
                 font=("Courier", 44)).place(x=5, y=5)

        # Search bar
        self.entry = tk.Entry(self.parent,
                              width=100)
        self.entry.place(x=300, y=40)

        #spelling correction
        self.label = tk.Label(self.parent,
                              text="")
        self.label.place(x=300, y=60)

        # Model radio buttons
        self.v = tk.IntVar(value=0)
        tk.Label(self.parent,
                 text="Model: ",
                 justify=tk.LEFT,
                 padx=20).place(x=280, y=80)
        tk.Radiobutton(root,
                       text="Boolean",
                       padx=20,
                       variable=self.v,
                       value=1).place(x=350, y=80)
        tk.Radiobutton(root,
                       text="Vector Space",
                       padx=20,
                       variable=self.v,
                       value=2).place(x=480, y=80)

        # Corpus radio buttons
        self.w = tk.IntVar(value=0)
        tk.Label(self.parent,
                 text="Corpus:",
                 justify=tk.LEFT,
                 padx=20).place(x=280, y=100)
        tk.Radiobutton(root,
                       text="UofO catalog",
                       padx=20,
                       variable=self.w,
                       value=1).place(x=350, y=100)
        tk.Radiobutton(root,
                       text="Reuters",
                       padx=20,
                       variable=self.w,
                       value=2).place(x=480, y=100)


if __name__ == '__main__':
    root = tk.Tk()
    run = GUI(root)
    root.mainloop()
