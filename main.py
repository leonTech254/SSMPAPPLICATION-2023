from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivymd.uix.tab import MDTabs,MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import MDList,TwoLineAvatarListItem,TwoLineRightIconListItem
from kivy.properties import ObjectProperty,StringProperty
from kivymd.uix.card import MDCard
# data processing 
from LeoDataCheck.datacheck import Validate,ManageMessages
class WindowManager(ScreenManager):
    pass

class RegisterScreen(Screen):
    pass
class IntoScreen(Screen):
    pass
class ValidateScreen(Screen):
    pass
class ChatScreen(Screen):
    pass

class ConversationScreen(Screen):
    pass

class ChatTab(MDFloatLayout,MDTabsBase):
    pass
class Status(MDFloatLayout,MDTabsBase):
    pass
class Calls(MDFloatLayout,MDTabsBase):
    pass

class ChatItem(TwoLineRightIconListItem):
    image=StringProperty()
    name=StringProperty()
    last_msg=StringProperty()
    name="martin"
class ChatUser(MDCard):
    image=StringProperty()
    name=StringProperty()
    last_msg=StringProperty()
    date=StringProperty()
    read=StringProperty()
    chatid=StringProperty()
    


# file loading
Builder.load_file("./Screens/Register.kv")
Builder.load_file("./Screens/ValidateScreen.kv")
Builder.load_file("./Screens/ChatScreen.kv")
Builder.load_file("./Screens/ConversationScreen.kv")
Builder.load_file("./widgets/ChatsLists.kv")
Builder.load_file("./widgets/BottomNav.kv")
class TempStore:
    mycode=''
    
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Cyan"
        # self.theme_cls.material_style = "M3"
        self.wm=ScreenManager(transition=FadeTransition())
        screens=[IntoScreen(name="intoScreen"),RegisterScreen(name="registerScreen"),ValidateScreen(name='ValidateScreen'),ChatScreen(name="chatScreen"),ConversationScreen(name="conversationScreen")]
        for screen in screens:
            self.wm.add_widget(screen)
        return self.wm
    def on_start(self):
        self.wm.current="chatScreen"
        ChatResponse=ManageMessages.Chats()
        if ChatResponse=="Nodne":
            pass
        else:
            for i in range(0,20):
                self.chats=ChatUser()
                self.chats.image="hello"
                self.chats.name="martin"
                self.chats.last_msg="hello my name is martin"
                self.chats.date="12:00 pm"
                self.wm.get_screen(self.wm.current).ids.chatTab.ids.chatlist.add_widget(self.chats)
            
        
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
            # all user to move next screen
            self.ManageScreens("chatScreen")
            pass
        else:
            self.wm.get_screen(self.wm.current).ids.response.text=codeResponse
    def converationScreen(self,chatId):

        ManageMessages.Messages(mycode=TempStore.mycode,chatcode=chatId)
        self.ManageScreens("conversationScreen")
        
        


MainApp().run()


