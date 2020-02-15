#module 4

import pandas as pd
import pickle

import string_formatting

class index:

    def __init__(self, dic_path):

        self.index = {}

        dic_list = list(pickle.load(open(dic_path, 'rb')))
        
        for x in dic_list:
            self.index[x] = []

    def add_from_df(self, df, name):
        for _, row in df.iterrows():
            tokens = string_formatting.get_formatted_tokens(row[name])
            
            for token in tokens:
                self.index[str(token)].append((row["id"]))

    def save(self, name):
        pickle.dump(self.index, open("save_files/{}.obj".format(name), "wb"  ) )

    
if __name__ == "__main__":

    df = pd.read_csv("save_files/corpus.csv", sep = "|")

    title_index = index("save_files/title_dic.obj")
    title_index.add_from_df(df, "title")
    title_index.save("title_index")

    description_index =  index("save_files/description_dic.obj")
    description_index.add_from_df(df, "description")
    description_index.save("description_index")