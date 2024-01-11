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
        self._keyboard = Window.request_keyboard(
        self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)
        with self.canvas:
            Rectangle(source='background.jpg', pos=(0,0), size=(Window.width, Window.height))
            self.player = Rectangle(source='player.png', pos=(550, 20), size=(100,
            100))
    
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None
    
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print('down', text)
        self.pressed_keys.add(text)
    
    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        print('up', text)

        if text in self.pressed_keys:
            self.pressed_keys.remove(text)

    def move_step(self, dt):
        cur_x = self.player.pos[0]
        cur_y = self.player.pos[1]
        step = 1000 * dt

        if 'a' in self.pressed_keys:
            cur_x -= step
        if 'd' in self.pressed_keys:
            cur_x += step
        self.player.pos = (cur_x, cur_y)

class Entity(object):
    def __init__(self):
        self._pos = (0, 0)
        self._size = (100, 100)
        self._source = "bullet.png"
        self._instruction = Rectangle(
            pos=self._pos, size=self._size, source=self._source)
        
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._instruction.pos = self._pos

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._instruction.size = self._size

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
        self._instruction.source = self._source

class Bullet(Entity):
    def __init__(self, pos, speed=500):
        super().__init__()
        # sound = SoundLoader.load("assets/bullet.wav")
        # sound.play()
        self._speed = speed
        self.pos = pos
        self.source = "bullet.png"
        game.bind(on_frame=self.move_step)
        
    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        # check for collision/out of bounds
        if self.pos[1] > Window.height:
            self.stop_callbacks()
            game.remove_entity(self)
            return
        for e in game.colliding_entities(self):
            if isinstance(e, Enemy):
                game.add_entity(Explosion(self.pos))
                self.stop_callbacks()
                game.remove_entity(self)
                e.stop_callbacks()
                game.remove_entity(e)
                game.score += 1
                return
        # move
        step_size = self._speed * dt
        new_x = self.pos[0]
        new_y = self.pos[1] + step_size
        self.pos = (new_x, new_y)

        
class RocketApp(App):
    def build(self):
        return Game()

if __name__ == "__main__":
    RocketApp().run()