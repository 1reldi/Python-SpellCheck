from Tkinter import *

# First create application class
"""AUTOCOMPLETE -
This file contains the process where we train our predictive models, Also
helpful are the load_models and save_models functions.
"""
# -*- coding: utf-8 -*-


import os

import collections

import pickle

import re

from collections import Counter

import time

import extremeRead

#the so called "Hidden" step, thus allowing this module to be
#a "Hidden Markov Model"... Whatever that means...
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


WORDS = []

WORD_TUPLES = []

WORDS_MODEL = {}

WORD_TUPLES_MODEL = {}

def norm_rsplit(text,n): return text.lower().rsplit(' ', n)[-n:]

#http://norvig.com/spell-correct.html
def re_split(text): return re.findall('[a-z]+', text.lower())

#http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
#https://github.com/rrenaud/Gibberish-Detector/blob/master/gib_detect_train.py#L16
def chunks(l, n):
    for i in range(0, len(l) - n + 1):
        yield l[i:i+n]

#This step is where we transform "raw" data
# into some sort of probabilistic model(s)
def train_models(corpus, model_name="models_compressed.pkl"):
    """Takes in a preferably long string (corpus/training data),
    split that string into a list, we \"chunkify\" resulting in
    a list of 2-elem list. Finally we create a dictionary,
    where each key = first elem and each value = Counter([second elems])

    Will save/pickle model by default ('models_compressed.pkl').
    Set second argument to false if you wish to not save the models.
    """

    # "preperation" step
    # word is in WORDS
    print("start preperation step " + time.asctime())
    global WORDS
    WORDS = re_split(corpus)
    print("end preperation step " + time.asctime())

    # first model -> P(word)
    print("start first model -> P(word) " + time.asctime())
    global WORDS_MODEL
    WORDS_MODEL = collections.Counter(WORDS)
    print("end first model -> P(word) " + time.asctime())

    # another preperation step
    # wordA, wordB are in WORDS
    print("start wordA, wordB are in WORDS " + time.asctime())
    global WORD_TUPLES
    WORD_TUPLES = list(chunks(WORDS, 2))
    print("end wordA, wordB are in WORDS " + time.asctime())

    # second model -> P(wordA|wordB)
    print("start second model -> P(wordA|wordB) " + time.asctime())
    global WORD_TUPLES_MODEL
    WORD_TUPLES_MODEL = {first:collections.Counter()
                         for first, second in WORD_TUPLES}
    print("end second model -> P(wordA|wordB) " + time.asctime())

    for tup in WORD_TUPLES:
        try:
            WORD_TUPLES_MODEL[tup[0]].update([tup[1]])
        except:
            # hack-y fix for uneven # of elements in WORD_TUPLES
            pass

    if model_name:
        save_models(os.path.join(os.path.dirname(__file__), model_name))


def train_bigtxt():
    """unnecessary helper function for training against
    default corpus data (big.txt)"""
##
##    bigtxtpath = os.path.join(os.path.dirname(__file__), 'corpus1.txt') #big hope
##    with open(bigtxtpath, 'rb') as bigtxtfile:
##
##        train_models(str(bigtxtfile.read()))
    with extremeRead.File('corpus1.txt') as f:
        text = ""
        print("start reading file " + time.asctime())
        for row in f.backward():
            #text.append(row.lower())
            text += row
        print("end reading file " + time.asctime())
        train_models(text)

def save_models(path=None):
    """Save models to 'path'. If 'path' not specified,
    save to module's folder under name 'models_compressed.pkl'"""

    if path == None:
        path = os.path.join(os.path.dirname(__file__), 'models_compressed.pkl')

    print("saving to:", path)
    #save for next use. pickle format: (key=model name, value=model)
    pickle.dump({'words_model': WORDS_MODEL,
                 'word_tuples_model': WORD_TUPLES_MODEL},
                open(path, 'wb'),
                protocol=2)


def load_models(load_path=None):
    """Load autocomplete's built-in model (uses Norvig's big.txt). Optionally
    provide the path to Python pickle object."""

    if load_path is None:
        load_path = os.path.join(os.path.dirname(__file__),
                                 'models_compressed.pkl')
    try:
        models = pickle.load(open(load_path,'rb'))

        global WORDS_MODEL
        WORDS_MODEL = models['words_model']

        global WORD_TUPLES_MODEL
        WORD_TUPLES_MODEL = models['word_tuples_model']

        print("U krijuan modelet")
    except IOError:
        print("Error in opening pickle object. Training on default corpus text.")
        train_bigtxt()
    except KeyError:
        print("Error in loading both predictve models.\
              Training on default corpus text.")
        train_bigtxt()
    except ValueError:
        print("Corrupted pickle string.\
              Training on default corpus text (big.txt)")
        train_bigtxt()

def this_word(word, top_n=10):
    """given an incomplete word, return top n suggestions based off
    frequency of words prefixed by said input word"""
    try:
        return [(k, v) for k, v in WORDS_MODEL.most_common()
                if k.startswith(word)][:top_n]
    except KeyError:
        raise Exception("Please load predictive models. Run:\
                        \n\tautocomplete.load()")


predict_currword = this_word


def this_word_given_last(first_word, second_word, top_n=10):
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

def print_results(results):
    for result in results[0:10]:
        print (result[0])


#time1 = time.asctime()
#print("start loading dataset " + time1)

#load_models()
#this_word_given_last("ti", "j") + this_word_given_last("ti", "a")

#time2 = time.asctime()
#print("finish loading dataset " + time2)

##while True:
##    print ""
##    name = raw_input("Shkruaj fjalen: ")
##    results = []
##    for letter in alphabet:
##        results = results + this_word_given_last(name, letter)
##
##    results = sorted(results, key=lambda res: res[1])[::-1]  # sort by age
##    results = filter(lambda x: not (x[0] in alphabet), results)
##    print_results(results)


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.create_widgets()
        load_models()

    # Create main GUI window
    def create_widgets(self):
        self.search_var = StringVar()
        #self.search_var.trace("w", self.update_list)
        self.entry = Entry(self, textvariable=self.search_var, width=50)
        self.button = Button(self, text="Sugjero", background="#009688", foreground="white", command=self.update_list)
        self.lbox = Listbox(self, width=45, height=15)

        self.entry.grid(row=0, column=0, padx=10, pady=3)
        self.button.grid(row=0, column=1, padx=10, pady=3)
        self.lbox.grid(row=1, column=0, padx=10, pady=3)

        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self, *args):
        name = self.search_var.get()
        results = []
        for letter in alphabet:
            results = results + this_word_given_last(name, letter)

        results = sorted(results, key=lambda res: res[1])[::-1]
        results = filter(lambda x: not (x[0] in alphabet), results)

        self.lbox.delete(0, END)

        for item in results:
            self.lbox.insert(END, item[0])


root = Tk()
root.title('Sugjero fjalen')
app = Application(master=root)
print ('Starting mainloop()')
app.mainloop()
