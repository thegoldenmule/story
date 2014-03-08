from kivy.app import App
from pydispatch import dispatcher

import windows
import models
import strategy


class StoryApp(App):

    def __init__(self, **kwargs):
        super(StoryApp, self).__init__(**kwargs)

        self.model = models.Model()
        self.window = None


    def build(self):
        dispatcher.connect(
            self.on_textchange,
            signal=windows.NarrativeView.SIGNAL_TEXT_UPDATED,
            sender=dispatcher.Any
        )

        window = windows.MainWindow()

        return window

    def on_textchange(self, sender, text):
        print text


if __name__ == '__main__':
    StoryApp().run()