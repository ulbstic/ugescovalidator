
import random
from tabulate import tabulate
import pandas as pd

from ugfunctions.get_results import *

# Apply get_results() on a random sample of 1000 pics


def sample_df(df, size=1000):
    """
    Take as input a dataframe and return a random sample of (size) rows
    :param df:
    :param size: the sample size
    :return: a (1000, 16) dataframe
    """
    return df.sample( 1000 )

def sample_list(liste, k=1000):
    """
    Take as input a list of tuples and return a random sample of (size)
    in a dataframe shape.
    :param liste: alist of tuples
    :param size: the sample size
    :return: a  dataframe
    """
    return random.sample(liste, k)
    #return pd.DataFrame( list( sample ) )


database = "../data/phototheque_pallas.tsv.gz"
hans_json = "../data/fototheek-ner-processing-v3/ugc-ner-fr-photo-v3.json"

data = get_json( hans_json, database )

sample_10 = sample_list(data, 10)

# sample_100_spatial = []
# # TODO : Deviendra inutile quand j'aurai réglé le prob dans get_json
# for i in sample_100.spatial_list:
#     try:
#         sample_100_spatial.append(i[0])
#     except ValueError:
#         sample_100_spatial.append("null")
#
# sample_100['spatial'] = pd.DataFrame({'spatial': sample_100_spatial})

my_list = []

for _ in sample_10:
    my_list.append( Picture(_) )

print(my_list)

for i in my_list:
    print("beeldid:", i.picid)
    print("caption:", i.caption, "spatial:", i.spatial, "result:", i.result())









