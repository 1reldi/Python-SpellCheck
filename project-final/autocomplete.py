import collections

from collections import Counter

#the so called "Hidden" step, thus allowing this module to be
#a "Hidden Markov Model"... Whatever that means...


alphabet = [
'a',
'b',
'c',
'd',
'dh',
'e',
'f',
'g',
'gj',
'h',
'i',
'j',
'k',
'l',
'll',
'm',
'n',
'nj',
'o',
'p',
'q',
'r',
'rr',
's',
'sh',
't',
'th',
'u',
'v',
'x',
'xh',
'y',
'z',
'zh'
]


NEARBY_KEYS = {
    'a': 'qwsz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'erfcxs',
    'e': 'rdsw',
    'f': 'rtgvcd',
    'g': 'tyhbvf',
    'h': 'yujnbg',
    'j': 'uikmnh',
    'k': 'iolmj',
    'l': 'opk',
    'm': 'njk',
    'n': 'bhjm',
    'o': 'iklp',
    'p': 'ol',
    'q': 'wa',
    'r': 'edft',
    's': 'wedxza',
    't': 'rfgy',
    'u': 'yhji',
    'v': 'cfgb',
    'w': 'qase',
    'x': 'zsdc',
    'y': 'tghu',
    'z': 'asx'
    }

def sugjero(first_word, second_word, top_n, WORD_TUPLES_MODEL):
    """given a word, return top n suggestions determined by the frequency of
    words prefixed by the input GIVEN the occurence of the last word"""
    try :
        # Hidden step
        possible_second_words =[second_word[:-1]+char
        for char in NEARBY_KEYS[second_word[-1]]
        if len(second_word) > 2]

        possible_second_words.append(second_word)

        probable_words = {w:c
        for w, c in
        WORD_TUPLES_MODEL[first_word.lower()].items()
        for sec_word in possible_second_words
        if w.startswith(sec_word)}

        return Counter(probable_words).most_common(top_n)
    except:
        #print second_word + " -1-> " + second_word[-1]
        return []
