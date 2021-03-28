from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton

class Lib(FloatLayout):
    grid = ObjectProperty(GridLayout())
    def __init__(self, **kwargs):
        super(Lib, self).__init__(**kwargs)
        self.size_hint_y = None
        self.cols = 1
        self.size_hint_y = None
        self.grid1 = GridLayout()
        self.grid1.pos_hint = {'center_x': .5, 'center_y': .45}
        self.grid1.size_hint_y = None
        self.grid1.cols = 1
        self.grid1.row_default_height = '125dp'
        self.grid1.spacing = (20, 20)
        self.grid1.padding = (10, 10)
        self.grid1.height = self.grid1.minimum_height
        self.ind_pages = {1: ["'illust'", "'glaz.png'", "'[b]Медный Всадник[/b]'", "'А.С. Пушкин'", "'Иллюстрации'"],
                          2: ["'vidbook'", "'glaz.png'", "'[b]Медный Всадник[/b]'", "'А.С. Пушкин'", "'Спектакль'"],
                          3: ["'abbook'", "'read.png'", "'[b]Медный Всадник[/b]'", "'А.С. Пушкин'", "'О книге'"],
                          4: ["'voda'", "'read.png'", "'[b]Медный Всадник[/b]'", "'А.С. Пушкин'", "'О наводнении'"],
                          5: ["'sign'", "'read.png'", "'[b]Медный Всадник[/b]'", "'А.С. Пушкин'", "'О печати на книге'"],
                          6: ["'audbook'", "'ears.png'", "'[b]Медный Всадник[/b]'", "'А.С. Пушкин'", "'Аудиокнига'"],
                          7: ["'vscraft'", "'glaz.png'", "'[b]Вишневый сад[/b]'", "'А.П. Чехов'", "'Minecraft-спектакль'"],
                          8: ["'vslecture'", "'glaz.png'", "'[b]Вишневый сад[/b]'", "'А.П. Чехов'", "'Лекция'"],
                          9: ["'dkfilm'", "'glaz.png'", "'[b]Дон Кихот[/b]'", "'М. де Сервантес'", "'Фильм'"],
                          10: ["'dpkast'", "'ears.png'", "'[b]Дон Кихот[/b]'", "'М. де Сервантес'", "'Подкаст'"],}
        self.ind_pages_filter = self.ind_pages.copy()
        self.do_page()

    def do_page(self,*l):
        self.add_widget(self.grid1)
        self.btn_view = ToggleButton(group='filter', allow_no_selection=True, state='normal', text='смотри',
                                    pos_hint={'center_x': .15, 'center_y': .7}, size_hint=[None, None], size=[100, 50],
                                    on_release=self.do_filter, background_color = (2.28, 2.17, 2.55, 1), color=[0, 0, 0, 1])

        self.btn_read = ToggleButton(group='filter', allow_no_selection=True, state='normal', text='читай',
                                       pos_hint={'center_x': .5, 'center_y': .7}, size_hint=[None, None], size=[100, 50],
                                       on_release=self.do_filter, background_color = (2.28, 2.17, 2.55, 1), color=[0, 0, 0, 1])

        self.btn_listen = ToggleButton(group='filter', allow_no_selection=True, state='normal', text='слушай',
                                     pos_hint={'center_x': .85, 'center_y': .7}, size_hint=[None, None], size=[100, 50],
                                     on_release=self.do_filter, background_color = (2.28, 2.17, 2.55, 1), color=[0, 0, 0, 1])

        self.add_widget(self.btn_view)
        self.add_widget(self.btn_read)
        self.add_widget(self.btn_listen)

        if (self.btn_view.state == 'normal')&(self.btn_read.state == 'normal')&(self.btn_listen.state == 'normal'):
            self.add_buttons()

    def do_filter(self,*l):
        self.grid1.clear_widgets()
        ind_pages_view = {}
        ind_pages_read = {}
        ind_pages_listen = {}
        for (key, value) in self.ind_pages.items():
            if value[1] == "'glaz.png'":
                ind_pages_view[key] = value
        for (key, value) in self.ind_pages.items():
            if value[1] == "'read.png'":
                ind_pages_read[key] = value
        for (key, value) in self.ind_pages.items():
            if value[1] == "'ears.png'":
                ind_pages_listen[key] = value

        if self.btn_view.state == 'down':
            self.ind_pages_filter = ind_pages_view.copy()
        elif self.btn_read.state == 'down':
            self.ind_pages_filter = ind_pages_read.copy()
        elif self.btn_listen.state == 'down':
            self.ind_pages_filter = ind_pages_listen.copy()
        else:
            self.ind_pages_filter = self.ind_pages.copy()

        self.add_buttons()


    def add_buttons(self,):
        print('btn_view:', self.btn_view.state)
        print('btn_read:', self.btn_read.state)
        print('btn_listen:', self.btn_listen.state)

        print(self.ind_pages_filter)

        for i in self.ind_pages_filter.keys():

            template = """
Button:
    on_release: app.root.current = """ + self.ind_pages_filter[i][0] + """
    background_color: 255, 255, 255, 0
    StackLayout:
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [(20, 20), (20, 20), (20, 20), (20, 20)]
        pos: self.parent.pos
        size: self.parent.size
        orientation: 'lr-tb'
        Label:
            size_hint_x: 0.05
            size_hint_y: 0.7
        Image:
            source: """ + self.ind_pages_filter[i][1] + """
            size_hint_x: 0.25
            size_hint_y: 0.7
        Label:
            size_hint_x: 0.05
            size_hint_y: 0.7
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.65
            size_hint_y: 0.7
            Label:
                text_size: self.size
                valign: 'bottom'
                halign: 'left'            
                markup: True
                text: """ + self.ind_pages_filter[i][2] + """
                color: 0, 0, 0, 1
            Label:
                text_size: self.size
                valign: 'top'
                halign: 'left'
                markup: True
                text: """ + self.ind_pages_filter[i][3] + """
                color: 0, 0, 0, 1
        Label:
            size_hint_x: 0.05
            size_hint_y: 0.7
        Label:
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            size_hint_x: 0.7
            size_hint_y: 0.3
            text: """ + self.ind_pages_filter[i][4] + """
            color: 0, 0, 0, 1
"""
            self.grid1.add_widget(Builder.load_string(template))