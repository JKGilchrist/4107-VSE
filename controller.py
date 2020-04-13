import pandas as pd
import numpy as np
from models.spelling_correction import weighted_edit_distance
from models.BRM import BRM
from models.vsm import vsm
from string_formatting import get_formatted_tokens
from models.query_expansion import expand_query
from models.rocchio_model import rocchio
from collections import Counter

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
        df = pd.read_csv("save_files/word_lists/" + query[i][0].upper() + "word.csv", quoting=3, error_bad_lines=False, sep = "|")
        if not df['word'].str.contains(query[i]).any():
            flag = True
            df['ed'] = df.apply(lambda x: weighted_edit_distance(query[i], str(x['word']).strip()), axis=1)
            if corpus == 1:
                df2 = pd.read_pickle("save_files/UO/weighted_ed_df.pkl")
            else:
                df2 = pd.read_pickle("save_files/Reuters/weighted_ed_df.pkl")
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
    query = expand_query(query, "boolean")
    if corpus == 1:
        path = "save_files/UO/"
    else:
        path = "save_files/Reuters/"

    title_brm = BRM(path + "title_index.obj", path + "title_secondary_index.obj")
    title_ids = title_brm.run_model(query)
    desc_brm = BRM(path + "descriptions_index.obj", path + "description_secondary_index.obj")
    desc_ids = desc_brm.run_model(query)
    
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

    df = pd.read_csv(path + "corpus.csv", sep = "|")
    return df.loc[ ids , ["title", "description"]]

def vector_controller(query, corpus):
    '''
    Returns a DataFrame containing the results of the VSM for the given query on the given corpus
    '''
    query.lower()
    rel_dict = np.load('relevant_dict.npy', allow_pickle='TRUE').item()
    if corpus == 1:
        newdict = np.load('models/complete_dict.npy', allow_pickle='TRUE').item()
        desc = pd.read_pickle("save_files/UO/descriptions_index_with_weight.obj")
        title = pd.read_pickle("save_files/UO/title_index_with_weight.obj")
    else:
        newdict = np.load('models/complete_dict_reuters.npy', allow_pickle='TRUE').item()
        desc = pd.read_pickle("save_files/Reuters/descriptions_index_with_weight.obj")
        title = pd.read_pickle("save_files/Reuters/title_index_with_weight.obj")
    r_query = rocchio(['oper', 'system'], ['operating', 'system'], rel_dict, newdict)
    query, expanded_values = expand_query(query, 'vsm')
    r_query = Counter(r_query)
    expanded_values = Counter(expanded_values)
    final_expanded = dict(r_query + expanded_values)
    repr = vsm(corpus, get_formatted_tokens(query), title, desc, final_expanded)
    if corpus == 1:
        corp = pd.read_csv("save_files/UO/corpus.csv", sep="|")
    else:
        corp = pd.read_csv("save_files/Reuters/corpus.csv", sep="|")
    result = corp.loc[ repr[0] , ["title", "description"]]
    result['score'] = repr[1]
    return result

if __name__ == "__main__":
    print(vector_controller('operating system', 'UOttawa'))
    # print(boolean_controller('(operating OR test) AND (system OR quality)', 'UOttawa'))