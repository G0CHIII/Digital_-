# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from PIL import Image
from kivy.uix.scrollview import ScrollView
import webbrowser
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
import random
from mycamera import *
from library import *
from kivy.uix.boxlayout import BoxLayout

from io import open
from kivy.config import Config

Config.set('kivy', 'keyboard_mode', 'systemanddock')

Window.size = (480, 853)


watchlist = ['Медный всадник А.С. Пушкин: Иллюстрации',
             'Медный всадник А.С. Пушкин: Спектакль',
             'Вишневый сад А.П. Чехов: Minecraft-спектакль',
             'Вишневый сад А.П. Чехов: Лекция',
             'Дон Кихот М. де Сервантес: Фильм']
readlist = ['Медный всадник А.С. Пушкин: О книге',
                'Медный всадник А.С. Пушкин: О наводнении',
                'Медный всадник А.С. Пушкин: О печати на книге']
listenlist = ['Медный всадник А.С. Пушкин: Аудиокнига',
              'Дон Кихот М. де Сервантес: Подкаст']

choisesscreen = {'Медный всадник А.С. Пушкин: Иллюстрации': 'illust',
                     'Медный всадник А.С. Пушкин: Спектакль': 'vidbook',
                     'Медный всадник А.С. Пушкин: О книге': 'abbook',
                     'Медный всадник А.С. Пушкин: О наводнении': 'voda',
                     'Медный всадник А.С. Пушкин: О печати на книге': 'sign',
                     'Медный всадник А.С. Пушкин: Аудиокнига': 'audbook',
                     'Вишневый сад А.П. Чехов: Minecraft-спектакль': 'vscraft',
                     'Вишневый сад А.П. Чехов: Лекция': 'vslecture',
                     'Дон Кихот М. де Сервантес: Фильм': 'dkfilm',
                     'Дон Кихот М. де Сервантес: Подкаст': 'dpkast'}


class Search(TextInput):
    choicesfile = StringProperty()

    def __init__(self, **kwargs):
        self.choicesfile = kwargs.pop('choicesfile', '')
        self.choiceslist = watchlist + readlist + listenlist
        self.choisesscreen = choisesscreen
        super(Search, self).__init__(**kwargs)
        self.bind(text=self.on_text)
        self.dropdown = None
        self.hint_text = 'Поиск'
        self.font_size = 20

    def on_text(self, Search, text):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None
        if text == '':
            return
        values = []
        for q in self.choiceslist:
            if text.lower() in q.lower():
                values.append(q)
        self.values = values
        if len(values) > 0:
            self.dropdown = DropDown()
            for val in self.values[:10]:
                self.dropdown.add_widget(Button(text=val, size_hint_y=None, height=48, font_size=15, halign='left',
                                                background_color=[255, 255, 255, 1], color=[0, 0, 0, 1],
                                                on_release=self.do_choose))
            self.dropdown.add_widget(Button(size_hint_y=None, height=1000, background_color=[255, 255, 255, 0.9]))
            self.dropdown.open(self)

    def do_choose(self, butt):
        screen_to_go = self.choisesscreen[butt.text]
        if self.dropdown:
            App.get_running_app().sm.current = screen_to_go
            self.dropdown.dismiss()
            self.dropdown = None

watch_random = random.choice(watchlist)
listen_random = random.choice(listenlist)
read_random = random.choice(readlist)

class MainScreenManager(ScreenManager):
    watch_screen = StringProperty(choisesscreen[watch_random])
    listen_screen = StringProperty(choisesscreen[listen_random])
    read_screen = StringProperty(choisesscreen[read_random])
    pass

class MyApp(App):
    watch = StringProperty(watch_random)
    listen = StringProperty(listen_random)
    read = StringProperty(read_random)
    def build(self):
        self.sm = MainScreenManager()
        return self.sm



if __name__ == '__main__':
    MyApp().run()
