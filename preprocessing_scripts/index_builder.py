#module 4

import pandas as pd
import pickle

import string_formatting

from models.wildcard_handler import get_bigrams

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
        tmp = []
        for x in self.dic_list:
            tmp.append(x)
        tmp.sort()
        #print(tmp)

    def build_primary_index(self, df, name):
        '''
        Generates a primary index from the given dataframe and column name
        '''

        for x in self.dic_list:
            self.index[x] = set() #generates the dict entry and its empty set

        count = 0
        for _, row in df.iterrows():
            print("\r\tprimary {}: ".format(name) + str(round(count / len(df), 2) * 100).split(".")[0] + "%" , end = "")
            count += 1
            
            tokens = string_formatting.get_formatted_tokens(row[name])
            for token in tokens:
                self.index[str(token)].add((row["id"])) #adds to dict sets
        print()

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
    print("\nMaking indexes.")
    print("Creating Uottawa indexes")
    df = pd.read_csv("save_files/UO/corpus.csv", sep = "|")

    title_index = index("save_files/UO/titles_dic.obj")
    title_index.build_primary_index(df, "title")
    title_index.save("UO/title_index")

    descriptions_index =  index("save_files/UO/descriptions_dic.obj")
    descriptions_index.build_primary_index(df, "description")
    descriptions_index.save("UO/descriptions_index")

    title_sec = index("save_files/UO/titles_dic.obj")
    title_sec.build_secondary_index()
    title_sec.save("UO/title_secondary_index")
    print("\t secondary title")

    desc_sec = index("save_files/UO/descriptions_dic.obj")
    desc_sec.build_secondary_index()
    desc_sec.save("UO/description_secondary_index")
    print("\t secondary description")


    print("\nDoing Reuters")

    df = pd.read_csv("save_files/Reuters/corpus.csv", sep = "|")

    title_index = index("save_files/Reuters/titles_dic.obj")
    title_index.build_primary_index(df, "title")
    title_index.save("Reuters/title_index")

    descriptions_index =  index("save_files/Reuters/descriptions_dic.obj")
    descriptions_index.build_primary_index(df, "description")
    descriptions_index.save("Reuters/descriptions_index")

    title_sec = index("save_files/Reuters/titles_dic.obj")
    title_sec.build_secondary_index()
    title_sec.save("Reuters/title_secondary_index")
    print("\t secondary title")

    desc_sec = index("save_files/Reuters/descriptions_dic.obj")
    desc_sec.build_secondary_index()
    desc_sec.save("Reuters/description_secondary_index")
    print("\t secondary description")


if __name__ == "__main__":
    main()