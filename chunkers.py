import nltk


class ConsecutiveBayesNPChunkTagger(nltk.TaggerI):

    def __init__(self, train_sentences):
        train_set = []
        for tagged_sent in train_sentences:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = self.features(untagged_sent, i, history)
                train_set.append((featureset, tag))
                history.append(tag)
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

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


class ConsecutiveBayesNPChunker(nltk.ChunkParserI):

    def __init__(self, train_sentences):
        tagged_sentences = [
            [((word, tag), chunk) for (word, tag, chunk) in
                nltk.chunk.tree2conlltags(sent)]
            for sent in train_sentences]
        self.tagger = ConsecutiveBayesNPChunkTagger(tagged_sentences)

    def parse(self, sentence):
        tagged_sentences = self.tagger.tag(sentence)
        conll_tags = [(word, tag, chunk) for ((word, tag), chunk) in tagged_sentences]
        return nltk.chunk.util.conlltags2tree(conll_tags)


class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sentences):
        train_data = [[(tag, chunk) for word, tag, chunk in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sentences]
        self.tagger = nltk.UnigramTagger(train_data)

    def __repr__(self):
        return "UnigramChunker()"

    def parse(self, sentence):
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.util.conlltags2tree(conlltags)


class BigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sentences):
        train_data = [[(tag, chunk) for word, tag, chunk in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sentences]
        self.tagger = nltk.BigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.util.conlltags2tree(conlltags)