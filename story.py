from kivy.app import App
from pydispatch import dispatcher

import windows
import models
import strategy


class StoryApp(App):

    # TODO: use simplified tags!
    color_table = {
        'NN' : '008800',
        'NNP' : '006600',

        'DT' : '066004',
        'PRP' : '556600',
        'VBD' : '888888',
        'VBZ' : 'AAAAAA',
        'VBG' : 'AA2222',
        'POS' : '77AAFF',
        'CC' : '7777FF',
        'RB' : '66AA66'
    }

    def __init__(self, **kwargs):
        super(StoryApp, self).__init__(**kwargs)

        self.model = models.Model()
        self.parser = strategy.Parser()
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
        sentence_data, word_data = self.parser.parse(text)

        self.window.parseView.content.text = " ".join(
            ('[color={}]{} ({})[/color]'.format(self.color_for(pos), word, pos)
             for (word, stem, pos) in word_data))
        pass

    def color_for(self, pos):
        if self.color_table.has_key(pos):
            return self.color_table[pos]
        return 'CCCCCC';


if __name__ == '__main__':
    StoryApp().run()