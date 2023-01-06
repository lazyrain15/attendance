import tkinter as tk2
from zk import ZK
import os
import sys
import mysql.connector
from tkinter import *

# Connect to Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="absensi"
)


def saveData(user_id, timestamp, status, punch):
    cursor = db.cursor()
    sql = "INSERT INTO finger (userId, dateTime, status, type) VALUES (%s, %s, %s, %s)"
    val = (user_id, timestamp, status, punch)
    cursor.execute(sql, val)

    db.commit()


def showMessage(message, type='info', timeout=2500):
    import tkinter as tk
    from tkinter import messagebox as msgb

    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        if type == 'info':
            msgb.showinfo('Info', message, master=root)
        elif type == 'warning':
            msgb.showwarning('Warning', message, master=root)
        elif type == 'error':
            msgb.showerror('Error', message, master=root)
    except:
        pass


def runView(msg='Welcome...', type=0):
    global label1
    try:
        if type == 0:
            label1 = Label(root2, text=msg)
            label1.pack()
        if type > 0:
            if type == 3:
                label1.destroy()
            label1 = Label(root2, text=msg)
            label1.pack()
        print(type, msg)
    except:
        pass


root2 = tk2.Tk()
root2.geometry('600x600')
runView()


CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

conn = None
zk = ZK('192.168.100.201', port=4370)
try:
    conn = zk.connect()
    print('Connected! waiting...')
    i = 1
    for attendance in conn.live_capture():
        if attendance is None:
            print(f'Waiting for user finger... ({i})')
            showMessage('Waiting for user finger...')
        else:
            attendances = str(attendance)
            print(attendances)

            dataString = attendances.replace('<Attendance>:', '')

            getUserId = ':'
            getDateTime = '('
            getStatus = ','
            getType = ')'

            x = dataString.find(getUserId)
            y = dataString.find(getDateTime, x)
            z = dataString.find(getStatus, y)
            a = dataString.find(getType, z)

            userId = dataString[1:(x-1)]
            dateTime = dataString[(x + 1):y]
            status = dataString[(y + 1):z]
            fingerType = dataString[(z + 2):a]

            print('UserID : ' + userId + ' DateTime : ' +
                  dateTime + ' Status : ' + status + ' Type : ' + fingerType)
            textMssg = f"UserID :  {userId} Type :  {('Masuk' if fingerType == '0' else 'Pulang')} DateTime :  {dateTime}"
            runView(textMssg, 3)
            showMessage(textMssg, 'info', 4000)
            saveData(userId, dateTime, status, fingerType)
        i += 1
except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
