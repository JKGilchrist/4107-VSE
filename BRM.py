#Module 6

from wildcard_handler import get_bigrams
from string_formatting import get_formatted_tokens

import pickle

class BRM:

    def __init__ (self, primary_index_path, *secondary_index_path):
        '''
        Sets up the model, connecting it to the relevant indices
        '''
        with open(primary_index_path, 'rb') as f: #open file
            self.primary_index = pickle.load(f)

        if secondary_index_path:
            with open(secondary_index_path[0], 'rb') as f:
                self.secondary_index = pickle.load(f)
    
    def run_model(self, query):
        '''
        Main input, takes a query as a string. Returns a list of document ids containing that match the query, based on the boolean retrieval model
        '''
        if "(" in query:
            query = query.replace("(", " ( ")
        if ")" in query:
            query = query.replace(")", " ) ")
        
        lst = query.split()
        
        return self.loop(lst) #inherently won't have duplicates

    def lookup(self, string):
        '''
        Returns the ids that match the given string. Handles both strings with wildcards and regular strings, first tokenizing then using the index get the ids
        '''
        #Formatting
        terms = []
        if "*" in string:
            bigrams = get_bigrams(string)
            for bigram in bigrams:
                try: #just in case it isn't there
                    terms += self.secondary_index[bigram]
                except:
                    continue
        else:
            terms = [string]
        
        #ID retrievals
        ids = []
        for term in terms:
            formatted = get_formatted_tokens(term)[0]
            try:
                ids += self.primary_index[formatted]
            except:
                continue

        return ids
        
    def loop(self, lst):
        '''
        Recursive function for handling the query formatting, to retrieve the results of each individual term and then merge the results based on the key word used.
        Ultimately returns a list of unique, relevant document ids
        '''
        if len(lst) == 1:
            return self.lookup(lst[0])
            #get values
        else:
            excess_parentheses = False

            for i in range(len(lst)):
                if lst[i] == "AND" or lst[i] == "OR" or lst[i] == "AND_NOT":
                    
                    before_start = lst[:i].count("(")
                    before_end = lst[:i].count(")")
                    after_start = lst[i:].count("(")
                    after_end = lst[i:].count(")")

                    if before_start == before_end and after_start == after_end: # found the middle
                        LHS = []
                        RHS =  []

                        if i == 1: #single element by itself
                            LHS = self.loop(lst[:i])
                        else: #something wrapped in ()
                            LHS = self.loop(lst[1:i- 1])
                            
                        if i+2 == len(lst): #single element
                            RHS = self.loop(lst[i+1:])
                        else:
                            RHS = self.loop(lst[i+2 : len(lst) - 1])
                        
                        if lst[i] == "OR":
                            return list( set(LHS) | set(RHS) )
                        elif lst[i] == "AND":
                            return [i for i in LHS if i in  RHS]
                        else: #AND_NOT
                            return [i for i in LHS if i not in  RHS]
                            
                elif i == len(lst) - 1: #couldnt find middle, due to extra parentheses around entire query
                    excess_parentheses = True

            if excess_parentheses: #remove them
                return self.loop(lst[1:len(lst) - 1])

if __name__ == "__main__":
    test = BRM("save_files/description_index.obj", "save_files/description_secondary_index.obj")
    print (test.run_model("4* OR competition"))

    print("\n\n\n")
    print (test.run_model("competition OR computer"))
    #print("\n\n\n")
    #breakdown("((x AND (x OR y)) OR (c AND d))")