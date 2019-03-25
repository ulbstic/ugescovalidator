# -*- coding: utf-8 -*-
import itertools
from typing import List

import numpy as np
import requests_cache
from sklearn.cluster import DBSCAN

from ugfunctions.clean_text import clean_entity, clean_caption
from ugfunctions.haversine import closest
from ugfunctions.json_to_df import get_json
from ugfunctions.nominatim import get_nominatim
from ugfunctions.spacy_locs import get_spacy_locs, get_ruler_locs
from ugfunctions.wikidata import get_wikidata

# Nominatim bloque les requêtes répétées
requests_cache.install_cache( 'nominatim_cache' )
requests_cache.install_cache( 'wikidata_cache' )


# On crée une classe pour les photos, ce sera plus net

class Picture:
    def __init__(self, ntuple):
        """
        :param picid: picture ID
        :param caption: legend
        :param spatial: spatial named entities tuple with type
        :param keywords: Pallas thesaurus
        :param group_descr: description of the picture's group
        """

        self.picid = ntuple.Index
        self.caption = clean_caption( ntuple.legend )
        self.keywords = ntuple.keyword
        self.group_descr = ntuple.bpallasf
        #self.extract_spatial = get_spacy_locs( self.caption ) + get_spacy_locs( self.group_descr )

        # effectuer assez d'opérations pour retrouver au moins une entité, sinon passer sans erreur
        # Pour le moment, on n'utilise spacy que si le nering de Hans ne donne aucun résultat
        if '__iter__' in dir( ntuple.spatial_list[0]):
            self.spatial = set( list( zip( *ntuple.spatial_list ) ) )
        else:
            self.spatial = get_ruler_locs( self.caption )
            if len(self.spatial) < 1:
                self.spatial = get_spacy_locs(self.caption)
                if len( self.spatial ) < 1:
                    self.spatial = []


    def __repr__(self):
        return f"beeldid: {self.picid}, legend: {self.caption}, ner_loc:{self.spatial}"

    @property
    def _spatial_list(self):
        return set( [clean_entity( x[0] ) for x in self.spatial] )  # + self.extract_spatial)

    @property
    def _spatial_combin(self):
        combin: List[str] = set([" ".join( x ) for x in list( itertools.combinations( self._spatial_list, 2 ) )])
        return combin

    def nominatim(self):
        """

        :return: json from Nominatim
        """
        result_combin = [x for xs in [get_nominatim(
            a ) for a in self._spatial_combin] for x in xs]

        if len( result_combin ) == 0:
            #print( "results from list" )
            result = [x for xs in [get_nominatim(
                a ) for a in self._spatial_list] for x in xs]
        else:
            #print( "resultats viennent de combin" )
            result = result_combin
        #print(self)
        if result:
            return result
        else:
            return "no nominatim"

    def cluster(self):
        """
        Find the centroid in a list of clustered Nominatim locations
        :return: a single json from Nominatim
        """

        result_nominatim = self.nominatim()
        try:
            coord = [(float( i['lat'] ), float( i['lon'] )) for i in result_nominatim]
        except:
            return None
        #print( "coord", coord )
        kms_per_radian = 6371.0088
        # Augmenter cette valeur augmente le nombre d'éléments dans un cluster et change les résultats
        epsilon = 2 / kms_per_radian
        # Adapter le nombre de clusters (min_sample) au nombre d'entités dans array ?
        db = DBSCAN( eps=epsilon, min_samples=1, algorithm='ball_tree',
                     metric='haversine' ).fit( np.radians( coord ) )
        cluster_labels = db.labels_
        #print( "cluster", cluster_labels )
        num_clusters = len( set( cluster_labels ) )
        #print( "num clusters", num_clusters )
        counts = np.bincount( cluster_labels )
        #print( "count", counts )
        maxi = np.argmax( counts )
        #print( "maxi", maxi )
        itemindex = np.where( cluster_labels == maxi )[0]
        #print( "itemindex", itemindex )

        lat: List[float] = [float( result_nominatim[index]['lat'] ) for index in itemindex]
        lon: List[float] = [float( result_nominatim[index]['lon'] ) for index in itemindex]

        # on récupère la moyenne des coordonnées du plus gros cluster. Cette moyenne équivaut au centroide :
        # https://gis.stackexchange.com/questions/12120/calculate-midpoint-from-a-series-of-latitude-and-longitude-coordinates

        average = {"lat": sum( lat ) / len( lat ), "lon": sum( lon ) / len( lon )}

        #print( list( zip( cluster_labels, [x['display_name'] for x in results] ) ) )
        #print( "plus proche de moyenne", closest( results, average ) )
        return closest( result_nominatim, average )


    def wikidata(self):
        """

        :return:
        """
        # notamment si le centroide a une ortho trop différente de la requête
        try:
            return [get_wikidata( x ) for x in self._spatial_list]
        except TypeError:
            print('no reliable match in Wikidata')


    def result(self):
        if len(self._spatial_list) == 1:

            return self.nominatim()[0]['display_name']

        else:

            return self.cluster()


if __name__ == "__main__":
    database = "../data/phototheque_pallas.tsv.gz"
    hans_json = "../data/fototheek-ner-processing-v3/ugc-ner-fr-photo-v3.json"

    data = get_json(hans_json, database)

    #print(data[1])

    p2 = Picture([item for item in data if item.Index == "00040179"][0])
    #print("extract spatial", p2.extract_spatial)
    print(p2)
    print( "picture spatial", p2.spatial )
    print( p2.caption )
    print( "spatial list", p2._spatial_list )

    # combin cause bcp de problèmes quand il y a du bruit, comme "Allemands" produit
    # par Spacy.
    # utiliser Wikidata d'abord ? Mais quid s'il ne reconnait pas un nom de lieu ?
    # on peut ne l'utiliser que sur Spacy
    print( "combin", p2._spatial_combin )


    print( "résultats", p2.result() )
    print( "cluster", p2.cluster()['display_name'] )

    # plutôt que le cluster, il faudrait  renvoyer le résultat Nominatim le plus proche de la requête concaténée
    # a savoir le 1er élément du display_name (avant la virgule) et la ville
    print("nominatim:", [i['display_name'] for i in p2.nominatim() ])

    #print( p2.wikidata() )
