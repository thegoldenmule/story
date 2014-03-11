import chunkers
from nltk.corpus import conll2000


# Tests a chunking strategy by training and evaluating against conll data
class ChunkStrategyTester():

    def __init__(self):
        self.test_sentences = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
        self.train_sentences = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

    def test(self, chunk_factory):
        chunker = chunk_factory(self.train_sentences)
        print chunker.evaluate(self.test_sentences)


harness = ChunkStrategyTester()
print ''

print 'Unigram:'
harness.test(lambda train: chunkers.UnigramChunker(train))
print ''

print 'Bigram:'
harness.test(lambda train: chunkers.BigramChunker(train))
print ''

print 'Consecutive Bayes:'
harness.test(lambda train: chunkers.ConsecutiveBayesNPChunker(train))
print ''