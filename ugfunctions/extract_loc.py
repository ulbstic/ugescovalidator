# -*- coding: utf-8 -*-
"""
@author: ettore
"""
import re
from pandas import read_table, read_csv
from unidecode import unidecode

# TODO : relative path
def get_poi(text):
    geo = read_csv( r"/Users/ettorerizza/Documents/GitHub/UGESCO/data/streets_and_poi.tsv",
                   encoding="utf-8", sep = "\t" )
    streets = set( [unidecode( str( name ).strip().lower().replace( '-', ' ' ) ) for name in geo.lowercase] )

    CHARS = "abcdefghijklmnopqrstuvwxyzéëèàäâçüûùABCDEFGHIJKLMNOPQRSTUVWXYZ-' "
    valeurs = "".join(
        unidecode( c.lower().replace( "' ", "'" ).replace( '-', ' ' ) ) for c in str( text ) if c in CHARS ).strip()
    valeurs = re.sub( r"\s+", " ", valeurs )
    liste = set()

    for tokens in streets:
        if tokens in valeurs:
            liste.add( tokens )
    # pour conserver l'élément le plus grand en cas de chevauchement des noms de rues
    if len( liste ) > 1 and min( liste, key=len ) in max( liste, key=len ):
        liste.remove( min( liste, key=len ) )

    return [(i, "poi") for i in liste]

# TODO : relative path
def get_localities(value):
    # Note : éliminer les noms de lieux qui sont également des noms communs, comme "membre"
    geo = read_csv(r"/Users/ettorerizza/Documents/GitHub/UGESCO/data/communes_et_sections.tsv",
                   encoding="utf-8", sep = "\t")
    lieux = set( [str( name ).strip().lower() for name in geo['nom']] )
    liste = []
    CHARS = "abcdefghijklmnopqrstuvwxyzéëèàäâçüûùABCDEFGHIJKLMNOPQRSTUVWXYZ- "
    valeurs = "".join( unidecode( c.lower().replace( "-", " " ) )
                       for c in str( value ) if c in CHARS ).strip()
    valeurs = re.sub( r"\s+", " ", valeurs ).split( ' ' )

    for i, tokens in enumerate( valeurs ):
        try:
            if tokens in lieux:
                tokens = tokens
            if tokens + " " + valeurs[i + 1] in lieux:
                tokens = tokens + " " + valeurs[i + 1]
            if tokens + "-" + valeurs[i + 1] in lieux:
                tokens = tokens + "-" + valeurs[i + 1]
            if tokens + "-" + valeurs[i + 1] + "-" + valeurs[i + 2] in lieux:
                tokens = tokens + "-" + valeurs[i + 1] + "-" + valeurs[i + 2]
            if tokens + " " + valeurs[i + 1] + " " + valeurs[i + 2] in lieux:
                tokens = tokens + " " + valeurs[i + 1] + " " + valeurs[i + 2]
            if tokens + " " + valeurs[i + 1] + " " + valeurs[i + 2] + valeurs[i + 3] in lieux:
                tokens = tokens + " " + \
                         valeurs[i + 1] + " " + valeurs[i + 2] + + valeurs[i + 3]
            if tokens + " " + valeurs[i + 1] + " " + valeurs[i + 2] + valeurs[i + 3] in lieux:
                tokens = tokens + "-" + \
                         valeurs[i + 1] + "-" + valeurs[i + 2] + valeurs[i + 3]
        except IndexError:
            pass
        if tokens in lieux:
            liste.append( tokens.title() )
        for i, tokens in enumerate( liste ):
            try:
                if liste[i + 1] in liste[i]:
                    del liste[i + 1]
            except IndexError:
                pass

    liste = set( liste )
    return [(i.title(), "locality") for i in liste]

def get_poi_localities(value):
    return get_poi(value) + get_localities(value)


if __name__ == '__main__':
    text = """En passant par la rue du Tilleul, à forchies-la-marche, j'ai vu quelqu'un regarder vers la place Royale"""

    print( get_poi( text ) )
    print( get_localities( text ) )
    print(get_poi_localities(text))
