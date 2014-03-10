import nltk
from nltk.tag.simplify import simplify_wsj_tag
from nltk.corpus import conll2000


class Parser:
    def __init__(self):
        self.stemmer = nltk.PorterStemmer()
        self.sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    # output:
    # ([sentence], [(word, stem, pos)])
    def parse(self, text):
        if not text:
            return [], []

        sentence_data = [sent for sent in self.sentence_tokenizer.tokenize(text)]
        word_data = [
            (word, self.stemmer.stem(word), simplify_wsj_tag(pos))
            for (word, pos)
            # todo: use default tagger for unknown words
            in nltk.pos_tag(nltk.word_tokenize(text))]

        return sentence_data, word_data


class EntityResolutionStrategy:
    def __init__(self):
        pass

    def resolve(self, taggedWords):
        return (word for (word, pos) in taggedWords if pos == 'NN')


class ConsecutiveNPChunkTagger(nltk.TaggerI):

    def __init__(self, train_sentences):
        train_set = []
        for tagged_sent in train_sentences:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = self.features(untagged_sent, i, history)
                train_set.append((featureset, tag))
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train(
            train_set,
            algorithm='megam',
            trace=0)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = self.features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

    def features(self, sentence, i, history):
        word, pos = sentence[i]
        if i == 0:
            prevword, prevpos = "<START>", "<START>"
        else:
            prevword, prevpos = sentence[i-1]

        if i == len(sentence)-1:
            nextword, nextpos = "<END>", "<END>"
        else:
            nextword, nextpos = sentence[i+1]

        return {"pos": pos,
            "word": word,
            "prevpos": prevpos,
            "nextpos": nextpos,
            "prevpos+pos": "%s+%s" % (prevpos, pos),
            "pos+nextpos": "%s+%s" % (pos, nextpos),
            "tags-since-dt": self.tags_since_dt(sentence, i)}

    def tags_since_dt(self, sentence, i):
        tags = set()

        for word, pos in sentence[:i]:
            if pos == 'DT':
                tags = set()
            else:
                tags.add(pos)

        return '+'.join(sorted(tags))


class ConsecutiveNPChunker(nltk.ChunkParserI):

    def __init__(self, train_sentences):
        tagged_sentences = [
            [((word, tag), chunk) for (word, tag, chunk) in
                nltk.chunk.tree2conlltags(sent)]
            for sent in train_sentences]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sentences)

    def parse(self, sentence):
        tagged_sentences = self.tagger.tag(sentence)
        conll_tags = [(word, tag, chunk) for ((word, tag), chunk) in tagged_sentences]
        return nltk.chunk.conlltags2tree(conll_tags)


# Tests a chunking strategy by training and evaluating against conll data
class ChunkStrategyTester():

    def __init__(self):
        self.test_sentences = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
        self.train_sentences = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

    def test(self, chunk_factory):
        chunker = chunk_factory(self.train_sentences)
        print chunker.evaluate(self.test_sentences)