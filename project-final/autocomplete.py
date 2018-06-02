import collections

from collections import Counter


alfabeti = [
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

#Kur jepet nje fjale, rikthen mundesit e mundshme duke u bazuar ne shpeshtesine e fjales dhe mbi mundesine e fjales se ardhshme
def parashiko_fjale(fjala, shkronja, top_n, WORD_TUPLES_MODEL):
    try :
        fjalet_e_mundshme = {w:c
        for w, c in
        WORD_TUPLES_MODEL[fjala.lower()].items() #Vendosim fjalet e mundshme dhe nje numer qe tregon mundesine qe ka ajo fjale te jet fjala pasardhese
        if w.startswith(shkronja)}

        return Counter(fjalet_e_mundshme).most_common(top_n)
    except:
        return []

#Per cdo shkronje te alfabetit ne gjejme mundesite e ndryshme se cila mund te jete fjala tjeter qe nis me ate germe
def sugjero(fjala, WORD_TUPLES_MODEL):
    rezultate = []
    for shkronje in alfabeti:
        rezultate = rezultate + parashiko_fjale(fjala, shkronje, 10, WORD_TUPLES_MODEL)
    return rezultate
