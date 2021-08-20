from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
# from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
# from kivy.uix.widget import Widget
# from kivy.uix.button import Button
from kivy.config import Config

Config.set('graphics', 'resizable', True)


class AcademicScraper:
    def generate_boxes():
        print("generating Boxes!!!")

class TopSection(BoxLayout):
    pass

class MainUI(BoxLayout):
    pass


class AcademicWebScraperApp(App):
    # pass
    def build(self):
        # return super().build()
        return MainUI()

    def runScrape(self, keyword):
        print("hello ", keyword)
        AcademicScraper.generate_boxes()

AcademicWebScraperApp().run()