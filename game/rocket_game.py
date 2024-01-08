from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

class Game(FloatLayout):
    pass

class RocketApp(App):

    def build(self):
        return Game()

if __name__ == "__main__":
    RocketApp().run()