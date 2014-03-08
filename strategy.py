import nltk


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
        word_data = [(word, self.stemmer.stem(word), pos) for (word, pos) in nltk.pos_tag(nltk.word_tokenize(text))]

        return sentence_data, word_data


class NounResolutionStrategy:
    def __init__(self):
        pass

    def resolve(self, taggedWords):
        # TODO: use simplified tags
        return (word for (word, pos) in taggedWords if pos == 'NN')