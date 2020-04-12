import tkinter as tk
import pandas as pd
import numpy as np
import math

import preprocessing_scripts

from controller import boolean_controller, vector_controller, spelling_correction


class ListItem(tk.Frame):

    def __init__(self, master, id, title, description, x, y, score, query, doc_id):
        tk.Frame.__init__(self, master, bg='white', relief='ridge', bd=2)

        self.button = tk.Button(self.master,
                 text=str(id) + ": " + title,
                 justify=tk.LEFT,
                 padx=20,
                 command= lambda: self.Create_Toplevel(id, title, description))
        self.button.place(x=x, y=y)
        if str(description) == 'nan':
            description = "No description provided."
        if len(description) <= 140:
           txt = description
        else:
           txt = description[:140].strip() + "..."
        if score != -1:
            txt = txt + " (" + str(score) + ")"
        self.label = tk.Label(self.master,
                 text=txt,
                 wraplength = 500,
                 justify= tk.LEFT)
        self.label.place(x=x+20, y=y+30)

        # Revelant radio buttons
        self.y = tk.IntVar(value=0)
        self.model = self.y
        tk.Radiobutton(root,
                       text="Relevant",
                       variable=self.y,
                       value=1,
                       command=lambda: self.save_relevance(self.y.get(), doc_id, query)).place(x=x+20, y=y+60)
        tk.Radiobutton(root,
                       text="Not relevant",
                       variable=self.y,
                       value=2,
                       command=lambda: self.save_relevance(self.y.get(), doc_id, query)).place(x=x+100, y=y+60)

    def save_relevance(self, y, id, query):
        try:
            dictionary = np.load('relevant_dict.npy', allow_pickle='TRUE').item()
        except:
            dictionary = {}
        if query in dictionary:
            if y == 1: # relevant
                dictionary[query][0].append(id)
                dictionary[query][0] = list(set(dictionary[query][0]))
            else: #not relevant
                dictionary[query][1].append(id)
                dictionary[query][1] = list(set(dictionary[query][1]))
        else:
            if y==1: #relevant
                dictionary[query] = [[id], []]
            else: #not relevant
                dictionary[query] = [[], [id]]
        np.save('relevant_dict.npy', dictionary)
        print(dictionary)

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
        self.display_user_interface()
        self.tmp_elems = []
        self.query = []
        self.model = 1
        self.corpus = 1

    def display_user_interface(self):
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

    def did_you_mean(self, responses):
        x = tk.Label(self.parent,text= "Spelling mistake detected. Showing search results instead for '" + responses[1] + "'.")
        x.place(x=280, y=60)
        self.tmp_elems.append(x)
        #options spelling correction
        y = tk.Label(self.parent,text="Did you mean:")
        y.place(x=280, y=80)
        self.tmp_elems.append(y)
        for i in range(3):
            j = 0
            if i > 0:
                j = i + 1
            op = tk.Label(self.parent,
                             text=responses[j],
                             fg="blue")
            op.place(x=370 + i * 100, y=80)
            op.bind("<Button-1>", lambda event, arg= j: self.handle_replacement(arg, responses[arg]))

            self.tmp_elems.append(op)


    def handle_replacement(self, args, txt):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, txt)
        self.search(self.query[args], 2, self.corpus, 0)

    def update(self, df, query):
        ind = 1
        df['index'] = df.index
        for _, row in df[:10].iterrows():
            score = -1
            
            if "score" in df.columns:
                score = row["score"]
            x = ListItem(root,
                 ind,
                 row["title"],
                 row["description"],
                 280,
                 150 + 80 * (ind - 1),
                 score,
                 query,
                 row["index"])
            ind += 1
            self.tmp_elems.append(x)

    def empty_result(self):
        x = tk.Label(self.parent, text="This query did not return any results")
        x.place(x=280, y=150)
        self.tmp_elems.append(x)

    def search(self, query, model, corpus, spell_correct = 1):
        self.query = query
        print("1" + query)
        print("1.5" + self.query)

        for elem in self.tmp_elems:
            elem.destroy()
        
        result = pd.DataFrame()

        if model == 1:
            try:
                result = boolean_controller(query, corpus)
            except:
                print("BRM fail")
                result = pd.DataFrame()

        else: # model == 2:
            if spell_correct:
                response = spelling_correction(query.split(" "), corpus)
                self.query = response
                if len(response) > 0:
                    self.did_you_mean(response)
                    query = response[1]
                
            try:
                if query != '':
                    result = vector_controller(query, corpus)
            except:
                print("VSM fail")

        if result.empty:
            self.empty_result()
        else:
            print(result)
            self.update(result, query)


if __name__ == "__main__":
    print("Checking if all required files are generated.")
    preprocessing_scripts.run_preprocessing()
    root = tk.Tk()
    run = GUI(root)
    root.mainloop()