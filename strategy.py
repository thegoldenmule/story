import nltk
from nltk.tag.simplify import simplify_wsj_tag
import chunkers
from nltk.corpus import conll2000


class ParseResults:
    def __init__(self, sentences, words, chunks):
        self.sentences = sentences
        self.words = words
        self.chunks = chunks


class Parser:
    simplify_tags = True

    def __init__(self):
        self.stemmer = nltk.PorterStemmer()
        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

        # todo: analyze more chunk types
        # possible chunk types:
        #       NP (noun phrase)
        #       VP (such as 'has already delivered')
        #       PP (such as 'because of')
        self.chunker = chunkers.UnigramChunker(conll2000.chunked_sents('train.txt', chunk_types=['NP']))

    # output:
    # ([sentence], [(word, stem, pos)], nltk.Tree)
    def parse(self, text):
        if not text:
            return [], [], None

        # first, tokenize words w/complex tags
        tokenized_words = nltk.pos_tag(nltk.word_tokenize(text))

        # grab sentences
        sentence_data = [sent for sent in self.sentence_tokenizer.tokenize(text)]

        # grab word data (word, stem, pos)
        word_data = [
            (word, self.stemmer.stem(word), (simplify_wsj_tag(pos) if self.simplify_tags else pos))
            for (word, pos)
            # todo: use default tagger for unknown words
            in tokenized_words]

        # parse chunks
        chunk_data = self.chunker.parse(tokenized_words)

        return ParseResults(sentence_data, word_data, chunk_data)


class EntityResolutionStrategy:
    def __init__(self):
        pass

    def resolve(self, taggedWords):
        return (word for (word, pos) in taggedWords if pos == 'NN')


class RelationExtractionStrategy:
    def __init__(self):
        pass