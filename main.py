from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivymd.uix.tab import MDTabs,MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList,TwoLineAvatarListItem,TwoLineRightIconListItem
from kivy.properties import ObjectProperty,StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDRaisedButton
# data processing 
from LeoDataCheck.datacheck import Validate,ManageMessages,generate,Crud,Server
from LeoDataCheck.LeoEncryption import Integrity,Encryption
from Network.leoNetwork import Server2,serverStore
from kivy.clock import Clock
import requests
from BIOMETRIC.boo import Bioo,run_on_ui_thread

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        if key == 27:
            print("pressed")
            if self.current == 'registerScreen':
                self.current = "intoScreen"
                return True
            elif self.current == 'ValidateScreen':
                self.current = "registerScreen"
                return True
            elif self.current == 'conversationScreen':
                self.current = "chatScreen"
                return True
            else:
                return False


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
class SsmpUsers(MDBoxLayout):
    image=StringProperty()
    name=StringProperty()
    code=StringProperty()
    last_msg=StringProperty()
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
    originalmsg=StringProperty()
    checksum=StringProperty()
    flag=StringProperty()
class Item(TwoLineAvatarListItem):
    source=StringProperty()
    

# file loading
Builder.load_file("./Screens/Register.kv")
Builder.load_file("./Screens/ValidateScreen.kv")
Builder.load_file("./Screens/ChatScreen.kv")
Builder.load_file("./Screens/ConversationScreen.kv")
Builder.load_file("./widgets/ConversationMessages.kv")
Builder.load_file("./widgets/ChatsLists.kv")
Builder.load_file("./widgets/BottomNav.kv")
Builder.load_file("./widgets/SSMPUsersList.kv")
class TempStore:
    mycode=''
    usercode=''
    receiverName=''


#Window.size = (330, 600)
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"


class MainApp(MDApp):
    dialog = None
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = 'Cyan'
        self.authentication_done = False

        screens = [
                 IntoScreen(name="intoScreen"),
                 RegisterScreen(name="registerScreen"),
                 ValidateScreen(name='ValidateScreen'),
                 ChatScreen(name="chatScreen"),
                 ConversationScreen(name="conversationScreen")
                   ]
        self.wm = WindowManager(transition=FadeTransition())

        for screen in screens:
            self.wm.add_widget(screen)
        return self.wm
    def on_start(self):
        data=Crud.myinfo()
        if data!="None":
            TempStore.mycode=data['code']
            # self.wm.current="intoScreen"
            self.wm.current="conversationScreen"
        elif data=='incomplete':
            self.wm.current='ValidateScreen'
            self.wm.get_screen(self.wm.current).ids.incomplete.text="complete registration"
        else:
            self.wm.current="intoScreen"
        # self.wm.current="chatScreen"
            
            
        self.allSSMPUsers()
        ChatResponse=ManageMessages.Chats()
        if ChatResponse=="None":
            pass
        else:
            for chat in ChatResponse:
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
        ssmpUsers=Server.getUsers()
        if ssmpUsers=="None":
            pass
        else:
            for user in ssmpUsers:
                deviceID=user["code"]
                if deviceID==TempStore.mycode:
                    pass
                else:
                    username=user['username']
                    deviceID=user["code"]
                    self.allusers=SsmpUsers()
                    self.allusers.image="hello"
                    self.allusers.name=username
                    self.allusers.code=deviceID
                    self.wm.get_screen("chatScreen").ids.allusersTab.ids.ssmpUsers.add_widget(self.allusers)
    def ManageScreens(self,screen):
        # self.wm.current=screen
        self.Fingerprint()
    def RegisterFunc(self,phone,username):
        phoneResponse=Validate.phone(phone)
        if phoneResponse=="success":
            usernameResponse=Validate.username(name=username)
            if usernameResponse and phoneResponse=="success":
                # generate device id
                code=generate.DeviceID(length=6)
                serverResponse=Server.registerUser(phone=phone,deviceID=code,username=username)
                if serverResponse=="success":
                    registrationResponse=Crud.RegistrationData(phone=phone,deviceID=code,username=username)
                    if registrationResponse=="success":
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
    def refreshConversation(self,nap):
        print(Server2.newMessages())
        if Server2.newMessages()=="new":
            Server2.closeMessage()
            chatId=TempStore.usercode
            mycode=TempStore.mycode       
            name=TempStore.receiverName
            self.wm.get_screen("conversationScreen").ids.loadConverstation.clear_widgets()
            self.converationScreen(name=name,chatId=chatId)
    
    def CheckIntegrity(self,nap):
        IntegrityLight=self.wm.get_screen("conversationScreen").ids.IntegrityCheckLight
        if 'yes' in self.compromised:
            IntegrityLight.icon='heart-broken'
            if self.color=='red':
                self.color='yellow'
                IntegrityLight.color='yellow'
            else:
                IntegrityLight.color='red'
                self.color='red'
        else:
            if self.color=='green':
                IntegrityLight.color='blue'
                self.color='blue'
            else:
                IntegrityLight.color='green'
                self.color='green'
    def Shufflekey(self,nap):
        chatId=TempStore.usercode
        mycode=TempStore.mycode       
        name=TempStore.receiverName
        self.wm.get_screen("conversationScreen").ids.loadConverstation.clear_widgets()
        self.converationScreen(name=name,chatId=chatId)
        
    def converationScreen(self,name,chatId):
        self.compromised=[]
        Clock.unschedule(self.refreshConversation)
        Clock.unschedule(self.CheckIntegrity)
        Clock.unschedule(self.Shufflekey)
        TempStore.usercode=chatId
        mycode=TempStore.mycode
        codeCombined=f"{mycode}-"+f"{chatId}"
        OrCode=f"{chatId}-"+f"{mycode}"       
        TempStore.receiverName=name
        self.wm.get_screen("conversationScreen").ids.username.text=name
        messagesResponse=ManageMessages.Messages(mycode=TempStore.mycode,chatcode=codeCombined,orCode=OrCode)
        Server2.LoadConversation(chatCode=codeCombined,orCode=OrCode)
        if messagesResponse!="None":
            for message in messagesResponse:
                msgFlag=message['msgFlag']
                msg=message['msg']
                time=message['time']
                user=message['user']
                checksum=message['checksum']
                self.msg=Converstations()
                self.msg.msg=Encryption.encrypt(Integrity.generate_key(length=6),message=msg)
                self.msg.originalmsg=msg
                self.msg.time=time
                self.msg.sender=user
                self.msg.checksum=checksum
                self.msg.flag=msgFlag
                self.wm.get_screen("conversationScreen").ids.loadConverstation.add_widget(self.msg)
                if msgFlag!='checked':
                    self.compromised.append("yes")
                else:
                    self.compromised.append('no')
        else:
            self.compromised.append('no')          
        self.ManageScreens("conversationScreen")
        # for refreshing the conversation screen
        self.color=''
        Clock.schedule_interval(self.refreshConversation, 3)
        Clock.schedule_interval(self.CheckIntegrity, 1)
        Clock.schedule_interval(self.Shufflekey, 5)
        
    def SendMessage(self,msg):
        mycode=TempStore.mycode
        userCode=TempStore.usercode
        usersName=TempStore.receiverName
        codeCombined=f"{mycode}-"+f"{userCode}"
        date=generate.date()
        phone='123'
        checksum=Integrity.checkSum(msg=msg)
        # Crud.InsertMessage(msg=msg,code=codeCombined, date=date,phone=phone,checksum=checksum)
        Crud.UPdateChatList(date=date,message=msg,username=usersName,code=userCode)
        Server.SendMessage(msg=msg,code=codeCombined, date=date,phone=phone,checksum=checksum)
        # updating the chatscreen temporary
        self.msg=Converstations()
        self.msg.msg=msg
        self.msg.time=date
        self.msg.sender=mycode
        self.msg.sender="me"
        self.wm.get_screen("conversationScreen").ids.loadConverstation.add_widget(self.msg)
    def viewMessage(self,message,checksum,flag):
        if flag!="checked":
            msgFlag="comprimised"
        else:
            msgFlag="not compromised"
        self.dialog = MDDialog(title="MESSAGE SUMMURY",type="simple",
                items=[
                Item(text="PLAIN MESSAGE",secondary_text=message,source="message-outline"),
                Item(text="CHECKSUM",secondary_text=checksum,source="file-outline"),
                Item(text="INTEGRITY",secondary_text=msgFlag,source="lock"),
            ],
                buttons=[
                MDRaisedButton(text="CLOSE", on_press=self.closeMessageView),
                ],
        )
        self.dialog.open()
    def closeMessageView(self,*args):
        self.dialog.dismiss()
        
        
        
                    
    def Fingerprint(self):
        if not self.authentication_done:
            if str(Bioo().get_auth()) == "0":
                Bioo().auth_now(self.my_auth_callback)
                print("hello kenya")
                self.lockViewOnce=2

    def my_auth_callback(self, args):
        MDApp.get_running_app().some_string = str(args)
        if str(args)=="success":
            self.authentication_done = True
            print("unlocked")
        
        


MainApp().run()






