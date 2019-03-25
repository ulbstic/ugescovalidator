from time import sleep

import requests
import requests_cache

# Nominatim bloque les requêtes répétées
requests_cache.install_cache('nominatim_cache')

# entrer ceci dans la fonction ?
SESSION = requests.Session()

def get_nominatim(value, countrycodes=('BE',""), limit=20, lang="fr", s=SESSION) -> object:
    """
    :param value:
    :param countrycodes:
    :param limit:
    :param lang:
    :param s: session
    :return: a json file
    """
    # doc : https://wiki.openstreetmap.org/wiki/Nominatim
    url = 'http://nominatim.openstreetmap.org/'

    params = {'q': value,
              'format': 'jsonv2',
              'addressdetails': 1,
              'limit': limit,
              'email': 'ettorerizza@mail.com',
              'polygon_kml': 0,
              'extratags': 1,
              'namedetails': 0,
              # ajouter 'BE' et un country_code vide
              # dans le tuple simule
              # la préférence pour un pays de geopy
              # sans se limiter à celui-ci
              'countrycodes': countrycodes,
              'accept-language': lang
              }

    headers = {
        'User-Agent': 'Ugesco app',
        'From': 'ettorerizza@mail.com'
    }

    r = s.get( url, params=params, headers=headers, timeout=10 )
    result: object = r.json()

    # Nominatim bloque les requêtes trop rapides
    if r.from_cache == False:
        sleep( 1 )

    return result


if __name__ == '__main__':

    print(get_nominatim("Berlin")) #pourquoi ce résultat en Italie avec ypres grand-place ???
