from kivy.app import App
from pydispatch import dispatcher
import nltk
from nltk.corpus import conll2000

import windows
import models
import strategy
import chunkers


class StoryApp(App):

    unimportant_style = '[color=cccccc]{}[/color]'
    noun_style = '[b][color=33cc33]{}[/color][/b]'
    verb_style = '[color=0033ff]{}[/color]'
    adjective_style = '[color=3399ff]{}[/color]'
    adverb_style = '[color=ffff33]{}[/color]'

    style_table = {
        '('     : '[color=ff8000]{}[/color]',
        ')'     : '[color=ff8000]{}[/color]',
        'CNJ'   : unimportant_style,                          # conjunction - and, or, but, if, while, although
        'NUM'   : '[color=ff00cc]{}[/color]',                 # number - twenty-four, fourth, 1991, 14:24
        'DET'   : unimportant_style,                          # determiner - the, a, some, most, every, no
        'EX'    : unimportant_style,                          # existential - there, there's
        'FW'    : '[i][color=9900cc]{}[/color][/i]',          # foreign word - dolce, ersatz, esprit, quo, maitre
        'P'     : unimportant_style,                          # preposition - on, of, at, with, by, into, under
        'ADJ'   : adjective_style,                            # adjective - new, good, high, special, big, local
        'L'     : unimportant_style,                          # ?
        'MOD'   : unimportant_style,                          # modal verb - will, can, would, may, must, should
        'N'     : noun_style,                                 # noun - year, home, costs, time, education
        'NP'    : noun_style,                                 # proper noun - Alison, Africa, April, Washington
        'PRO'   : noun_style,                                 # pronoun - he, their, her, its, my, I, us
        'ADV'   : adverb_style,                               # adverb - really, already, still, early, now
        'S'     : unimportant_style,                          # ?
        'TO'    : unimportant_style,                          # the word to - to
        'UH'    : '[color=ff3300]{}[/color]',                 # interjection - ah, bang, ha, whee, hmpf, oops
        'V'     : verb_style,                                 # verb - is, has, get, do, make, see, run
        'VD'    : verb_style,                                 # past tense - said, took, told, made, asked
        'VG'    : verb_style,                                 # present participle - making, going, playing, working
        'VN'    : verb_style,                                 # past participle - given, taken, begun, sung
        'WH'    : unimportant_style                           # wh determiner - who, which, when, what, where, how
    }

    def __init__(self, **kwargs):
        super(StoryApp, self).__init__(**kwargs)

        self.model = models.Model()
        self.parser = strategy.Parser(
            stemmer=nltk.PorterStemmer(),
            sentence_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle'),

            # todo: analyze more chunk types
            # possible chunk types:
            #       NP (noun phrase)
            #       VP (such as 'has already delivered')
            #       PP (such as 'because of')
            chunker=chunkers.UnigramChunker(conll2000.chunked_sents('train.txt', chunk_types=['NP']))
        )
        self.entity_resolver = strategy.EntityResolutionStrategy()

        self.window = None

    def build(self):
        dispatcher.connect(
            self.on_text_change,
            signal=windows.NarrativeView.SIGNAL_TEXT_UPDATED,
            sender=dispatcher.Any
        )

        self.window = windows.MainWindow()

        return self.window

    def on_text_change(self, sender, text):
        # parse
        results = self.parser.parse(text)

        # resolve entities
        entities = self.entity_resolver.resolve_entities(results.chunks)

        # output
        if 0 == len(entities):
            self.window.parseView.content.text = ''
        else:
            # print all the entities we found
            text = '\n'.join((self.format(entity) for entity in entities))

            # then print the chunk trees
            text = text + '\n\n' + '\n\t'.join((chunk.pprint() for chunk in results.chunks))

            self.window.parseView.content.text = text

        pass

    # formats an entity for printing using the style table
    def format(self, entity):
        return '{} ({})'.format(
            self.style_for('N').format(entity.name),
            ','.join((self.style_for(pos).format(word) for (word, pos) in entity.chunk.leaves()))
        )

    def style_for(self, pos):
        if self.style_table.has_key(pos):
            return self.style_table[pos]
        return '{}'


if __name__ == '__main__':
    StoryApp().run()