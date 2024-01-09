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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
import random

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Rectangle(source='background.jpg', pos=(0,0), size=(Window.width, Window.height))
            self.player = Rectangle(source='player.png', pos=(550, 20), size=(100,
            100))

class RocketApp(App):
    def build(self):
        return Game()

if __name__ == "__main__":
    RocketApp().run()