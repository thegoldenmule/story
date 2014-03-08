from kivy.app import App
from pydispatch import dispatcher

import windows
import models
import strategy


class StoryApp(App):

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

        #self.window.parseView.content.text = " ".join((word for (word, stem, pos) in word_data))
        pass


if __name__ == '__main__':
    StoryApp().run()