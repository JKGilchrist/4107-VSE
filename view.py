import tkinter as tk
import pandas as pd
import numpy as np
import math

import preprocessing_scripts
from controller import boolean_controller, vector_controller, spelling_correction, next_word

class ListItem(tk.Frame):

    def __init__(self, master, id, title, description, x, y, score, query, doc_id):
        tk.Frame.__init__(self, master, bg='white', relief='ridge', bd=2)

        self.button = tk.Button(self.master, 
                 text=str(id) + ": " + title,
                 justify = tk.LEFT, padx = 20,
                 command= lambda: self.expanded_window(id, title, description))
        self.button.place(x = x, y = y)
        if str(description) == 'nan':
            description = "No description provided."
        if len(description) <= 140:
           txt = description
        else:
           txt = description[:140].strip() + "..."
        if score != -1:
            txt = txt + " (" + str(score) + ")"
        self.label = tk.Label(self.master, text = txt, wraplength = 500, justify= tk.LEFT)
        self.label.place(x = x + 20, y = y + 30)

        # Revelant radio buttons
        
        self.model2 = tk.IntVar(value=0)
        self.button1 = tk.Radiobutton(root,
                       text="Relevant",
                       variable=self.model2,
                       value=1,
                       command=lambda: self.save_relevance(self.model2.get(), doc_id, query))
        self.button1.place(x=x+20, y=y+60)
        self.button2 = tk.Radiobutton(root,
                       text="Not relevant",
                       variable=self.model2,
                       value=2,
                       command=lambda: self.save_relevance(self.model2.get(), doc_id, query))
        self.button2.place(x=x+100, y=y+60)
        


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
        self.button1.destroy()
        self.button2.destroy()

    # modified from https://stackoverflow.com/questions/16803686/how-to-create-a-modal-dialog-in-tkinter
    def expanded_window(self, id, title, description):

        # THE CLUE
        self.master.wm_attributes("-disabled", True)

        # Creating the toplevel dialog
        self.toplevel_dialog = tk.Toplevel(self)
        self.toplevel_dialog.minsize(500, 100)
        self.toplevel_dialog.transient(self)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW", self.close_expanded_window)
        self.toplevel_dialog_label = tk.Label(self.toplevel_dialog, text=str(id) + ": " + title)
        self.toplevel_dialog_label.pack(side='top')
        self.toplevel_dialog_label = tk.Label(self.toplevel_dialog, text=description, wraplength = 300)
        self.toplevel_dialog_label.pack(side='top')
        self.toplevel_dialog_yes_button = tk.Button(self.toplevel_dialog, text='Close', command=self.close_expanded_window)
        self.toplevel_dialog_yes_button.pack(side='left', fill='x', expand=True)

    def close_expanded_window(self):
        # IMPORTANT!
        self.master.wm_attributes("-disabled", False) # IMPORTANT!
        self.toplevel_dialog.destroy()

        # Possibly not needed, used to focus parent window again
        self.master.deiconify()


class GUI(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        #The useful variables
        self.tmp_elems = []
        self.query = []
        self.txt = ""
        self.buttons = [] #Query completion buttons
        #as well as self.model, self.corpus

        
        self.model = tk.IntVar(value = 1)
        
        self.set_up_ui()

    def set_up_ui(self):
        self.parent.geometry("1000x1000")
        self.parent.title("Spring Search Engine")

        tk.Label(self.parent, text = "Spring", justify=tk.LEFT, padx=20, font=("Courier", 44)).place(x=5, y=5)
        
        self.entry = tk.Entry(self.parent, width = 99, textvariable = tk.StringVar())
        self.entry.bind('<space>', (lambda _: self.completion()) )
        self.entry.bind('<Return>', (lambda _: self.search(self.entry.get(), self.model.get(), self.corpus.get())  ) )
        self.entry.place(x = 283, y = 43)

        # search button
        tk.Button(self.parent, text="Search", padx = 20, command = lambda: self.search(self.entry.get(), self.model.get(), self.corpus.get())).place(x=900, y=40)

        # Model radio buttons
        tk.Label(self.parent, text = "Model: ", justify = tk.RIGHT, padx = 20).place(x = 13, y =  80)
        tk.Radiobutton(root, text = "Boolean", padx = 0, variable = self.model, value = 1).place(x = 90, y = 80)
        tk.Radiobutton(root, text = "Vector Space", padx = 0, variable = self.model, value = 2).place(x = 160, y = 80)

        # Corpus radio buttons
        self.corpus = tk.IntVar(value=1)
        tk.Label(self.parent, text = "Corpus:", justify = tk.RIGHT, padx = 20).place(x = 9, y=100 )
        tk.Radiobutton(root, text = "UofO", padx = 0, variable = self.corpus, value = 1).place(x = 90, y = 100 )
        tk.Radiobutton(root, text = "Reuters", padx = 0, variable = self.corpus, value = 2).place(x = 160, y = 100 )


    def completion(self):

        ans = next_word(self.entry.get(), self.corpus.get(), self.model.get())
        print(ans)

        #f tkinter
        try: 
            i = 0
            x = tk.Button(self.parent, 
                    text= ans[0],
                    justify = tk.LEFT, padx = 20, width = 10, height = 1,
                    command = lambda: self.completion_button_event(ans[0])
                    )
            x.place(x = 283, y = 63 + 26 * i)
            self.buttons.append(x)
            i += 1
            
            x = tk.Button(self.parent, 
                    text= ans[1],
                    justify = tk.LEFT, padx = 20, width = 10, height = 1,
                    command = lambda: self.completion_button_event(ans[1])
                    )
            x.place(x = 283, y = 63 + 26 * i)
            self.buttons.append(x)
            i += 1
            
            x = tk.Button(self.parent, 
                    text= ans[2],
                    justify = tk.LEFT, padx = 20, width = 10, height = 1,
                    command = lambda: self.completion_button_event(ans[2])
                    )
            x.place(x = 283, y = 63 + 26 * i)
            self.buttons.append(x)
            i += 1
            
            x = tk.Button(self.parent, 
                    text= ans[3],
                    justify = tk.LEFT, padx = 20, width = 10, height = 1,
                    command = lambda: self.completion_button_event(ans[3])
                    )
            x.place(x = 283, y = 63 + 26 * i)
            self.buttons.append(x)
            i += 1
            
            x = tk.Button(self.parent, 
                    text= ans[4],
                    justify = tk.LEFT, padx = 20, width = 10, height = 1,
                    command = lambda: self.completion_button_event(ans[4])
                    )
            x.place(x = 283, y = 63 + 26 * i)
            self.buttons.append(x)

        except:
            pass
        print("T")

    def completion_button_event(self, txt):
        print("G")
        self.entry.insert(tk.END, txt + " ")
        
        for x in self.buttons:
            x.destroy()
        self.completion()


    def did_you_mean(self, responses):
        x = tk.Label(self.parent, text = "Spelling mistake detected. Showing search results instead for '" + responses[1] + "'.")
        x.place(x = 280, y = 60)
        self.tmp_elems.append(x)
        #options spelling correction
        y = tk.Label(self.parent, text = "Did you mean:")
        y.place(x = 280, y = 80)
        self.tmp_elems.append(y)
        for i in range(3):
            j = 0
            if i > 0:
                j = i + 1
            op = tk.Button(self.parent, text = responses[j], fg = "blue")
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
            x = ListItem(root, ind, row["title"], row["description"],
                 280, 150 + 80 * (ind - 1),
                 score, query, row["index"])
            ind += 1
            self.tmp_elems.append(x)

    def empty_result(self):
        x = tk.Label(self.parent, text = "This query did not return any results")
        x.place(x = 280, y = 150)
        self.tmp_elems.append(x)

    def search(self, query, model, corpus, spell_correct = 1):
        self.query = query
        corpus2 = corpus
        
        for elem in self.tmp_elems:
            elem.destroy()
        for elem in self.buttons:
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
                response = spelling_correction(query.strip().split(" "), corpus)
                self.query = response
                if len(response) > 0:
                    self.did_you_mean(response)
                    query = response[1]
                
            try:
                if query != '':
                    print('======================')
                    print(query)
                    print(corpus)
                    print('======================')
                    result = vector_controller(query, corpus2)
            except:
                print("VSM fail")

        if result.empty:
            self.empty_result()
        else:
            print(result)
            self.update(result, query)


if __name__ == "__main__":
    
    print("Checking if all required files are generated.")
    #preprocessing_scripts.run_preprocessing()
    
    root = tk.Tk()
    GUI(root)
    root.mainloop()