#This step is where we transform "raw" data
# into some sort of probabilistic model(s)
import os

import re

import pickle

import collections

from collections import Counter


WORDS = []

WORD_TUPLES = []

WORDS_MODEL = {}

WORD_TUPLES_MODEL = {}

#http://norvig.com/spell-correct.html
def re_split(text): return re.findall('[a-z]+', text.lower())

#http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
#https://github.com/rrenaud/Gibberish-Detector/blob/master/gib_detect_train.py#L16
def chunks(l, n):
    for i in range(0, len(l) - n + 1):
        yield l[i:i+n]

def testo_modelet(corpus, model_name="modele_dinamike.pkl"):
    """Takes in a preferably long string (corpus/training data),
    split that string into a list, we \"chunkify\" resulting in
    a list of 2-elem list. Finally we create a dictionary,
    where each key = first elem and each value = Counter([second elems])

    Will save/pickle model by default ('modele_dinamike.pkl').
    Set second argument to false if you wish to not save the models.
    """

    # "preperation" step
    # word is in WORDS
    global WORDS
    WORDS = re_split(corpus)

    # first model -> P(word)
    global WORDS_MODEL
    WORDS_MODEL = collections.Counter(WORDS)

    # another preperation step
    # wordA, wordB are in WORDS
    global WORD_TUPLES
    WORD_TUPLES = list(chunks(WORDS, 2))

    # second model -> P(wordA|wordB)
    global WORD_TUPLES_MODEL
    WORD_TUPLES_MODEL = {first:collections.Counter()
                         for first, second in WORD_TUPLES}

    for tup in WORD_TUPLES:
        try:
            WORD_TUPLES_MODEL[tup[0]].update([tup[1]])
        except:
            # hack-y fix for uneven # of elements in WORD_TUPLES
            pass

    if model_name:
        ruaj_modelet(os.path.join(os.path.dirname(__file__), model_name))


def ruaj_modelet(path=None):
    """Save models to 'path'. If 'path' not specified,
    save to module's folder under name 'modele_dinamike.pkl'"""

    if path == None:
        path = os.path.join(os.path.dirname(__file__), 'modele_dinamike.pkl')

    print("saving to:", path)
    #save for next use. pickle format: (key=model name, value=model)
    pickle.dump({'words_model': WORDS_MODEL,
                 'word_tuples_model': WORD_TUPLES_MODEL},
                open(path, 'wb'),
                protocol=2)



def krijo_modelet():
    """unnecessary helper function for training against
    default corpus data (big.txt)"""

    bigtxtpath = os.path.join(os.path.dirname(__file__), 'dataSet.txt')
    with open(bigtxtpath, 'rb') as bigtxtfile:

        testo_modelet(str(bigtxtfile.read()))
        #return [WORDS_MODEL, WORD_TUPLES_MODEL]


def merr_modelet(load_path=None):
    """Load autocomplete's built-in model (uses Norvig's big.txt). Optionally
    provide the path to Python pickle object."""

    if load_path is None:
        load_path = os.path.join(os.path.dirname(__file__),
                                 'modele_dinamike.pkl')
    try:
        models = pickle.load(open(load_path,'rb'))

        global WORDS_MODEL
        WORDS_MODEL = models['words_model']

        global WORD_TUPLES_MODEL
        WORD_TUPLES_MODEL = models['word_tuples_model']

        print("U krijuan modelet")
    except:
       krijo_modelet()

    return [WORDS_MODEL, WORD_TUPLES_MODEL]
