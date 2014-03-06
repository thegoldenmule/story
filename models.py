import nltk

#ADJ	adjective           new, good, high, special, big, local
#ADV	adverb              really, already, still, early, now
#CNJ	conjunction         and, or, but, if, while, although
#DET	determiner          the, a, some, most, every, no
#EX	    existential         there, there's
#FW	    foreign word        dolce, ersatz, esprit, quo, maitre
#MOD	modal verb          will, can, would, may, must, should
#N	    noun                year, home, costs, time, education
#NP	    proper noun         Alison, Africa, April, Washington
#NUM	number              twenty-four, fourth, 1991, 14:24
#PRO	pronoun             he, their, her, its, my, I, us
#P	    preposition         on, of, at, with, by, into, under
#TO	    the word to         to
#UH	    interjection        ah, bang, ha, whee, hmpf, oops
#V	    verb                is, has, get, do, make, see, run
#VD	    past tense          said, took, told, made, asked
#VG	    present participle  making, going, playing, working
#VN	    past participle     given, taken, begun, sung
#WH	wh  determiner          who, which, when, what, where, how

class Model:
    def __init__(self):
        self.taggedWords = []
        self.sents = []
        self.raw = ''

        self._stemmer = nltk.PorterStemmer()
        self._sentTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def processInput(self, str):
        print ''

        newSents = [self.prepSent(sent) for sent in self._sentTokenizer.tokenize(str)]
        newTaggedWords = [self.prepWord((word, pos)) for (word, pos) in nltk.pos_tag(nltk.word_tokenize(str))]

        self.sents = self.sents + newSents
        self.taggedWords = self.taggedWords + newTaggedWords
        self.raw = self.raw + str

        print self.generateResponse(str, newSents, newTaggedWords)

        print ''

    def generateResponse(self, newRaw, newSents, newTaggedWords):
        return ['{0} => {1}'.format(word, tag) for (word, tag) in newTaggedWords]

    def prepWord(self, (word, tag)):
        taggedTokens = (self._stemmer.stem(word.lower()), tag)

        # Another normalization task involves identifying non-standard words
        # including numbers, abbreviations, and dates, and mapping any such
        # tokens to a special vocabulary. For example, every decimal number
        # could be mapped to a single token 0.0, and every acronym could be
        # mapped to AAA. This keeps the vocabulary small and improves the
        # accuracy of many language modeling tasks.
        return taggedTokens

    def prepSent(self, sent):
        return sent.lower()