from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivymd.uix.tab import MDTabs,MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList,TwoLineAvatarListItem,TwoLineRightIconListItem
from kivy.properties import ObjectProperty,StringProperty
from kivymd.uix.card import MDCard
# data processing 
from LeoDataCheck.datacheck import Validate,ManageMessages,generate,Crud,Server
from LeoDataCheck.LeoEncryption import Integrity
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
class FindFrinds(MDFloatLayout,MDTabsBase):
    pass


class SsmpUsers(TwoLineRightIconListItem):
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
class Converstations(MDBoxLayout):
    msg=StringProperty()
    time=StringProperty()
    sender=StringProperty()


# file loading
Builder.load_file("./Screens/Register.kv")
Builder.load_file("./Screens/ValidateScreen.kv")
Builder.load_file("./Screens/ChatScreen.kv")
Builder.load_file("./Screens/ConversationScreen.kv")
Builder.load_file("./widgets/ConversationMessages.kv")
Builder.load_file("./widgets/ChatsLists.kv")
Builder.load_file("./widgets/BottomNav.kv")
class TempStore:
    mycode=''
    usercode=''
    receiverName=''
    
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
        data=Crud.myinfo()
        TempStore.mycode=data['code']
        self.wm.current="chatScreen"
        self.allusers()
        ChatResponse=ManageMessages.Chats()
        if ChatResponse=="None":
            pass
        else:
            for chat in ChatResponse:
                print(chat)
                username=chat['username']
                time=chat["time"]
                deviceID=chat["deviceID"]
                msg=chat["msg"]
                self.chats=ChatUser()
                self.chats.image="hello"
                self.chats.name=username
                self.chats.last_msg=msg
                self.chats.date=time
                self.chats.chatid=deviceID
                self.wm.get_screen("chatScreen").ids.chatTab.ids.chatlist.add_widget(self.chats)
    
    def allSSMPUsers(self):
        ChatResponse=Server.ssmpUsers()
        if ChatResponse=="None":
            pass
        else:
            for chat in ChatResponse:
                username=chat['username']
                deviceID=chat["deviceID"]
                self.allusers=SsmpUsers()
                self.allusers.image="hello"
                self.allusers.name=username
                self.allusers.chatid=deviceID
                self.wm.get_screen("chatScreen").ids.allusersTab.ids.ssmpUsers.add_widget(self.allusers)
               
               
        
    def ManageScreens(self,screen):
        self.wm.current=screen
    def RegisterFunc(self,phone,username):
        phoneResponse=Validate.phone(phone)
        if phoneResponse=="success":
            usernameResponse=Validate.username(name=username)
            if usernameResponse and phoneResponse=="success":
                # generate device id
                code=generate.DeviceID(length=6)
                registrationResponse=Crud.RegistrationData(phone=phone,deviceID=code,username=username)
                if registrationResponse=="success":
                    print(code)
                    print("data save saved successfully")
                    
                
                self.ManageScreens("ValidateScreen")
            else:
                self.wm.get_screen(self.wm.current).ids.response.text=phoneResponse   
        else:
            self.wm.get_screen(self.wm.current).ids.response.text=phoneResponse
    def CheckCode(self,code):
        codeResponse=Validate.CheckCode(code=code)
        # 288032
        if codeResponse=="success":
            # all user to move next screen
            # send the details to the server
            self.ManageScreens("chatScreen")
            pass
        else:
            self.wm.get_screen(self.wm.current).ids.response.text=codeResponse
    def converationScreen(self,name,chatId):
        TempStore.usercode=chatId
        TempStore.receiverName=name
        self.wm.get_screen("conversationScreen").ids.username.text=name
        messagesResponse=ManageMessages.Messages(mycode=TempStore.mycode,chatcode=chatId)
        if messagesResponse!="None":
            for message in messagesResponse:
                msg=message['msg']
                time=message['time']
                user=message['user']
                self.msg=Converstations()
                self.msg.msg=msg
                self.msg.time=time
                self.msg.sender=user
                self.wm.get_screen("conversationScreen").ids.loadConverstation.add_widget(self.msg)
        self.ManageScreens("conversationScreen")
        
    def SendMessage(self,msg):
        mycode=TempStore.mycode
        userCode=TempStore.usercode
        usersName=TempStore.receiverName
        codeCombined=f"{mycode}-"+f"{userCode}"
        date=generate.date()
        phone='123'
        checksum=Integrity.checkSum(msg=msg)
        Crud.InsertMessage(msg=msg,code=codeCombined, date=date,phone=phone,checksum=checksum)
        Crud.UPdateChatList(date=date,message=msg,username=usersName,code=userCode)
        
        
        
        
        
        


MainApp().run()


