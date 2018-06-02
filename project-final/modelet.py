#Ketu ne marrim te dhenat tekst dhe formojme modele statistikore
import os

import re

import pickle

import collections

FJALET = []

FJALET_TUPLE = []

FJALET_MODELE = {}

FJALET_MODELE_TUPLES = {}

def re_split(text): return re.findall('[a-z]+', text.lower())

def chunks(l, n):
    for i in range(0, len(l) - n + 1):
        yield l[i:i+n]

def testo_modelet(corpus, model_name="modele_dinamike.pkl"):
    """
    Merr nje string me shume karakter dhe e ndajme ate string ne nje liste, ndajme rezulatet ne nje liste 2 me dy element
    Ne fund krijojme nje dictionary cdo key eshte elementi pare dhe cdo value nje Counter me elementin e dyte

    Keto modele qe krijojme i ruajme ne nje pickle file 'modele_dinamike.pkl'
    """

    global FJALET
    FJALET = re_split(corpus)

    global FJALET_MODELE
    FJALET_MODELE = collections.Counter(FJALET)

    global FJALET_TUPLE
    FJALET_TUPLE = list(chunks(FJALET, 2))

    global FJALET_MODELE_TUPLES
    FJALET_MODELE_TUPLES = {first:collections.Counter()
                         for first, second in FJALET_TUPLE}

    for tup in FJALET_TUPLE:
        try:
            FJALET_MODELE_TUPLES[tup[0]].update([tup[1]])
        except:
            pass

    if model_name:
        ruaj_modelet(os.path.join(os.path.dirname(__file__), model_name))


def ruaj_modelet(path=None):
    """
    Ketu bejme ruajtjen e modeleve ne file picke, nese emri i file nuk eshte dhene, perdorim 'modele_dinamike.pkl'

    """

    if path == None:
        path = os.path.join(os.path.dirname(__file__), 'modele_dinamike.pkl')

    print("saving to:", path)

    pickle.dump({'words_model': FJALET_MODELE,
                 'word_tuples_model': FJALET_MODELE_TUPLES},
                open(path, 'wb'),
                protocol=2)



def krijo_modelet():
    """Ne rast se ndodh nje problem me marrjen e te dhenave nga file pickle therrasim kete funksion per te riprovuar te marrim te dhenat"""

    bigtxtpath = os.path.join(os.path.dirname(__file__), 'dataSet.txt')
    with open(bigtxtpath, 'rb') as bigtxtfile:

        testo_modelet(str(bigtxtfile.read()))


def merr_modelet(load_path=None):
    """Marrim modelet qe kemi ruajtur ne file"""

    if load_path is None:
        load_path = os.path.join(os.path.dirname(__file__),
                                 'modele_dinamike.pkl')
    try:
        models = pickle.load(open(load_path,'rb'))

        global FJALET_MODELE
        FJALET_MODELE = models['words_model']

        global FJALET_MODELE_TUPLES
        FJALET_MODELE_TUPLES = models['word_tuples_model']

        print("U krijuan modelet")
    except:
       krijo_modelet()

    return [FJALET_MODELE, FJALET_MODELE_TUPLES]
