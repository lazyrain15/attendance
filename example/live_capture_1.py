# -*- coding: utf-8 -*-
from zk import ZK
import os
import sys
import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="absensi"
)

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

conn = None
zk = ZK('192.168.100.201', port=4370)
try:
    conn = zk.connect()
    print('Connected! waiting...')
    for attendance in conn.live_capture():
        if attendance is None:
            pass
        else:
            attendances = str(attendance)
            print(attendances)
            messagebox.showwarning('Title', 'Data')
except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()

mainloop()
