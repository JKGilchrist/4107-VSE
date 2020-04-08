import nltk
from nltk.corpus import wordnet


def expand_query(query, model):
    if model == "boolean":
        if "(" in query:
            query = query.replace("(", " ( ")
        if ")" in query:
            query = query.replace(")", " ) ")

        lst = query.split()
        synonyms = []
        # based off of code from https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
        for i in range(len(lst)):
            if lst[i] not in ['AND', 'OR', 'AND_NOT', ')', '(']:
                for syn in wordnet.synsets(lst[i]):
                    for l in syn.lemmas():
                        synonyms.append(l.name())
                synonyms = list(dict.fromkeys(synonyms))
                synonyms = synonyms[0:5]
                lst[i] = "(" + " OR ".join(synonyms) + ")"
                synonyms = []
        print(" ".join(lst))
        return " ".join(lst)

if __name__ == "__main__":
    expand_query("operating AND system", "boolean")