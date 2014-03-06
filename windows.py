from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty


class NarrativeView(BoxLayout):
    _output = ObjectProperty(None)
    _input = ObjectProperty(None)

    colorComputer = '4444aa'
    colorUser = '44aa44'
    colorInputBG = '444444'

    def addUserMessage(self, message):
        self.addMessage(message, self.colorUser)

    def addComputerMessage(self, message):
        self.addMessage(message, self.colorComputer)

    def addMessage(self, message, color):
        self._output.text += '\n[color={}]{}[/color]'.format(color, message)

    def on_enter(self, instance):
        print "enter"
        self.addUserMessage(instance.text)

        instance.text = ''
        instance.focus = True

    def on_input_change(self, instance, value):
        print 'Analyze ' + value


class ParseView(BoxLayout):
    _content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ParseView, self).__init__(**kwargs)


class MainWindow(BoxLayout):
    _narrativeView = ObjectProperty(None)
    _parseView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
