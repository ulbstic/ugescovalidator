# -*- coding: utf-8 -*-

import json
import pandas as pd
from pandas.io.json import json_normalize


def get_json(nerfile, database):
    """
    Convert Hans JSON to a list of tuple and join with Pallas
    :param file: Json from Nering
    :return: a list of namedtuples
    """
    database = pd.read_csv( database,
                            sep="\t",
                            compression="infer",
                            encoding="utf-8",
                            dtype={'beeldid': str, 'trfwnumm': str},
                            error_bad_lines=True)

    with open( nerfile, "r", encoding="utf8" ) as file:
        data = json.load( file )

    df = json_normalize( data, sep="_" ).dropna( axis='columns', how='all' )

    # Check the beeldid zero-padding
    df['beeldid'] = df["beeldid"].apply( lambda x: x.zfill( 8 ) )

    df = pd.merge( df, database, how='left', on=['beeldid'] )

    df.set_index( "beeldid", drop=True, append=False, inplace=True, verify_integrity=False )

    # What's wrong here with zip()? I'm stuck. TODO : find a solution
    df['spatial_list'] = list(zip( df.spatial_value, df.spatial_key ) )

    list_of_tuples = [row for row in df.itertuples()]

    return list_of_tuples


if __name__ == '__main__':
    test = get_json(
        r"../data/fototheek-ner-processing-v3/ugc-ner-fr-photo-v3.json", r"../data/phototheque_pallas.tsv.gz" )

    print(test)

    print(list(zip(*test[4].spatial_list)))
