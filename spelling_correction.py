from similarity.weighted_levenshtein import WeightedLevenshtein
from similarity.weighted_levenshtein import CharacterSubstitutionInterface
import pickle
import pandas as pd

#source for neighbors_of https://kth.diva-portal.org/smash/get/diva2:1116701/FULLTEXT01.pdf
neighbors_of = {}
# nw ne e se sw w
neighbors_of['q'] = [ 'w', 'a']
neighbors_of['w'] = [ 'e', 's', 'a', 'q']
neighbors_of['e'] = [ 'r', 'd', 's', 'w']
neighbors_of['r'] = [ 't', 'f', 'd', 'e']
neighbors_of['t'] = [ 'y', 'g', 'f', 'r']
neighbors_of['y'] = [ 'u', 'h', 'g', 't']
neighbors_of['u'] = [ 'i', 'j', 'h', 'y']
neighbors_of['i'] = [ 'o', 'k', 'j', 'u']
neighbors_of['o'] = [ 'p', 'l', 'k', 'i']
neighbors_of['p'] = [ 'l', 'o']
neighbors_of['a'] = ['q', 'w', 's', 'z']
neighbors_of['s'] = ['w', 'e', 'd', 'x', 'z', 'a']
neighbors_of['d'] = ['e', 'r', 'f', 'c', 'x', 's']
neighbors_of['f'] = ['r', 't', 'g', 'v', 'c', 'd']
neighbors_of['g'] = ['t', 'y', 'h', 'b', 'v', 'f']
neighbors_of['h'] = ['y', 'u', 'j', 'n', 'b', 'g']
neighbors_of['j'] = ['u', 'i', 'k', 'm', 'n', 'h']
neighbors_of['k'] = ['i', 'o', 'l', 'm', 'j']
neighbors_of['l'] = ['o', 'p', 'k']
neighbors_of['z'] = ['a', 's', 'x']
neighbors_of['x'] = ['s', 'd', 'c', 'z']
neighbors_of['c'] = ['d', 'f', 'v', 'x']
neighbors_of['v'] = ['f', 'g', 'b', 'c']
neighbors_of['b'] = ['g', 'h', 'n', 'v']
neighbors_of['n'] = ['h', 'j', 'm', 'b']
neighbors_of['m'] = ['j', 'k', 'n']

class CharacterSubstitution(CharacterSubstitutionInterface):
    def cost(self, c0, c1):
        if (c0 in 'aeiou') and (c1 in 'aeiou'):
            return 0.5
        elif (not(c0 in 'aeiou')) and (c1 in 'aeiou'):
            return 0.75
        elif not c0.isdigit():
            if c1 in neighbors_of[c0]:
                return 0.5
        return 1.0

def weighted_edit_distance(x, y):
    weighted_levenshtein = WeightedLevenshtein(CharacterSubstitution())
    if x[0] != y[0]:
        return weighted_levenshtein.distance(x, y) + 1
    return weighted_levenshtein.distance(x, y)

if __name__ == "__main__":
    df = pd.read_pickle("save_files/weighted_ed_df.pkl")
    df['ed'] = df.apply(lambda x: weighted_edit_distance('3242', x['word']), axis=1)
    df.nsmallest(5, 'ed')