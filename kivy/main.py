from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
# from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.widget import Widget
# from kivy.uix.button import Button
from kivy.config import Config

Config.set('graphics', 'resizable', True)


class TopSection(BoxLayout):
    pass

class MainUI(BoxLayout):
    pass


class AcademicWebScraperApp(App):
    # pass
    def build(self):
        # return super().build()
        return MainUI()

AcademicWebScraperApp().run()