import nltk
from nltk.corpus import wordnet
from string_formatting import get_formatted_tokens

def expand_query(query, model):
    if model == "boolean":
        if "(" in query:
            query = query.replace("(", " ( ")
        if ")" in query:
            query = query.replace(")", " ) ")

        lst = query.split()
        synonyms = []
        new_syn = []
        # based off of code from https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
        for i in range(len(lst)):
            if lst[i] not in ['AND', 'OR', 'AND_NOT', ')', '(']:
                for syn in wordnet.synsets(lst[i]):
                    for l in syn.lemmas():
                        synonyms.append(l.name())
                synonyms = list(dict.fromkeys(synonyms))
                for j in range(len(synonyms)):
                    if "_" not in synonyms[j]:
                        new_syn.append(synonyms[j])
                new_syn = new_syn[:5]
                lst[i] = create_term(new_syn[1:], new_syn[0])
                new_syn = []
                synonyms = []
        print(" ".join(lst))
        return " ".join(lst)
    if model == "vsm":
        lst = query.split()
        values = {}
        for i in range(len(lst)):
            values[lst[i]] = 1
        synonyms = []
        new_syn = []
        # based off of code from https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
        for i in range(len(lst)):
            for syn in wordnet.synsets(lst[i]):
                for l in syn.lemmas():
                    if l.name() != lst[i]:
                        synonyms.append(l.name())
            synonyms = list(dict.fromkeys(synonyms))
            for j in range(len(synonyms)):
                if "_" not in synonyms[j]:
                    new_syn.append(synonyms[j])
            new_syn = new_syn[:5]
            weight = 1/len(new_syn)
            if weight == 1:
                weight = 0.8
            for j in range(len(new_syn)):
                values["".join(get_formatted_tokens(new_syn[j]))] = weight
                lst.append(new_syn[j])
            new_syn = []
            synonyms = []
        return " ".join(lst), values

def create_term(syn_lst, str):
    if len(syn_lst) == 0:
        return ""
    if len(syn_lst) == 1:
        return "(" + syn_lst[0] + " OR " + str + ")"
    return create_term(syn_lst[1:], "(" + syn_lst[0] + " OR " + str + ")")

if __name__ == "__main__":
    print(expand_query("operating science", "vsm"))
