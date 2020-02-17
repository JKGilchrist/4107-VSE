#module 4

import pandas as pd
import pickle

import string_formatting

from wildcard_handler import get_bigrams

class index:
    '''
    Builds all the non-weighted indices
    '''

    def __init__(self, dic_path):
        '''
        Sets up the index
        '''
        self.index = {} # a dict of sets

        with open(dic_path, 'rb') as f:
            self.dic_list = pickle.load(f) #set of tokenized terms
        
    def build_primary_index(self, df, name):
        '''
        Generates a primary index from the given dataframe and column name
        '''
        
        for x in self.dic_list:
            self.index[x] = set() #generates the dict entry and its empty set

        for _, row in df.iterrows():
            tokens = string_formatting.get_formatted_tokens(row[name])
            
            for token in tokens:
                self.index[str(token)].add((row["id"])) #adds to dict sets

    def build_secondary_index(self):
        '''
        Generates a secondary index, mapping a bigram to a set of words within the dictionary that contain it.
        '''
        for term in self.dic_list:
            bigrams = get_bigrams(term)
            for bigram in bigrams:
                if bigram in self.index:
                    self.index[bigram].add(term)
                else:
                    self.index[bigram] = set(term)

    def save(self, name):
        '''
        Saves the index, with the file name being the given name
        '''
        with open("save_files/{}.obj".format(name), "wb"  ) as f:
            pickle.dump(self.index, f )

def main():
    '''
    The main function, performing all the set-up required
    '''
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

