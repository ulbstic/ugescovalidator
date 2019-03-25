import requests


def wikipedia_to_wikidata(wikilink):
    """get the Wikidata QID from a full Wikipedia URL"""

    url = "https://tools.wmflabs.org/openrefine-wikidata/en/api?" + "query=" + wikilink

    r = requests.get( url )

    return r.json()['result'][0]['id']


if __name__ == '__main__':
    print( wikipedia_to_wikidata( "https://en.wikipedia.org/wiki/Charles_Michel" ) )
    print( wikipedia_to_wikidata( "https://fr.wikipedia.org/wiki/%C3%89tats-Unis" ) )
