from kivy.app import App

import windows
import models

class StoryApp(App):
    def build(self):
        return windows.MainWindow()


if __name__ == '__main__':
    StoryApp().run()