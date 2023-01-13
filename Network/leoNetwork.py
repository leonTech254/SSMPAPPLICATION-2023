import requests
import urllib
from kivy.network.urlrequest import UrlRequest
import sqlite3

conn = sqlite3.connect("hashDatabase.db")
cursor=conn.cursor()
conn.row_factory = sqlite3.Row
class serverStore:
    chatcode=''
    orcode=''
    newMessages="none"    
class Server2:
    def on_success(req, result):
        check=f"SELECT * FROM messages WHERE chatKey='{serverStore.chatcode}' OR chatKey='{serverStore.orcode}'"
        localmessages = cursor.execute(check).fetchall()
        contents=result
        messages=contents['messages']
        if len(messages)>len(localmessages):
            # q="DELETE FROM messages"
            # cursor.execute(q)
            # conn.commit()
            rowAdded=len(messages)-len(localmessages)
            messages.reverse()
            messages=messages[:rowAdded]
            for message in messages:
                msg=message['msg']
                time=message['time']
                user=message['user']
                chatKey=message['username']
                phone='g'
                code=message['deviceID']
                date=message['time']
                checksum=message['checksum']
                users="INSERT INTO Messages('chatKey','msg','phoneNumber','DeviceCode','MsgTimeStamp','msgCheckSum') VALUES(?,?,?,?,?,?)"
                values=(f'{code}',f'{msg}',f'{phone}',f'{code}',f'{date}',f'{checksum}')
                cursor.execute(users, values)
                conn.commit()
            # updating the chatList
            msg=messages[0]
            username=msg['username']
            date=msg['time']
            message=message['msg']
            code=serverStore.chatcode.split('-')[1]
            query=f"UPDATE Chats SET MsgTimeStamp='{date}', msg='{message}' WHERE DeviceCode='{code}'"
            conn.execute(query)
            conn.commit()
            
            
            
            serverStore.newMessages='new'
            
            
            

        Server2.LoadConversation(serverStore.chatcode,serverStore.orcode)
    def on_failure(req, result):
        # Handle failure
        
        return "false"
    def LoadConversation(chatCode,orCode):
        serverStore.chatcode=chatCode
        serverStore.orcode=orCode
        data = {'chatcode':chatCode,'orcode':orCode}
        # params = urllib.parse.urlencode(data)
        url='http://127.0.0.1:5000/ssmp/load/conversation'
        params = urllib.parse.urlencode(data)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/plain'}
        req = UrlRequest(url, on_success=Server2.on_success, req_body=params,
                            req_headers=headers)
    def newMessages():
        return serverStore.newMessages
    def closeMessage():
        serverStore.newMessages='none'
        
    
    
    # def SendMessage(chatCode,orCode):
    #     serverStore.chatcode=chatCode
    #     serverStore.orcode=orCode
    #     data = {'chatcode':chatCode,'orcode':orCode}
    #     # params = urllib.parse.urlencode(data)
    #     url='http://127.0.0.1:5000/ssmp/messages'
    #     params = urllib.parse.urlencode(data)
    #     headers = {'Content-type': 'application/x-www-form-urlencoded',
    #                 'Accept': 'text/plain'}
    #     req = UrlRequest(url, on_success=Server2.on_success, req_body=params,
    #                         req_headers=headers)
    
        
       
        
        


    
     
            
        
        
 