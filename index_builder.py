#module 4

import pandas as pd
import pickle

import string_formatting

def get_bigrams(string):
    lst = ["$" + string[0], string[len(string) - 1] + "$"]

    i = 0
    while i < len(string) - 1:
        if string[i] != "*" and string[i+1] != "*":
            lst.append(string[i] + string[i+1])
        i += 1
    return lst

class index:

    def __init__(self, dic_path):

        self.index = {} # a set of sets

        with open(dic_path, 'rb') as f:
            self.dic_list = pickle.load(f)
        
        
    def build_primary_index(self, df, name):
        
        for x in self.dic_list:
            self.index[x] = set()

        for _, row in df.iterrows():
            tokens = string_formatting.get_formatted_tokens(row[name])
            
            for token in tokens:
                self.index[str(token)].add((row["id"]))

    def build_secondary_index(self):
        for term in self.dic_list:
            bigrams = get_bigrams(term)
            for bigram in bigrams:
                if bigram in self.index:
                    self.index[bigram].add(term)
                else:
                    self.index[bigram] = set(term)

    def save(self, name):
        with open("save_files/{}.obj".format(name), "wb"  ) as f:
            pickle.dump(self.index, f )
        


    
if __name__ == "__main__":

    df = pd.read_csv("save_files/corpus.csv", sep = "|")

    title_index = index("save_files/title_dic.obj")
    title_index.build_primary_index(df, "title")
    title_index.save("title_index")

    description_index =  index("save_files/description_dic.obj")
    description_index.build_primary_index(df, "description")
    description_index.save("description_index")

    title_sec = index("save_files/title_dic.obj")
    title_sec.build_secondary_index()
    title_sec.save("title_secondary_index")

    desc_sec = index("save_files/description_dic.obj")
    desc_sec.build_secondary_index()
    desc_sec.save("description_secondary_index")