import pandas as pd
from spelling_correction import weighted_edit_distance
from BRM import BRM

def spelling_correction(query, corpus):
    if corpus == 1:
        df = pd.read_pickle("save_files/weighted_ed_df.pkl")
        for i in range(len(query)):
            df['ed'] = df.apply(lambda x: weighted_edit_distance(query[i], x['word']), axis=1)
            if df.loc[0, 'ed'] != 0:
                df = df.nsmallest(5, 'ed')
                print(df)
                query[i] = df.loc[0, 'word']
        print(query)

def controller(query, model, corpus):
    #boolean
    ids = []
    if model == 1:
        desc_brm = BRM("save_files/description_index.obj", "save_files/description_secondary_index.obj")
        title_brm = BRM("save_files/title_index.obj", "save_files/title_secondary_index.obj")
        ids1 = desc_brm.run_model(query)
        ids2 = title_brm.run_model(query)
        ids3 = [t for t in ids2 if t in ids1] #in both
        for x in  ids3:
            ids1.remove(x)
            ids2.remove(x)
        ids = ids3 + ids2 + ids1
        
    #VSM
    else:
        print("TODO")
        ids = []
    
    df = pd.read_csv("save_files/corpus.csv", sep = "|")
    return df.loc[ ids , ["title", "description"]]


if __name__ == "__main__":
    x = controller("computer AND systems", 1, 1)
    print(x.head())





