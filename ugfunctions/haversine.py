from math import cos, asin, sqrt


def closest(data, v):
    def distance(lat1, lon1, lat2, lon2):
        """Formule d'Harvesine pour trouver, dans une liste de dictionnaires lat-lon,
        le point le plus proche d'un point de référence"""
        p = 0.017453292519943295
        a = 0.5 - cos( (lat2 - lat1) * p ) / 2 + cos( lat1 * p ) * \
            cos( lat2 * p ) * (1 - cos( (lon2 - lon1) * p )) / 2
        return 12742 * asin( sqrt( a ) )

    return min( data, key=lambda p: distance( float( v['lat'] ),
                                              float( v['lon'] ),
                                              float( p['lat'] ),
                                              float( p['lon'] ) )
                )


if __name__ == '__main__':
    tempDataList = [{'id': 1, 'lat': 39.7612992, 'lon': -86.1519681},
                    {'id': 2, 'lat': 39.762241, 'lon': -86.158436},
                    {'id': 3, 'lat': 39.7622292, 'lon': -86.1578917}]

    v = {'id': 4, 'lat': 39.7622290, 'lon': -86.1519750}

    print( closest( tempDataList, v ) )
