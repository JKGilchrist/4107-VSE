import pandas as pd
import numpy as np
from spelling_correction import weighted_edit_distance
from BRM import BRM
from vsm import vsm
from string_formatting import get_formatted_tokens

def spelling_correction(query, corpus):
    '''
    If no spelling correction needed returns an empty list.
    If spelling correction, returns a list where the first element is the original query, and the subsequent three
    elements are the top three most likely queries.
    '''
    result = [query] * 3
    flag = False
    for i in range(len(query)):
        query[i] = query[i].lower()
        df = pd.read_csv("save_files/word_lists/" + query[i][0] + "word.csv", quoting=3, error_bad_lines=False, sep = "|")
        if not df['word'].str.contains(query[i]).any():
            flag = True
            df['ed'] = df.apply(lambda x: weighted_edit_distance(query[i], str(x['word']).strip()), axis=1)
            df2 = pd.read_pickle("save_files/weighted_ed_df.pkl")
            df['in_corpus'] = df['format'].isin(df2['word'].tolist())
            df['ed'] = np.where(df['in_corpus'] == True, df['ed'] - 3, df['ed'])
            df = df.nsmallest(3, 'ed')
            words = df['word'].tolist()
            for j in range(len(words)):
                temp = result[j].copy()
                temp[i] = words[j].strip()
                result[j] = temp
    if (flag == False):
        return []
    result.insert(0, query)
    for i in range(len(result)):
        result[i] = ' '.join(result[i])
    return result

def boolean_controller(query, corpus):
    '''
    Returns a DataFrame containing the results of the BRM for the given query on the given corpus
    '''
    desc_brm = BRM("save_files/description_index.obj", "save_files/description_secondary_index.obj")
    title_brm = BRM("save_files/title_index.obj", "save_files/title_secondary_index.obj")
    desc_ids = desc_brm.run_model(query)
    title_ids = title_brm.run_model(query)
    both_ids = []
    ids = []
    if desc_ids != [] and title_ids != []:
        for x in title_ids:
            if x in desc_ids:
                both_ids.append(x)
        both_ids = list(set(both_ids))
        for x in both_ids:
            desc_ids.remove(x)
            title_ids.remove(x)
        ids = both_ids + title_ids + desc_ids
    elif desc_ids == []:
        ids = title_ids
    elif title_ids == []:
        ids = desc_ids
    df = pd.read_csv("save_files/corpus.csv", sep = "|")
    return df.loc[ ids , ["title", "description"]]

def vector_controller(query, corpus):
    '''
    Returns a DataFrame containing the results of the VSM for the given query on the given corpus
    '''
    query.lower()
    desc = pd.read_pickle("save_files/description_index_with_weight.obj")
    title = pd.read_pickle("save_files/title_index_with_weight.obj")
    repr = vsm(corpus, get_formatted_tokens(query), title, desc)
    corpus = pd.read_csv("save_files/corpus.csv", sep="|")
    result = corpus.loc[ repr[0] , ["title", "description"]]
    result['score'] = repr[1]
    return result