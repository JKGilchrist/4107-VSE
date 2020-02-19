import pandas as pd
import numpy as np
from spelling_correction import weighted_edit_distance
from BRM import BRM
from vsm import vsm
from string_formatting import get_formatted_tokens

def spelling_correction(query, corpus):
    result = [query] * 3
    for i in range(len(query)):
        df = pd.read_csv("save_files/word_lists/" + query[i][0] + "word.csv", quoting=3, error_bad_lines=False)
        df.columns = ['word']
        df = df.drop_duplicates()
        df['word'] = df['word'].astype(str)
        if not df['word'].str.contains(query[i]).any():
            df['ed'] = df.apply(lambda x: weighted_edit_distance(query[i], x['word'].strip()), axis=1)
            df['format'] = df['word'].apply(lambda x: get_formatted_tokens(x))
            df['format'] = df['format'].apply(lambda x: ' '.join(x))
            df2 = pd.read_pickle("save_files/weighted_ed_df.pkl")
            df['in_corpus'] = df['format'].isin(df2['word'].tolist())
            df['ed'] = np.where(df['in_corpus'] == True, df['ed'] - 1, df['ed'])
            df = df.nsmallest(3, 'ed')
            words = df['word'].tolist()
            for j in range(len(words)):
                temp = query.copy()
                temp[i] = words[j].strip()
                result[j] = temp
        else:
            return []
    result.insert(0, query)
    for i in range(len(result)):
        result[i] = ' '.join(result[i])
    return result

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

    #vsm
    if model == 2:
        print('HERE!!!')
        desc = pd.read_pickle("save_files/description_index_with_weight.obj")
        title = pd.read_pickle("save_files/title_index_with_weight.obj")
        repr = vsm(corpus, get_formatted_tokens(query), title, desc)
        return list(repr.index.values)
    
    df = pd.read_csv("save_files/corpus.csv", sep = "|")
    return df.loc[ ids , ["title", "description"]]


if __name__ == "__main__":
    # x = controller("computer AND systems", 1, 1)
    # print(x.head())
    print(spelling_correction(['compter', 'programing'], 1))

