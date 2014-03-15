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

# Another normalization task involves identifying non-standard words
# including numbers, abbreviations, and dates, and mapping any such
# tokens to a special vocabulary. For example, every decimal number
# could be mapped to a single token 0.0, and every acronym could be
# mapped to AAA. This keeps the vocabulary small and improves the
# accuracy of many language modeling tasks.


class EntityRelation:
    def __init__(self, a, b, relation):
        self.a = a
        self.b = b
        self.relation = relation

    def __repr__(self):
        return "EntityRelation(a=%r, b=%r, relation=%r)" % (self.a, self.b, self.relation)


class Entity:
    def __init__(self, name, chunk):
        self.name = name
        self.chunk = chunk
        self.relations = []

    def __repr__(self):
        return "Entity(name=%r, chunk=%r)" % (self.name, self.chunk)


class Model:

    def __init__(self):
        self.tagged_words = []
        self.sentences = []
        self.raw = ''
        self.entities = []

    def __repr__(self):
        return "Model()"