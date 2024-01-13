from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import CoreLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.label import CoreLabel
import random

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=self._update_size)
        
        self._end_game_label = Label(
            text="",
            font_size=50,
            halign='center',
            valign='middle'
        )

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self._score_label = CoreLabel(text="Score: 0",font_size=35)
        self._score_label.refresh()
        self._score = 0
        
        self._time_label = CoreLabel(text="Time: 01:00", font_size=35)
        self._time_label.refresh()
        self._time_remaining = 60
        
        self.how_to_play_label = CoreLabel(text="How to Play\n\nMove: A/D keys\nShoot: Spacebar\n",
                font_size=25,)
        self.how_to_play_label.refresh()
        
        self.register_event_type("on_frame")
        
        with self.canvas:
            self._background = Rectangle(source="img/background.jpg", pos=(0, 0),
                    size=(Window.width, Window.height))
            self._score_instruction = Rectangle(texture=self._score_label.texture, 
                    pos=(0, Window.height - 50), size=self._score_label.texture.size)
            
            self._time_instruction = Rectangle(texture=self._time_label.texture, 
                    pos=(Window.width - 200, Window.height - 50), size=self._time_label.texture.size)
            
            self.how_to_play_instruction = Rectangle(
                texture=self.how_to_play_label.texture,
                pos=((Window.width - self.how_to_play_label.texture.size[0]) / 2,(Window.height - self.how_to_play_label.texture.size[1] - 25))
                , size=self.how_to_play_label.texture.size)


            self._end_game_instruction = Rectangle(pos=(0, 0), size=(0, 0))

        self.keysPressed = set()
        self._entities = set()

        Clock.schedule_interval(self._on_frame, 0)

        self.sound = SoundLoader.load("sound/bg_song.mp3")
        self.sound.play()

        Clock.schedule_interval(self.spawn_enemies, 5)
        
        Clock.schedule_interval(self.spawn_coins, 10)
        
        Clock.schedule_interval(self._update_time, 1)
        
    def _update_size(self, instance, value):
        self._score_instruction.pos = (0, self.height - 50)
        self._score_instruction.size = self._score_label.texture.size
        
        self._background.pos = (0, 0)
        self._background.size = (self.width, self.height)  
        
        self._time_instruction.pos = (Window.width - 200, Window.height - 50)
        self._time_instruction.size = self._time_label.texture.size

        self.how_to_play_instruction.pos = ((Window.width - self.how_to_play_label.texture.size[0]) / 2, 
                                (Window.height - self.how_to_play_label.texture.size[1] - 25)) 
        self.how_to_play_instruction.size = self.how_to_play_label.size

    def spawn_enemies(self, dt):
        for i in range(3):
            random_x = random.randint(0, Window.width - 100)
            y = Window.height
            random_speed = random.randint(60, 100)
            self.add_entity(Enemy((random_x, y), random_speed))
    
    def spawn_coins(self, dt):    
        for i in range(1):
            random_x = random.randint(0, Window.width - 100)
            y = Window.height
            random_speed = random.randint(50, 70)
            self.add_entity(Coin((random_x, y)))

    def _on_frame(self, dt):
        self.dispatch("on_frame", dt)

    def on_frame(self, dt):
        pass

    def _update_time(self, dt):
        self._time_remaining -= 1
        minutes = self._time_remaining // 60
        seconds = self._time_remaining % 60
        self._time_label.text = f"Time: {minutes:02d}:{seconds:02d}"
        self._time_label.refresh()
        self._time_instruction.texture = self._time_label.texture
        self._time_instruction.size = self._time_label.texture.size

        if self._time_remaining <= 0:
            self._end_game()
    
    def _end_game(self):
        Clock.unschedule(self._update_time)
        message_label = CoreLabel(text=f"Time Out!\nScore: {self.score}", font_size=50)
        message_label.refresh()

        with self.canvas:
            self.message_instruction = Rectangle(
                texture=message_label.texture,
                pos=(Window.width / 2 - message_label.texture.size[0] / 2,
                    Window.height / 2 - message_label.texture.size[1] / 2),
                size=message_label.texture.size
            )
        popup = GameOverPopup()
        popup.open()

    def store_score(self, player_name):
        print(f"Player: {player_name}, Score: {self.score}")

        Clock.schedule_once(self._exit_app, 3)  

    def _exit_app(self, dt):
        App.get_running_app().stop()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self._score_label.text = "Score: " + str(value)
        self._score_label.refresh()
        self._score_instruction.texture = self._score_label.texture
        self._score_instruction.size = self._score_label.texture.size

    def add_entity(self, entity):
        self._entities.add(entity)
        self.canvas.add(entity._instruction)

    def remove_entity(self, entity):
        if entity in self._entities:
            self._entities.remove(entity)
            self.canvas.remove(entity._instruction)


    def collides(self, e1, e2):
        r1x = e1.pos[0]
        r1y = e1.pos[1]
        r2x = e2.pos[0]
        r2y = e2.pos[1]
        r1w = e1.size[0]
        r1h = e1.size[1]
        r2w = e2.size[0]
        r2h = e2.size[1]

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else:
            return False
        
    def colliding_entities(self, entity):
        result = set()
        for e in self._entities:
            if self.collides(e, entity) and e != entity:
                result.add(e)
        return result

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

class Entity(object):
    def __init__(self):
        self._pos = (0, 0)
        self._size = (100, 100)
        self._source = "img/bullet.png"
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
        sound = SoundLoader.load("sound/bullet_sound.mp3")
        sound.play()
        self._speed = speed
        self.pos = pos
        self.source = "img/bullet.png"
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
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
            
            elif isinstance(e, Coin): 
                game.add_entity(Explosion(self.pos))
                self.stop_callbacks()
                game.remove_entity(self)
                e.stop_callbacks() 
                game.remove_entity(e)
                game.score += 2  
                return

        step_size = self._speed * dt
        new_x = self.pos[0]
        new_y = self.pos[1] + step_size
        self.pos = (new_x, new_y)

        step_size = self._speed * dt
        new_x = self.pos[0]
        new_y = self.pos[1] + step_size
        self.pos = (new_x, new_y)


class Enemy(Entity):
    def __init__(self, pos, speed=100):
        super().__init__()
        self._speed = speed
        self.pos = pos
        self.source = "img/enemy.png"
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):

        if self.pos[1] < 0:
            self.stop_callbacks()
            game.remove_entity(self)
            game.score -= 1
            return
        for e in game.colliding_entities(self):
            if e == game.player:
                game.add_entity(Explosion(self.pos))
                self.stop_callbacks()
                game.remove_entity(self)
                game.score -= 1
                return

        step_size = self._speed * dt
        new_x = self.pos[0]
        new_y = self.pos[1] - step_size
        self.pos = (new_x, new_y)


class Explosion(Entity):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        sound = SoundLoader.load("sound/bomb.mp3")
        self.source = "img/explode.png"
        sound.play()
        Clock.schedule_once(self._remove_me, 0.1)

    def _remove_me(self, dt):
        game.remove_entity(self)


done = False

class Coin(Entity):
    def __init__(self, pos, speed=200):
        super().__init__()
        self._speed = speed
        self.pos = pos
        self.source = "img/coin.png"
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        if self.pos[1] < 0:
            self.stop_callbacks()
            game.remove_entity(self)
            return

        for e in game.colliding_entities(self):
            if e == game.player:
                game.add_entity(Explosion(self.pos))
                self.stop_callbacks()
                game.remove_entity(self)
                game.score += 2
                return

            elif isinstance(e, Bullet) and e in game.colliding_entities(self):
                game.add_entity(Explosion(self.pos))
                e.stop_callbacks()  
                game.remove_entity(self)
                game.remove_entity(e)
                game.score += 2
                return

        step_size = self._speed * dt
        new_x = self.pos[0]
        new_y = self.pos[1] - step_size
        self.pos = (new_x, new_y)

        if self.pos[1] < -100:  #
            self.stop_callbacks()
            game.remove_entity(self)
        step_size = self._speed * dt
        new_x = self.pos[0]
        new_y = self.pos[1] - step_size
        self.pos = (new_x, new_y)

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.source = "img/player.png"
        game.bind(on_frame=self.move_step)
        self._shoot_event = Clock.schedule_interval(self.shoot_step, 0.3)
        self.pos = (400, 0)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)
        self._shoot_event.cancel()

    def shoot_step(self, dt):
        if "spacebar" in game.keysPressed:
            x = self.pos[0]
            y = self.pos[1] + 50
            game.add_entity(Bullet((x, y)))

    def move_step(self, sender, dt):
        step_size = 1000 * dt
        newx = self.pos[0]
        newy = self.pos[1]
        if "a" in game.keysPressed:
            newx -= step_size
        if "d" in game.keysPressed:
            newx += step_size
        self.pos = (newx, newy)
        if newx < 0:
            newx = 0
        elif newx > Window.width - self.size[0]:
            newx = Window.width - self.size[0]

        self.pos = (newx, newy)

class GameOverPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Thanks for play'
        self.size_hint = (None, None)
        self.size = (1000, 850)

        self.content = BoxLayout(orientation='vertical', padding=10)
        
        self.label = Label(text="Enter your name:")
        self.text_input_name = TextInput(multiline=False, size_hint=(0.5, 0.5), height=30, width=400)

        self.label_rating = Label(text="Rate the game (1-5):")
        self.text_input_rating = TextInput(input_type='number', multiline=False, size_hint=(0.5, 0.5), height=30, width=400)
        
        self.label_explosion_sound = Label(text="Score for explosion sound (1-10):")
        self.text_input_explosion_sound = TextInput(input_type='number', multiline=False, size_hint=(0.5, 0.5), height=30, width=400)

        self.label_bullet_sound = Label(text="Score for bullet sound (1-10):")
        self.text_input_bullet_sound = TextInput(input_type='number', multiline=False, size_hint=(0.5, 0.5), height=30, width=400)

        self.label_player_movement = Label(text="Score for player movement (1-10):")
        self.text_input_player_movement = TextInput(input_type='number', multiline=False, size_hint=(0.5, 0.5), height=30, width=400)

        self.label_game_difficulty = Label(text="Score for game difficulty (1-10):")
        self.text_input_game_difficulty = TextInput(input_type='number', multiline=False, size_hint=(0.5, 0.5), height=30, width=400)

        self.label_like = Label(text="What do you like in this game ?:")
        self.text_input_like = TextInput(multiline=True, size_hint=(0.5, 0.5), height=100, width=400)

        self.label_suggest = Label(text="Do you have any suggestions ?:")
        self.text_input_suggest = TextInput(multiline=True, size_hint=(0.5, 0.5), height=100, width=400)

        self.ok_button = Button(text='OK', size_hint=(0.5, 0.5), height=60, width=200)
        self.ok_button.bind(on_press=self.dismiss_with_data)

        self.content.add_widget(self.label)
        self.content.add_widget(self.text_input_name)
        self.content.add_widget(self.label_rating)
        self.content.add_widget(self.text_input_rating)
        self.content.add_widget(self.label_explosion_sound)
        self.content.add_widget(self.text_input_explosion_sound)
        self.content.add_widget(self.label_bullet_sound)
        self.content.add_widget(self.text_input_bullet_sound)
        self.content.add_widget(self.label_player_movement)
        self.content.add_widget(self.text_input_player_movement)
        self.content.add_widget(self.label_game_difficulty)
        self.content.add_widget(self.text_input_game_difficulty)
        self.content.add_widget(self.label_like)
        self.content.add_widget(self.text_input_like)
        self.content.add_widget(self.label_suggest)
        self.content.add_widget(self.text_input_suggest)
        self.content.add_widget(self.ok_button)


    def dismiss_with_data(self, instance):
        player_name = self.text_input_name.text
        if not player_name:
            player_name = "Anonymous"

        try:
            rating = int(self.text_input_rating.text)
            if 1 <= rating <= 5:

                explosion_sound_score = int(self.text_input_explosion_sound.text)
                bullet_sound_score = int(self.text_input_bullet_sound.text)
                player_movement_score = int(self.text_input_player_movement.text)
                game_difficulty_score = int(self.text_input_game_difficulty.text)

                game.store_score(player_name)
                feedback = self.text_input_like.text
                print(f"Player: {player_name}, Score: {game.score}, Rating: {rating}, Feedback: {feedback}")
                self.dismiss()
            else:
                self.show_error_message("Invalid rating. Please enter a number between 1 and 5.")
        except ValueError:
            self.show_error_message("Invalid rating input. Please enter a number between 1 and 5.")

game = GameWidget()
game.player = Player()
game.player.pos = (Window.width - Window.width/1.75, 0)
game.add_entity(game.player)

class RocketApp(App):
    def build(self):
        return game

if __name__ == "__main__":
    RocketApp().run()