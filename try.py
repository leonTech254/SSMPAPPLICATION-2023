import sqlite3
from LeoDataCheck.datacheck import generate
conn=sqlite3.connect("hashDatabase.db")
cursor = conn.cursor()


# for i in range(1,6):
#     users="INSERT INTO Messages('username','msg','phoneNumber','DeviceCode','MsgTimeStamp','msgCheckSum') VALUES(?,?,?,?,?,?)"
#     code=generate.DeviceID(length=2)
#     values=(f'jose+{code}','hello my name is jose','12345678',f'{code}','20:59','nswndw242ndwk')
#     cursor.execute(users, values)
#     conn.commit()

for i in range(1,6):
    users="INSERT INTO Chats('username','msg','DeviceCode','MsgTimeStamp') VALUES(?,?,?,?)"
    code=generate.DeviceID(length=2)
    values=(f'leon+{code}','hello my name is jose',f'{code}','20:59')
    cursor.execute(users, values)
    conn.commit()