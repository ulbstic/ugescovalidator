import re
import string
from unidecode import unidecode

PUNCTUATION = re.compile( '[%s]' % re.escape( string.punctuation ) )

def clean_caption(text):
    """
    Remove brackets with photographer names or locations at the end of some captions
    :param text: a photo caption
    :return: text cleaned
    """
    text = str(text)
    text = re.sub(r'\s*\[.+?\]$', '.', text)
    text = re.sub(r'\s*\(photo.+?\)', '', text)
    return re.sub(r'-- --.+', '.', text).strip()


def clean_entity(entity):
    """
    Remove definite article from named entities
    :param entity: a named entity extracted by Hans
    :return: the same without "le, la, le..."
    """
    entity = str(entity)
    regex = r"^\b(le|la|l\s+'|l'|les)\b\s*"

    # You can manually specify the number of replacements by changing the 4th argument
    return re.sub( regex, "", entity, 0, re.MULTILINE | re.IGNORECASE )


class Fingerprinter(object):
    '''
    Python implementation of Google Refine fingerprinting algorithm described here:
    https://github.com/OpenRefine/OpenRefine/wiki/Clustering-In-Depth
    Requires the unidecode module: https://github.com/iki/unidecode
    '''

    def __init__(self, string):
        self.string = self._preprocess(string)

    def _preprocess(self, string):
        '''
        Strip leading and trailing whitespace, lowercase the string, remove all punctuation,
        in that order.
        '''
        return PUNCTUATION.sub('', string.strip().lower())

    def _latinize(self, string):
        '''
        Replaces unicode characters with closest Latin equivalent. For example,
        Alejandro González Iñárritu becomes Alejando Gonzalez Inarritu.
        '''
        return unidecode(string)

    def _unique_preserving_order(self, seq):
        '''
        Returns unique tokens in a list, preserving order. Fastest version found in this
        exercise: http://www.peterbe.com/plog/uniqifiers-benchmark
        '''
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def get_fingerprint_nonsorted(self):
        '''
        Gets non sorted fingerpint that remove isolated letters
        '''
        result = self._latinize(' '.join(
            self._unique_preserving_order(
                self.string.split()

            )
        ))

        return re.sub(r'\b\w{1}\b', '', result)

    def get_fingerprint(self):
        '''
        Gets conventional fingerpint.
        '''
        return self._latinize(' '.join(
            self._unique_preserving_order(
                sorted(self.string.split())
            )
        ))

    def get_ngram_fingerprint(self, n=1):
        '''
        Gets ngram fingerpint based on n-length shingles of the string.
        Default is 1.
        '''
        return self._latinize(''.join(
            self._unique_preserving_order(
                sorted([self.string[i:i + n]
                        for i in range(len(self.string) - n + 1)])
            )
        ))


if __name__ == '__main__':
    print(clean_entity("La cathédrale"))

    print(clean_caption("""(photo: albert) Charle Michel à Bruxelles [photo Sipho]"""))

    f = Fingerprinter("hôtel de ville de Bruxelles à bruxelles")
    print(f.get_fingerprint())

    print(f.get_fingerprint_nonsorted())