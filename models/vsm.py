import pandas as pd
from scipy.spatial.distance import cosine
import numpy as np

def vsm(collection, query, title, desc, expanded_values):
    '''
    Returns a list of the ids of the 10 most similar documents using the vsm model
    '''
    # create query df
    values = []
    query_no_duplicates = []
    for i in range(len(query)):
        if query[i] not in query_no_duplicates:
            query_no_duplicates.append(query[i])
            values.append(0)
        values[query_no_duplicates.index(query[i])] = values[query_no_duplicates.index(query[i])] + 1
    query_df = pd.DataFrame([values], columns=query_no_duplicates)

    # create title df
    index = []
    values = []
    for k, v in title.items():
        if k in query_no_duplicates:
            v= list(v)
            for i in range(len(v)):
                if v[i][0] not in index:
                    index.append(v[i][0])
                    values.append([0] * len(query_no_duplicates))
                values[index.index(v[i][0])][query_no_duplicates.index(k)] = v[i][1]
    title_df = pd.DataFrame(values, index=index, columns=query_no_duplicates)


    # create desc df
    index = []
    values = []
    for k, v in desc.items():
        if k in query_no_duplicates:
            v = list(v)
            for i in range(len(v)):
                if v[i][0] not in index:
                    index.append(v[i][0])
                    values.append([0] * len(query_no_duplicates))
                values[index.index(v[i][0])][query_no_duplicates.index(k)] = v[i][1]
    desc_df = pd.DataFrame(values, index=index, columns=query_no_duplicates)

    tf_idf = ((2/3) * title_df).append((1/3) * desc_df)
    tf_idf = tf_idf.groupby(tf_idf.index).sum()
    tf_idf['cosine'] = tf_idf.apply(lambda row: np.dot(row, query_df.iloc[0]), axis=1)
    tf_idf = tf_idf.nlargest(10, 'cosine')
    tf_idf['cosine'] = tf_idf['cosine'].round(2)
    result = []
    result.append(tf_idf.index.values)
    result.append(tf_idf['cosine'].to_list())
    return result


if __name__ == "__main__":
    desc = pd.read_pickle("../save_files/UO/descriptions_index_with_weight.obj")
    title = pd.read_pickle("../save_files/UO/title_index_with_weight.obj")
    query = ['operting', 'system']
    print(vsm("UofO", query, title, desc, {'operating': 1, 'system': 1}))