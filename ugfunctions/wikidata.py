# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 12:35:54 2018

@author: ettor
"""

import pandas as pd
import requests
import requests_cache
from collections import namedtuple

import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


def get_wikidata_item(predicat, objet):
    """
    Use the WDQ service to get items by property and object.
    Return a panda dataframe with the items and their english label.
    Can be slow or raise timeout
    """
    sparql = SPARQLWrapper( "https://query.wikidata.org/sparql" )

    sparql.setQuery( """
    SELECT ?item ?itemLabel
    WHERE
    {
        ?item wdt:%s wd:%s .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    }
    """ % (predicat, objet) )

    sparql.setReturnFormat( JSON )
    results = sparql.query().convert()

    results_df = pd.io.json.json_normalize( results['results']['bindings'] )
    return results_df[['item.value', 'itemLabel.value']]


def get_wikidata(value, type_id='Q618123', prop_id='P17', prop_value='Q31', lang="en"):
    """
  Use the Antonin's API to return the best match on Wikidata based on the type and a property.

  Example : get_wikidata('Binche', 'Q618123', 'P17', 'Q31')
  Which means : search the label "Binche" instance of geographical object (Q618123)
  in country (P17) Belgium (Q31)
  The result is a tuple (main_type, match, name, qid, score)
  Result : ('municipality of Belgium', False, 'Binche', 'Q95121', 100.0)
  """
    Wikidata = namedtuple( 'Wikidata', 'qid label confidence match type' )

    base_url = "https://tools.wmflabs.org/openrefine-wikidata/%s/api" % (lang)

    query = {"query": """{"query":"%s",
                      "limit":0,
                      "type" : "%s"}""" % (value, type_id)}

    if prop_id or prop_value:
        query = {"query": """{"query":"%s",
                      "limit":0,
                      "type" : "%s",
                      "properties":[{"pid":"%s",
                      "v":{"id":"%s"}}]}""" % (value, type_id, prop_id, prop_value)}

    r = requests.get( base_url, params=query )

    # print(r.url)

    json_result = r.json()

    try:
        qid = [d['id'] for d in json_result['result']]
        name = [d['name'] for d in json_result['result']]
        score = [d['score'] for d in json_result['result']]
        match = [d['match'] for d in json_result['result']]
        main_type = [d['type'][0]['name'] for d in json_result['result']]

        df = pd.DataFrame( {'qid': qid,
                            'name': name,
                            'score': score,
                            'match': match,
                            'main_type': main_type
                            } )

        # order by score
        df.sort_values( ['score'], ascending=[False], inplace=True )
        print( df.head() )

        # select the best match
        matches = df.query( "score == 100" ).values
        print( "matches:", matches )

        if matches.size > 0:
            best_match = tuple( matches )
            print( "best match1:", best_match )
        else:
            best_match = list( tuple, df.iloc[[0]].values )
            print( "best match2:", best_match )

        return {Wikidata( *x ) for x in [x for x in best_match]}

    except IndexError:
        print( "No exact match in Wikidata" )
        return json_result


    # add the location of each result using the data extension API
def get_location():
    pass


if __name__ == '__main__':

    print(get_wikidata('Binche', 'Q618123', 'P31', 'Q15273785', "fr"))
    print(get_wikidata('Binche', 'Q618123'))

    print(get_wikidata('camp de beverloo', 'Q618123'))

    print(get_wikidata("Boulevard Anspach",''))

    liste = ["Namur", "rue du Moulin"]

    print( [get_wikidata( x ) for x in liste] )


    # get instances of building (slow)
    print(get_wikidata_item('P31', 'Q41176'))



