# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup


def cvclass_to_qid(array):
    """ Turn computer vision classes into Wikidata qids"""
    with open( "../data/classes_places.json", "r", encoding="utf-8" ) as f:
        classes = json.load(f)
    try:
        qid_array = []
        for el in array:
            key = el.split( '/' )[0].lower().strip()
            qid_array.append( "wd:" + [i['wiki_id'] for i in classes if i['original_class'] == key][0] )
        return qid_array
    except (IndexError, TypeError) as e:
        print( 'no match' )


def get_lcs(array):
    """
    Get the Least common subsumers between several Wikidata qids in a list
    Return a Python list
    """
    array_string = ", ".join(array)
    query = {"query": """
    SELECT ?lcs ?lcsLabel WHERE {
    ?lcs ^wdt:P279* %s .
    filter not exists {
    ?sublcs ^wdt:P279* %s ;
          wdt:P279 ?lcs .
      }
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en " . } }""" % (array_string, array_string)
             }
    url = "https://query.wikidata.org/sparql"
    r = requests.get(url, params=query)
    soup = BeautifulSoup(r.text, "lxml")

    return [x.text for x in soup.find_all("literal")]


if __name__ == '__main__':

    array = ["synagogue/indoor", "mosque/outdoor",
             "church", "amphitheater"]

    list_of_qids = cvclass_to_qid( array )

    print( get_lcs( list_of_qids ) )
