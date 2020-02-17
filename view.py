import tkinter as tk
from controller import controller, spelling_correction
from string_formatting import get_formatted_tokens

class ListItem(tk.Frame):
    def __init__(self, master, id, title, description, x, y):
        tk.Frame.__init__(self, master, bg='white', relief='ridge', bd=2)

        self.item(id, title, description, x, y)

    def item(self, id, title, description, x, y):
        tk.Button(self.master,
                 text=str(id) + ": " + title,
                 justify=tk.LEFT,
                 padx=20,
                 command= lambda: self.Create_Toplevel(id, title, description))\
            .place(x=x, y=y)
        tk.Label(self.master,
                 text=description[0:200] + " ...",
                 wraplength = 500,
                 justify=tk.LEFT)\
            .place(x=x, y=y+30)

    # modified from https://stackoverflow.com/questions/16803686/how-to-create-a-modal-dialog-in-tkinter
    def Create_Toplevel(self, id, title, description):

        # THE CLUE
        self.master.wm_attributes("-disabled", True)

        # Creating the toplevel dialog
        self.toplevel_dialog = tk.Toplevel(self)
        self.toplevel_dialog.minsize(300, 100)
        self.toplevel_dialog.transient(self)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW", self.Close_Toplevel)
        self.toplevel_dialog_label = tk.Label(self.toplevel_dialog, text=str(id) + ": " + title)
        self.toplevel_dialog_label.pack(side='top')
        self.toplevel_dialog_label = tk.Label(self.toplevel_dialog, text=description, wraplength = 300)
        self.toplevel_dialog_label.pack(side='top')
        self.toplevel_dialog_yes_button = tk.Button(self.toplevel_dialog, text='Close', command=self.Close_Toplevel)
        self.toplevel_dialog_yes_button.pack(side='left', fill='x', expand=True)

    def Close_Toplevel(self):

        # IMPORTANT!
        self.master.wm_attributes("-disabled", False) # IMPORTANT!

        self.toplevel_dialog.destroy()

        # Possibly not needed, used to focus parent window again
        self.master.deiconify()

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

        # search button
        tk.Button(self.parent,
                  text="Search",
                  padx=20,
                  command=lambda: self.search(self.entry.get(), self.v.get(), self.w.get())) \
            .place(x=900, y=40)

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

        ListItem(root,
                 1,
                 "ADM 1100 Introduction to Business Management (3 units)",
                 "This course provides the student with the basic knowledge necessary to effectively manage an organization. The student will learn what constitutes the manager's role and how the managerial functions of planning, organizing, leading, controlling, and communication are used to oversee the organization's human, financial, physical, material, and commercial resources. In particular, through the case method approach, students will be introduced to the art of logical problem solving, while addressing such issues as corporate social responsibility and managerial ethics.",
                 280,
                 140)

    def search(self, query, model, corpus):
        print(query, model, corpus)
        if model == 2:
            format_query = get_formatted_tokens(query)
            spelling_correction(format_query, corpus)
            controller(format_query, model, corpus)
        controller(query, model, corpus)


if __name__ == "__main__":
    root = tk.Tk()
    run = GUI(root)
    root.mainloop()
