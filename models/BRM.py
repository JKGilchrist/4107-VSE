#Module 6

from models.wildcard_handler import get_bigrams
from string_formatting import get_formatted_tokens

import pickle
import pandas as pd

#TODO don't limit results

'''
Was expecting the linear time Posting Merge Sort algorithms for 'AND', 'OR', and 'AND_NOT'. Specifically, marks are docked for using for ... in ... loops which are less efficient
'''

class BRM:
    '''
    The Boolean Retrieval Model, after initializing, just give run_model a query and it will compute and return a list of relevant, unique ids
    '''

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
            #print(bigrams)
            for bigram in bigrams:

                try: #just in case it isn't there
                    #print(bigram, "IND", self.secondary_index[bigram])
                    terms += self.secondary_index[bigram]
                except:
                    continue
            terms = [t for t in terms if len(t) > 2] #filter
            x = pd.Series(terms).value_counts().tolist() #sorts by frequency
            y = pd.Series(terms).value_counts().index.tolist() #sorts by frequency

            ind = len(x) - x[::-1].index(x[0])
            
            terms = y[:ind]
        else:
            terms = [string]
        #ID retrievals
        ids = []
        
        for term in terms: 
            try:
                formatted = get_formatted_tokens(term)[0]
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
                            return merger(LHS, RHS, "or" )
                        
                        elif lst[i] == "AND":
                            return merger(LHS, RHS, "and" )

                        else: #AND_NOT
                            return merger(LHS, RHS, "and_not" )

                elif i == len(lst) - 1: #couldnt find middle, due to extra parentheses around entire query
                    excess_parentheses = True

            if excess_parentheses: #remove them, recall function
                return self.loop(lst[1:len(lst) - 1])

def merger(lst1,lst2, func):

    #both lists must be first sorted
    ###print("LHS pre-sort:", lst1)
    lst1 = merge_sort(lst1)
    ###print("LHS sorted:", lst1)
    ###print("RHS pre-sort:", lst2)
    lst2 = merge_sort(lst2)
    ###print("RHS sorted:", lst2)
    
    ans = []

    lst1_i = 0
    lst2_i = 0
    
    while lst1_i < len(lst1) or lst2_i < len(lst2):
        
        #If at both ends, no loop, no work to do

        if lst1_i < len(lst1) and lst2_i >= len(lst2):  #if not end(lst) and end(lst2)
            if func in ["or", "and_not"]:
                ans.append(lst1[lst1_i])
            lst1_i += 1
        
        elif lst1_i >= len(lst1) and lst2_i < len(lst2):  #if end(lst1) and ! end(lst2)
            if func in ["or"]:
                ans.append(lst2[lst2_i])
            lst2_i += 1

        elif lst1[lst1_i] == lst2[lst2_i]: #if lst1_value == lst2_value
            if func in ["or", "and"]:
                ans.append(lst1[lst1_i])
            lst1_i += 1
            lst2_i += 1
        
        elif lst1[lst1_i] < lst2[lst2_i] : #if lst1_value < lst2_value
            if func in ["or", "and_not"]:
                ans.append(lst1[lst1_i])
            lst1_i += 1

        else: # if lst1_value > lst2_value
            if func in ["or"]:
                ans.append(lst2[lst2_i])
            lst2_i += 1
        
    return ans

def merge_sort(lst):
    if len(lst) > 1:
        LHS = merge_sort(lst[0: (len(lst) // 2)])
        RHS = merge_sort(lst[(len(lst) // 2) :] )
        LHS_i = 0
        RHS_i = 0
        ans = []

        while LHS_i < len(LHS) or RHS_i < len(RHS):
            if LHS_i < len(LHS) and RHS_i >= len(RHS) or LHS_i < len(LHS) and LHS[LHS_i] <= RHS[RHS_i]  :
                ans.append(LHS[LHS_i])
                LHS_i += 1
            else:
                ans.append(RHS[RHS_i])
                RHS_i += 1
        return ans

    else:
        return lst
    

def test_BRM():
    test = BRM("./save_files/UO/descriptions_index.obj", "./save_files/UO/description_secondary_index.obj")
    #print (test.run_model("competition"))

    #print("\n\n")
    #print (test.run_model("competition OR computer"))
    print (test.run_model("enhances OR digital"))
    print (test.run_model("enhances AND digital"))
    print (test.run_model("enhances AND_NOT digital"))
    #print("\n\n")
    #print (test.run_model("operating AND (system OR platform)"))

if __name__ == "__main__":
    test_BRM()