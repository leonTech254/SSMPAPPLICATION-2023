import sqlite3
import random
conn = sqlite3.connect("hashDatabase.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
query="CREATE TABLE  IF NOT EXISTS  Users(username VARCHAR(100),phoneNumber VARCHAR(100),DeviceCode VARCHAR(100),isValidated VARCHAR(100) default 'false')"
cursor.execute(query)
# messages
query="CREATE TABLE  IF NOT EXISTS  Messages(username VARCHAR(100),msg VARCHAR(100),phoneNumber VARCHAR(100),DeviceCode VARCHAR(100), MsgTimeStamp VARCHAR(100),msgCheckSum VARCHAR(100))"
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
            return "success"
        
        
class ManageMessages:
    def Messages(mycode,chatcode):
        check = f"SELECT * FROM Messages"# WHERE DeviceCode='{chatcode}'"
        messages = cursor.execute(check).fetchall()
        MessagesList=[]
        
        if not messages:
            return "None"
        else:
            print("hellosdf")
            
            for message in messages:
                print(message)
                print(message)
                messageDict={}
                messageDict['deviceID']=message["DeviceCode"]
                messageDict['username']=message["username"]    
                messageDict['time']=message["MsgTimeStamp"]
                messageDict['checksum']=message["msgCheckSum"]
                messageDict['msg']=message["msg"]
                if message["DeviceCode"]==mycode:
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
        
class generate:
    def DeviceID(length):
        code=""
        for i in range(0,length):
            code+=str(random.randint(0,9))
        return code