import sqlite3
import random
import re
import datetime
import requests
from kivy.network.urlrequest import UrlRequest
from datetime import timezone
conn = sqlite3.connect("hashDatabase.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
query="CREATE TABLE  IF NOT EXISTS  Users(username VARCHAR(100),phoneNumber VARCHAR(100),DeviceCode VARCHAR(100),isValidated VARCHAR(100) default 'false')"
cursor.execute(query)
# messages
query="CREATE TABLE  IF NOT EXISTS  Messages(chatKey VARCHAR(100),msg VARCHAR(100),phoneNumber VARCHAR(100),DeviceCode VARCHAR(100),msgFlag VARCHAR(100) default 'checked',MsgTimeStamp VARCHAR(100),msgCheckSum VARCHAR(100))"
cursor.execute(query)
query="CREATE TABLE  IF NOT EXISTS  Chats(username VARCHAR(100),msg VARCHAR(100),DeviceCode VARCHAR(100), MsgTimeStamp VARCHAR(100))"
cursor.execute(query)
class Validate:
    def phone(number):
        print(number.isnumeric)
        if number.isnumeric():
            if(len(number)==12):
                checkCode=number[0:4]
                if checkCode=="2547":
                    print("phone")
                    return "success"
                else:
                    return "only kenyan numbers are supported,+254"        
            else:
                print(len(number))
                return "invalid phone number"  
            
        else:
            print("not numeric")
            return "invalid phone number"
    def username(name):
        if len(name)>4:
            return "success"
        else:
            return "username must have atleast 4 characters"
    def CheckCode(code):
        check = f"SELECT * FROM Users WHERE DeviceCode='{code}'"
        result = cursor.execute(check).fetchall()
        if not result:
            return "invalid code"
        else:
            query=f"UPDATE Users SET isValidated='true'"
            conn.execute(query)
            conn.commit()
            return "success"
        
        
class ManageMessages:
    def Messages(mycode,chatcode,orCode):
        check = f"SELECT * FROM Messages WHERE chatKey='{chatcode}' OR chatKey='{orCode}'"
        messages = cursor.execute(check).fetchall()
        
        MessagesList=[]
        
        if not messages:
            return "None"
        else:
            
            for message in messages:
                allID=message["DeviceCode"]
                myId=allID.split("-")[0]
                messageDict={}
                messageDict['deviceID']=message["DeviceCode"]
                messageDict['username']=message["chatKey"]    
                messageDict['time']=message["MsgTimeStamp"]
                messageDict['checksum']=message["msgCheckSum"]
                messageDict['msg']=message["msg"]
                messageDict['msgFlag']=message['msgFlag']
                if allID==chatcode:
                    messageDict['user']='me'
                else:
                    messageDict['user']='friend'
                MessagesList.append(messageDict)
            return MessagesList
    def Chats():
        check = f"SELECT * FROM Chats"
        messages = cursor.execute(check).fetchall()
        ChatList=[]
        if not messages:
            return "None"
        else:
            for message in messages:
                ChatDict={}
                ChatDict['deviceID']=message["DeviceCode"]
                ChatDict['username']=message["username"]    
                ChatDict['time']=message["MsgTimeStamp"]
                ChatDict['msg']=message["msg"]
                ChatList.append(ChatDict)
            return ChatList
class Crud:
    def RegistrationData(username,phone,deviceID):
        add_data = f"INSERT INTO Users(username,phoneNumber,DeviceCode) VALUES(?,?,?)"
        values = (f'{username}', f'{phone}',f'{deviceID}')
        cursor.execute(add_data, values)
        conn.commit()
        return "success"
    def myinfo():
        check = f"SELECT * FROM Users"# WHERE DeviceCode='{chatcode}'"
        Users = cursor.execute(check).fetchall()
        userInfo={}
        if not Users:
            return "None"
        else:
            for user in Users:
                userInfo["code"]=user['DeviceCode']
                userInfo['username']=user['username']
                userInfo['isValidated']=user['isValidated']
                if userInfo['isValidated']!='true':
                    return "incomplete"
                else:
                    return userInfo
    def InsertMessage(msg,code,date,phone,checksum):
        print(code)
        users="INSERT INTO Messages('chatKey','msg','phoneNumber','DeviceCode','MsgTimeStamp','msgCheckSum') VALUES(?,?,?,?,?,?)"
        values=(f'{code}',f'{msg}',f'{phone}',f'{code}',f'{date}',f'{checksum}')
        cursor.execute(users, values)
        conn.commit()
    def UPdateChatList(username,date,message,code):
        check = f"SELECT * FROM Chats WHERE DeviceCode='{code}'"
        User = cursor.execute(check).fetchall()
        if not User:
            # add the user to the chat list
            users="INSERT INTO Chats('username','msg','DeviceCode','MsgTimeStamp') VALUES(?,?,?,?)"
            values=(f'{username}',f'{message}',f'{code}',f'{date}')
            cursor.execute(users, values)
            conn.commit()
            print("inserted")
            return "None"
        else:
            # update 
            query=f"UPDATE Chats SET MsgTimeStamp='{date}', msg='{message}' WHERE DeviceCode='{code}'"
            conn.execute(query)
            conn.commit()
            
        
                
                
            
            
        
        
class generate:
    def DeviceID(length):
        code=""
        for i in range(0,length):
            code+=str(random.randint(0,9))
        return code
    def date():
        now = datetime.datetime.now(timezone.utc)
        current_time = now.strftime("%H:%M:%S")
        hours = int(current_time[:2])
        cur = re.sub(current_time[:2], str(hours), current_time)
        tdate = now.strftime("%d""-%m" "-%y")
        regtime = cur+" Date-"+tdate
        return regtime
    
class Server:
    def ssmpUsers():
        return "None"
    
    def registerUser(username,phone,deviceID):
        url="https://api2.leonteqsecurity.com/ssmp/allusers"
        data = {'username': username,'phone':phone,'deviceID':deviceID}
        response = requests.post(url, json=data)
        print(response.status_code)
        contents=response.json()
        return contents['message']
    def getUsers():
        url="https://api2.leonteqsecurity.com/ssmp/allusers"
        response = requests.get(url)
        contents=response.json()
        return contents['users']
    def SendMessage(msg,code,date,phone,checksum):
        url="https://api2.leonteqsecurity.com/ssmp/messages"
        data = {'chatKey': code,'msg':msg,'time':date,'code':code,'checksum':checksum}
        response = requests.post(url, json=data)
        print(response.status_code)
        contents=response.json()
        return contents['message']
    
    def LoadConversation(chatCode,orCode):
        url="https://api2.leonteqsecurity.com/ssmp/load/conversation"
        data = {'chatcode':chatCode,'orcode':orCode}
        try:
            response = requests.post(url, json=data,timeout=5)
            print(response.status_code)
            contents=response.json()
            print(contents['messages'])
            MessageList=[]
            if contents['messages']!="None":
                messageDict={}
                messageDict['message']='success'
                MessageList.append(messageDict)
                MessageList.append(contents['messages'])
                return MessageList
            else:
                return contents[{'message':"None"}]
        except:
            return contents[{'message':"None"}]
            
        
   
        