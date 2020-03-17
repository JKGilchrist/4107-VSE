import pickle
import pandas as pd

def create_weighted_ed_df():
    infile = open("./save_files/UO/descriptions_index.obj", "rb")
    index_description = pickle.load(infile)
    infile.close()
    infile = open("./save_files/UO/title_index.obj", "rb")
    index_title = pickle.load(infile)
    infile.close()

    df = pd.DataFrame(index_description.items(), columns=['word', 'index_list'])
    del df['index_list']
    df1 = pd.DataFrame(index_title.items(), columns=['word', 'index_list'])
    del df1['index_list']
    df2 = pd.concat([df, df1]).drop_duplicates().reset_index(drop=True)
    df2.to_pickle("save_files/UO/weighted_ed_df.pkl")
