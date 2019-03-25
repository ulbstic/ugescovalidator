# -*- coding: utf-8 -*-

import spacy
from spacy.pipeline import EntityRuler

# from langdetect import detect
from ugfunctions.clean_text import clean_caption


# la version multilingue xx ne marche pas très bien avec des entités composées du type "Forchies-la-Marche"
def get_spacy_locs(text):
    # lang = detect( text ) # ralentit pas mal l'execution

    # do not forget to install the language packages fr, nl, en, xx (and fr_core_news_sm ?)
    # if (lang == 'nl' or lang == 'en' or lang == 'fr'):
    #     nlp = spacy.load( lang )
    # # elif lang == 'fr':
    # #     nlp = spacy.load( 'fr_core_news_sm' )
    # else:
    #     nlp = spacy.load( 'xx' )
    nlp = spacy.load( 'fr' )

    # Load current language tokenizer, tagger, parser, NER and word vectors
    text_cleaned = clean_caption(text)
    doc = nlp( text_cleaned )

    # Find named entities, phrases and concepts
    # liste_spacy = [" ".join( x ) for x in list(
    #     itertools.combinations(
    #         [entity.text for entity in doc.ents if entity.label_ == "LOC"] , 2 ) )]

    liste_spacy = [(entity.text, entity.label_) for entity in doc.ents if entity.label_ == "LOC"]

    #return [get_wikidata( x ) for x in liste_spacy]

    return liste_spacy


def patternizer(value):
  return [{"lower":i.lower()} for i in value.strip().split(' ')]

# TODO : relative paths
# TODO : clean poi gazeeter (street numbers remain)
with open(r"/Users/ettorerizza/Documents/GitHub/UGESCO/data/streets_and_poi.tsv") as poi:
  poi_list = [{"label": "poi_be", "pattern":patternizer(x)} for x in poi.readlines()]

with open(r"/Users/ettorerizza/Documents/GitHub/UGESCO/data/countries.tsv") as countries:
  countries_list = [{"label": "countries", "pattern":patternizer(x)} for x in countries.readlines()]

with open(r"/Users/ettorerizza/Documents/GitHub/UGESCO/data/communes_et_sections.tsv") as localities:
  localities_list = [{"label": "localities_be", "pattern":patternizer(x)} for x in localities.readlines()]

nlp = spacy.load("fr_core_news_sm")

ruler = EntityRuler(nlp, overwrite_ents=True)

ruler.add_patterns(poi_list)
ruler.add_patterns(countries_list)
ruler.add_patterns(localities_list)

nlp.add_pipe(ruler)


def get_ruler_locs(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ["localities_be", "countries", "poi_be"]]


# ruler.to_disk( "./patterns.jsonl" )

if __name__ == '__main__':
    text = """Parti de la rue de la Loi, il s'est rendu à Ans et à Mont-saint-Guibert, puis en ex-Yougoslavie"""
    print( text, "\n\n", get_ruler_locs( text ))

    texte = """Tempête sur la mer du Nord. Par tous les temps, nos malles traversent le Channel. 
    Photo: La mer déchaînée pendant une traversée du "Prins Albert", dont le pont est incliné à 45°."""

    print( get_spacy_locs( texte) )
    print(get_ruler_locs( texte ))

    print(clean_caption(texte))
