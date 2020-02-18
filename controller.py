import pandas as pd
from spelling_correction import weighted_edit_distance
from BRM import BRM
from vsm import vsm
from string_formatting import get_formatted_tokens

def spelling_correction(query, corpus):
    if corpus == 1:
        for i in range(len(query)):
            df = pd.read_csv("save_files/word_lists/" + query[i][0] + "word.csv", quoting=3, error_bad_lines=False)
            df.columns = ['word']
            df = df.drop_duplicates()
            df['ed'] = df.apply(lambda x: weighted_edit_distance(query[i], x['word']), axis=1)
            df = df.nsmallest(3, 'ed')
            if df.ed.iloc[0] != 0:
                words = df['word'].to_list()
                return words
    return []

def controller(query, model, corpus):
    #boolean
    ids = []
    if model == 1:
        desc_brm = BRM("save_files/description_index.obj", "save_files/description_secondary_index.obj")
        title_brm = BRM("save_files/title_index.obj", "save_files/title_secondary_index.obj")
        ids1 = desc_brm.run_model(query)
        ids2 = title_brm.run_model(query)

        ids3 = [t for t in ids2 if t in ids1]  # in both
        for x in ids3:
            ids1.remove(x)
            ids2.remove(x)
        ids = ids3 + ids2 + ids1
        return ids

    if model == 2:
        desc = pd.read_pickle("save_files/description_index_with_weight.obj")
        title = pd.read_pickle("save_files/title_index_with_weight.obj")
        repr = vsm(corpus, get_formatted_tokens(query), title, desc)
        return list(repr.index.values)
    
    df = pd.read_csv("save_files/corpus.csv", sep = "|")
    return df.loc[ ids , ["title", "description"]]


if __name__ == "__main__":
    x = controller("computer AND systems", 1, 1)
    print(x.head())
