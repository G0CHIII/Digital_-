from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton

class Menu(FloatLayout):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.size_hint = (1, 0.10)
        self.add_buttons()

    def add_buttons(self,*l):
        template = """
GridLayout:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    cols: 4
    BoxLayout:
        orientation: 'horizontal'
        Button:
            background_color: 255, 255, 255, 1
            on_release: app.root.current = 'main'
            Image:
                source: 'main.png'
                pos: self.parent.center_x*0.35, self.parent.center_y
                center_y: self.parent.center_y
                size: self.parent.width * 0.5, self.parent.width * 0.5
    BoxLayout:
        orientation: 'horizontal'
        Button:
            background_color: 255, 255, 255, 1
            on_release: app.root.current = 'library'
            Image:
                source: 'library.png'
                pos: self.parent.center_x*0.75, self.parent.center_y
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                size: self.parent.width * 0.5, self.parent.width * 0.5
    BoxLayout:
        orientation: 'horizontal'
        Button:
            background_color: 255, 255, 255, 1
            on_release: app.root.current = 'thecamera'
            Image:
                source: 'skan.png'
                pos: self.parent.center_x*0.85, self.parent.center_y
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                size: self.parent.width * 0.5, self.parent.width * 0.5
    BoxLayout:
        orientation: 'horizontal'
        Button:
            background_color: 255, 255, 255, 1
            on_release: app.root.current = 'abapp'
            Image:
                source: 'abapp.png'
                pos: self.parent.center_x*0.90, self.parent.center_y
                center_x: self.parent.center_x
                center_y: self.parent.center_y
                size: self.parent.width * 0.5, self.parent.width * 0.5
"""
        self.add_widget(Builder.load_string(template))