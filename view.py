import tkinter as tk
import pandas as pd
import math
from controller import boolean_controller, vector_controller, spelling_correction

class ListItem(tk.Frame):
    def __init__(self, master, id, title, description, x, y):
        tk.Frame.__init__(self, master, bg='white', relief='ridge', bd=2)

        self.button = tk.Button(self.master,
                 text=str(id) + ": " + title,
                 justify=tk.LEFT,
                 padx=20,
                 command= lambda: self.Create_Toplevel(id, title, description))
        self.button.place(x=x, y=y)
        if str(description) == 'nan':
            description = "No description provided"
        if len(description) <= 140:
           txt = description
        else:
           txt = description[:140] + " ..."
        self.label = tk.Label(self.master,
                 text=txt,
                 wraplength = 500,
                 justify= tk.LEFT)
        self.label.place(x=x + 20, y=y+30)
    
    def destroy(self):
        self.button.destroy()
        self.label.destroy()

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
        self.elems = []
        self.query = []
        self.model = 1
        self.corpus = 1

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
        self.link = tk.Label(self.parent,
                              text="",
                                fg="blue")
        self.link.place(x=280, y=60)
        self.link.bind("<Button-1>", lambda event, arg=self.link.cget("text"): self.callback(event, arg))

        #options spelling correction
        self.did_you_mean = tk.Label(self.parent,
                                text="")
        self.did_you_mean.place(x=280, y=80)
        self.did_you_mean.bind("<Button-1>", lambda event, arg=1: self.callback(event, arg))

        self.option1 = tk.Label(self.parent,
                             text="",
                             fg="blue")
        self.option1.place(x=370, y=80)
        self.option1.bind("<Button-1>", lambda event, arg=1: self.callback(event, arg))

        self.option2 = tk.Label(self.parent,
                             text="",
                             fg="blue")
        self.option2.place(x=585, y=80)
        self.option2.bind("<Button-1>", lambda event, arg=2: self.callback(event, arg))

        self.option3 = tk.Label(self.parent,
                             text="",
                             fg="blue")
        self.option3.place(x=800, y=80)
        self.option3.bind("<Button-1>", lambda event, arg=3: self.callback(event, arg))

        # Model radio buttons
        self.v = tk.IntVar(value=1)
        self.model = self.v
        tk.Label(self.parent,
                 text="Model: ",
                 justify=tk.LEFT,
                 padx=20).place(x=280, y=100)
        tk.Radiobutton(root,
                       text="Boolean",
                       padx=20,
                       variable=self.v,
                       value=1).place(x=350, y=100)
        tk.Radiobutton(root,
                       text="Vector Space",
                       padx=20,
                       variable=self.v,
                       value=2).place(x=480, y=100)

        # Corpus radio buttons
        self.w = tk.IntVar(value=1)
        self.corpus = self.w
        tk.Label(self.parent,
                 text="Corpus:",
                 justify=tk.LEFT,
                 padx=20).place(x=280, y=120)
        tk.Radiobutton(root,
                       text="UofO catalog",
                       padx=20,
                       variable=self.w,
                       value=1).place(x=350, y=120)
        tk.Radiobutton(root,
                       text="Reuters",
                       padx=20,
                       variable=self.w,
                       state = "disabled",
                       value=2).place(x=480, y=120)


    def callback(self, event, args):
        # self.search(self.query, self.model, self.corpus)
        if args != "":
            self.link.config(text="")
            self.option1.config(text="")
            self.option2.config(text="")
            self.option3.config(text="")
            self.did_you_mean.config(text="")
            self.search(self.query[args], self.model, self.corpus)

    def update(self, df):
        ind = 1
        for _, row in df[:10].iterrows():
            x = ListItem(root,
                 ind,
                 row["title"],
                 row["description"],
                 280,
                 150 + 70 * (ind - 1)) 
            ind += 1
            self.elems.append(x)

    def empty_result(self):
        x = tk.Label(self.parent, text="This query did not return any results")
        x.place(x=280, y=150)
        self.elems.append(x)

    def search(self, query, model, corpus, spell_correct = 1):
        print(query)

        for elem in self.elems:
            elem.destroy()
        
        result = pd.DataFrame()

        if model == 1:
            try:
                result = boolean_controller(query, corpus)
            except:
                print("BRM fail")
                result = pd.DataFrame()

        else: # model == 2:
            response = spelling_correction(query.split(" "), corpus)
            self.query = response
            if len(response) > 0:
                self.link.config(text=response[1])
                self.option1.config(text=response[0])
                self.option2.config(text=response[2])
                self.option3.config(text=response[3])
                self.did_you_mean.config(text="Did you mean:")
                query = response[1]
            else:
                self.link.config(text="")
                self.option1.config(text="")
                self.option2.config(text="")
                self.option3.config(text="")
                self.did_you_mean.config(text="")
                
            try:
                if query != '':
                    result = vector_controller(query, corpus)
            except:
                print("VSM fail")

        if result.empty:
            self.empty_result()
        else:
            print(result)
            self.update(result)


if __name__ == "__main__":
    root = tk.Tk()
    run = GUI(root)
    root.mainloop()
