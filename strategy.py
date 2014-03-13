import nltk
from nltk.tag.simplify import simplify_wsj_tag
import chunkers
from nltk.corpus import conll2000


class Parser:
    def __init__(self):
        self.stemmer = nltk.PorterStemmer()
        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

        # todo: analyze more chunk types
        self.chunker = chunkers.UnigramChunker(conll2000.chunked_sents('train.txt', chunk_types=['NP']))

    # output:
    # ([sentence], [(word, stem, pos)], nltk.Tree)
    def parse(self, text):
        if not text:
            return [], [], None

        sentence_data = [sent for sent in self.sentence_tokenizer.tokenize(text)]
        word_data = [
            (word, self.stemmer.stem(word), simplify_wsj_tag(pos))
            for (word, pos)
            # todo: use default tagger for unknown words
            in nltk.pos_tag(nltk.word_tokenize(text))]

        # possible chunk types: NP (noun phrase), VP (such as 'has already delivered') and PP (such as 'because of')
        chunk_data = self.chunker.parse([(word, pos) for (word, stem, pos) in word_data])

        return sentence_data, word_data, chunk_data


class EntityResolutionStrategy:
    def __init__(self):
        pass

    def resolve(self, taggedWords):
        return (word for (word, pos) in taggedWords if pos == 'NN')