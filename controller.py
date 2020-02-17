import pandas as pd
from spelling_correction import weighted_edit_distance
import BRM

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
    if model == 1:
        brm = BRM.BRM("save_files/description_index.obj", "save_files/description_secondary_index.obj")
        brm.run_model(query)
        print(brm.run_model(query))
