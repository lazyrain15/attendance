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
    sql = "INSERT INTO data_attendance (userId, dateTime, status, type) VALUES (%s, %s, %s, %s)"
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


def runView(idUser='Waiting...', nameUser='Waiting...', typeFinger='Waiting', dateTimeFinger='Waiting...',  typeView='0', counter='0'):
    global userId, userName, fingerType, fingerDateTime
    try:
        if typeView == '0':
            userId = Label(root2, text=f'ID : {idUser}', )
            userId.place(relx=0.5,
                         rely=0.29,
                         anchor='center')
            userId.config(font=('Arial italic', 20), bg='white',
                          borderwidth=3, relief='solid', padx=10, pady=8, background='white')

            userName = Label(root2, text=f'Nama : {nameUser}', )
            userName.place(relx=0.5,
                           rely=0.4,
                           anchor='center')
            userName.config(font=('Arial', 26, 'bold'),
                            borderwidth=2, relief='solid', padx=20, pady=20, background='white')

            fingerType = Label(root2, text=f'{typeFinger}')
            fingerType.place(relx=0.5, rely=0.515, anchor='center')
            fingerType.config(font=('Arial', 22, 'bold'), borderwidth=3,
                              relief='sunken', padx=15, pady=8, background='white')

            fingerDateTime = Label(root2, text=f'{dateTimeFinger}')
            fingerDateTime.place(relx=0.5, rely=0.6, anchor='center')
            fingerDateTime.config(font=('Arial', 21, 'bold'),
                                  borderwidth=10, relief='ridge', padx=10, pady=8, background='white')
        if typeView != '0':
            if typeView == '3':
                userId.destroy()
                userName.destroy()
                fingerType.destroy()
                fingerDateTime.destroy()

            userId = Label(root2, text=f'ID : {idUser}', )
            userId.place(relx=0.5,
                         rely=0.29,
                         anchor='center')
            userId.config(font=('Arial italic', 20), bg='white',
                          borderwidth=3, relief='solid', padx=10, pady=8, background='white')

            userName = Label(root2, text=f'Nama : {nameUser}', )
            userName.place(relx=0.5,
                           rely=0.4,
                           anchor='center')
            userName.config(font=('Arial', 26, 'bold'),
                            borderwidth=2, relief='solid', padx=20, pady=20, background='white')

            fingerType = Label(root2, text=f'{typeFinger}')
            fingerType.place(relx=0.5, rely=0.515, anchor='center')
            fingerType.config(font=('Arial', 22, 'bold'), borderwidth=3,
                              relief='sunken', padx=15, pady=8, background='white')

            fingerDateTime = Label(root2, text=f'{dateTimeFinger}')
            fingerDateTime.place(relx=0.5, rely=0.6, anchor='center')
            fingerDateTime.config(font=('Arial', 21, 'bold'),
                                  borderwidth=10, relief='ridge', padx=10, pady=8, background='white')
        print(typeView, idUser)
    except:
        pass


root2 = tk2.Tk()
root2.geometry('600x600')
root2.title('Attendance User')
root2.resizable(FALSE, FALSE)
bg = PhotoImage(
    file="C:\\Users\\HP\\Pictures\\PT SEFONG INDUSTRIES_LOGO\\PT_SEFONG_rB.png")
root2.geometry('600x600')
lbl_bg = Label(root2, image=bg)
lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
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
            dateTime = dataString[(x + 2):y]
            status = dataString[(y + 1):z]
            fingerType = dataString[(z + 2):a]

            print('UserID : ' + userId + ' DateTime : ' +
                  dateTime + ' Status : ' + status + ' Type : ' + fingerType)
            textMssg = f"UserID :  {userId} Type :  {('Masuk' if fingerType == '0' else 'Pulang')} DateTime :  {dateTime}"
            typeFinger = 'Masuk' if fingerType == '0' else 'Pulang'
            typeCount = '3'
            showMessage(textMssg, 'info', 4000)

            cursor = db.cursor()
            sql = f"SELECT karyawan.nama_karyawan FROM karyawan WHERE karyawan.id_karyawan = '{userId}' ORDER BY id_karyawan DESC LIMIT 1"
            cursor.execute(sql)
            myresult = cursor.fetchall()
            print(dateTime)
            namaKaryawan = myresult[0][0]

            runView(f'{userId}', f'{namaKaryawan}',
                    f'{typeFinger}', f'{dateTime}', 3)
            showMessage(textMssg, 'info', 100)
            saveData(userId, dateTime, status, fingerType)
        i += 1
except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
