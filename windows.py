from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class NarrativeView(BoxLayout):

    def __init__(self, **kwargs):
        super(NarrativeView, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.colorComputer = '4444aa'
        self.colorUser = '44aa44'
        self.colorInputBG = '444444'

        self._output = Label(
            font_size='16sp',
            markup=True,
            size_hint=(1, .9),
            halign='left',
            valign='top'
        )
        self._output.text_size = (self._output.width, self._output.height)

        self._input = TextInput(
            font_size='16sp',
            size_hint=(1, .1),
            multiline=False,
            background_color=self.colorInputBG,
            focus=True
        )

        self.add_widget(self._output)
        self.add_widget(self._input)

        self._input.bind(on_text_validate=self.on_enter)
        self._input.bind(text=self.on_input_change)

        self.addComputerMessage('...Where am I?')

    def addUserMessage(self, message):
        self.addMessage(message, self.colorUser)

    def addComputerMessage(self, message):
        self.addMessage(message, self.colorComputer)

    def addMessage(self, message, color):
        self._output.text += '\n[color={}]{}[/color]'.format(color, message)

    def on_enter(self, instance):
        self.addUserMessage(instance.text)

        instance.text = ''
        instance.focus = True

    def on_input_change(self, instance, value):
        print 'Analyze ' + value


class ParseView(BoxLayout):
    def __init__(self, **kwargs):
        super(ParseView, self).__init__(**kwargs)

        self.orientation = 'vertical'

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.add_widget(NarrativeView())
        self.add_widget(ParseView())