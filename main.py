from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
# data processing 
from LeoDataCheck.datacheck import Validate
class WindowManager(ScreenManager):
    pass

class RegisterScreen(Screen):
    pass
class IntoScreen(Screen):
    pass
class ValidateScreen(Screen):
    pass


# file loading
Builder.load_file("./Screens/Register.kv")
Builder.load_file("./Screens/ValidateScreen.kv")


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Cyan"
        # self.theme_cls.material_style = "M3"
        self.wm=ScreenManager(transition=FadeTransition())
        screens=[IntoScreen(name="intoScreen"),RegisterScreen(name="registerScreen"),ValidateScreen(name='ValidateScreen')]
        for screen in screens:
            self.wm.add_widget(screen)
        return self.wm
    def ManageScreens(self,screen):
        self.wm.current=screen
        
    def RegisterFunc(self,phone,username):
        phoneResponse=Validate.phone(phone)
        if phoneResponse=="success":
            usernameResponse=Validate.username(name=username)
            if usernameResponse and phoneResponse=="success":
                self.ManageScreens("ValidateScreen")
            else:
                self.wm.get_screen(self.wm.current).ids.response.text=phoneResponse   
        else:
            self.wm.get_screen(self.wm.current).ids.response.text=phoneResponse
    def CheckCode(self,code):
        codeResponse=Validate.CheckCode(code=compile)
        if codeResponse=="success":
            pass
        
        


MainApp().run()


