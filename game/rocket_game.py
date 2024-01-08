from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
import random

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class RocketApp(App):

    def build(self):
        return Game()

if __name__ == "__main__":
    RocketApp().run()