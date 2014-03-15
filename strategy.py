import models

import nltk
from nltk.tag.simplify import simplify_wsj_tag


class ParseResults:
    def __init__(self, sentences, words, chunks):
        # list of sentences
        # ['You suffered a meltdown.', 'Then the giraffe blew up.']
        self.sentences = sentences

        # list of list of (word, stem, pos) [one list for each sentence]
        # [
        #   [('You', 'NN'), ..],
        #   [('Then', 'P'), ..],
        #   ..
        # ]
        self.words = words

        # list of chunk trees, one for each sentence
        # [nltk.Tree(...), nltk.Tree(...), ...]
        self.chunks = chunks

        # successful parsing
        self.success = (sentences is not None) and (words is not None) and (chunks is not None)

    def __repr__(self):
        return "ParseResults(sentences=%r, words=%r, chunks=%r)" % (self.sentences, self.words, self.chunks)


class Parser:
    simplify_tags = True

    def __init__(self, stemmer, sentence_tokenizer, chunker):
        self.stemmer = stemmer
        self.sentence_tokenizer = sentence_tokenizer
        self.chunker = chunker

    def __repr__(self):
        return "Parser(stemmer=%r, sentence_tokenizer=%r, chunker=%r", (self.stemmer, self.sentence_tokenizer, self.chunker)

    def parse(self, text):
        if not text:
            return ParseResults(None, None, None)

        # tokenize sentences
        sentence_data = [sent for sent in self.sentence_tokenizer.tokenize(text)]

        # first, tokenize words w/complex tags per sentence
        tokenized_sentences = [nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentence_data]

        # grab word data [[(word, stem, pos)]], i.e. a list of lists of (word, stem, pos), one list for
        # each sentence
        word_data = [[
            (word, self.stemmer.stem(word), (simplify_wsj_tag(pos) if self.simplify_tags else pos))
            for (word, pos)
            # todo: use default tagger for unknown words
            in sentence] for sentence in tokenized_sentences]

        # parse chunks
        # todo: bug: chunker needs to parse each tokenized sentence!
        chunk_data = [self.chunker.parse(tokenized_sentence) for tokenized_sentence in tokenized_sentences]

        return ParseResults(sentence_data, word_data, chunk_data)


# todo: map PRPs (pronouns) to corresponding noun
class EntityResolutionStrategy:
    def __init__(self):
        pass

    def __repr__(self):
        return "EntityResolutionStrategy()"

    def resolve_entities(self, chunks):
        if chunks is None:
            return []

        # walk NP subtrees for each chunk tree
        entities = []
        for chunk in chunks:
            for np_tree in chunk.subtrees(lambda subtree: subtree.node == 'NP'):
                # pick out only nouns
                nns = [leaf for leaf in np_tree.leaves() if 'NN' in leaf[1]]

                # if there are nouns in this subtree, create an entity
                if 0 != len(nns):
                    entity = models.Entity(
                        # use the last noun in the NP subtree
                        nns[-1][0],
                        np_tree)
                    entities.append(entity)

        return entities


class RelationExtractionStrategy:
    def __init__(self):
        pass