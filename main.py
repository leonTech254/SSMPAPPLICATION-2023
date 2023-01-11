from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition

class WindowManager(ScreenManager):
    pass

class RegisterScreen(Screen):
    pass
class IntoScreen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Cyan"
        # self.theme_cls.material_style = "M3"
        self.wm=ScreenManager(transition=FadeTransition())
        screens=[IntoScreen(name="intoScreen"),RegisterScreen(name="registerScreen")]
        for screen in screens:
            self.wm.add_widget(screen)
            
        return self.wm


MainApp().run()


