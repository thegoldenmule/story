from kivy.app import App
import windows

class Story(App):
    def build(self):
        return windows.MainWindow()


if __name__ == '__main__':
    Story().run()