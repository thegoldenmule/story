from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from pydispatch import dispatcher


class NarrativeView(BoxLayout):

    def __init__(self, **kwargs):
        super(NarrativeView, self).__init__(**kwargs)

        output = ObjectProperty(None)
        input = ObjectProperty(None)

    def on_enter(self, instance):
        dispatcher.send(signal=self.SIGNAL_TEXT_VALIDATE, sender=self, instance.text)

    def on_input_change(self, instance, value):
        dispatcher.send(signal=self.SIGNAL_TEXT_VALIDATE, sender=self, instance.text)


class ParseView(BoxLayout):

    def __init__(self, **kwargs):
        super(ParseView, self).__init__(**kwargs)

        self.content = ObjectProperty(None)


class MemoryView(BoxLayout):

    def __init(self, **kwargs):
        super(MemoryView, self).__init__(**kwargs)

        self.content = ObjectProperty(None)


class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        narrativeView = ObjectProperty(None)
        parseView = ObjectProperty(None)
        memoryView = ObjectProperty(None)