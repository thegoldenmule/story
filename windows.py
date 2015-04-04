from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from pydispatch import dispatcher


class NarrativeView(BoxLayout):

    SIGNAL_TEXT_UPDATED = 'textUpdated'
    SIGNAL_TEXT_ENTERED = 'textEntered'

    output = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(NarrativeView, self).__init__(**kwargs)

    def on_enter(self, instance):
        dispatcher.send(signal=self.SIGNAL_TEXT_ENTERED, sender=self, text=instance.text)

        instance.text = ''

    def on_input_change(self, instance, value):
        dispatcher.send(signal=self.SIGNAL_TEXT_UPDATED, sender=self, text=value)


class ParseView(BoxLayout):

    content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ParseView, self).__init__(**kwargs)


class MemoryView(BoxLayout):

    content = ObjectProperty(None)

    def __init(self, **kwargs):
        super(MemoryView, self).__init__(**kwargs)


class MainWindow(BoxLayout):

    parseView = ObjectProperty(None)
    narrativeView = ObjectProperty(None)
    memoryView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)