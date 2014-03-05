import nltk
from nltk import *
from nltk.corpus import wordnet as wn
from textwrap import *

class Model:
    def __init__(self):
        self.words = []
        self.sents = []
        self.raw = ''

        self._stemmer = nltk.PorterStemmer()
        self._sentTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

        # this is probably not the best way to do things
        wn.synsets('init')

    def processInput(self, str):
        print ''

        newSents = [self.prepSent(sent) for sent in self._sentTokenizer.tokenize(str)]
        newWords = [self.prepWord(word) for word in nltk.word_tokenize(str)]

        self.sents = self.sents + newSents
        self.words = self.words + newWords
        self.raw = self.raw + str

        print self.generateResponse(str, newSents, newWords)

        print ''

    def generateResponse(self, newRaw, newSents, newWords):
        return [wn.synsets(word) for word in newWords]

    def prepWord(self, word):
        tokens = self._stemmer.stem(word.lower())

        # Another normalization task involves identifying non-standard words
        # including numbers, abbreviations, and dates, and mapping any such
        # tokens to a special vocabulary. For example, every decimal number
        # could be mapped to a single token 0.0, and every acronym could be
        # mapped to AAA. This keeps the vocabulary small and improves the
        # accuracy of many language modeling tasks.
        return tokens

    def prepSent(self, sent):
        return sent.lower()

model = Model()

print ''
print '...where am I?'
print ''

# main loop
while True:
    input = raw_input(">")

    if 'exit' == input:
        break

    model.processInput(input)