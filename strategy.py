import chunkers
import models

import nltk
from nltk.tag.simplify import simplify_wsj_tag
from nltk.corpus import conll2000


class ParseResults:
    def __init__(self, sentences, words, chunks):
        self.sentences = sentences
        self.words = words
        self.chunks = chunks
        self.success = (sentences is not None) and (words is not None) and (chunks is not None)

    def __repr__(self):
        return "ParseResults(success=%r)" % self.success


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
            return ParseResults(None, None, None)

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

    def resolve_entities(self, chunks):
        if chunks is None:
            return []

        # walk NP subtrees
        entities = []
        for np_tree in chunks.subtrees(lambda subtree: subtree.node == 'NP'):
            nns = [leaf for leaf in np_tree.leaves() if 'NN' in leaf[1]]

            if 0 != len(nns):
                entity = models.Entity(
                    nns[-1][0],
                    np_tree)
                entities.append(entity)

        return entities


class RelationExtractionStrategy:
    def __init__(self):
        pass