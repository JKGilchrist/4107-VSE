import numpy as np
import pandas as pd
from collections import Counter

def rocchio(query, org_query, rel_dict, newdict):
    # Given query in array with pre-processing applied
    rocchio_dict = {}
    for rev_ids_lst in rel_dict[" ".join(org_query)]:
        for id in rev_ids_lst:
            for term in newdict[id]:
                rocchio_dict[term] = query.count(term) * 0.8
    frequency = 0
    for term in rocchio_dict.keys():
        for i in rel_dict[" ".join(org_query)][0]:
            if term in newdict[i]:
                frequency += 1
        rocchio_dict[term] = rocchio_dict[term] + (abs((frequency / len(rel_dict[" ".join(org_query)][0]))) * 0.3)
        frequency = 0
    frequency = 0
    for term in rocchio_dict.keys():
        for i in rel_dict[" ".join(org_query)][1]:
            if term in newdict[i]:
                frequency += 1
        rocchio_dict[term] = rocchio_dict[term] - ((frequency / len(rel_dict[" ".join(org_query)][1])) * 0.1)
        frequency = 0
    return (dict(Counter(rocchio_dict).most_common(5)))

if __name__ == "__main__":
    rel_dict = np.load('../relevant_dict.npy', allow_pickle='TRUE').item()
    newdict = np.load('complete_dict.npy', allow_pickle='TRUE').item()
    print(rocchio(['oper', 'system'], ['operating', 'system'], rel_dict, newdict))

