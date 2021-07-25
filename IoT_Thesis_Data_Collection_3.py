import tkinter as tk
import xlwt
from xlwt import Workbook
from datetime import datetime
import socket

import numpy as np
import pandas as pd


def HSCalulation(st, bt, spo2):
    if(st>=27 and st<=32):
        if((bt>=38 and bt<39) or (spo2<=75 and spo2 >=73)):
            hs=2
        elif((bt>=39 and bt<41) or (spo2<=72 and spo2 >=70)):
            hs=3
        elif((bt>=41 and bt<=42) or (spo2<=69 and spo2 >=65)):
            hs=4
        elif((bt>42) or (spo2<65)):
            hs=5
        else:
            hs=1
    elif(st>32 and st<=41):
        if((bt>=38 and bt<41) or (spo2<=75 and spo2 >=70)):
            hs=3
        elif((bt>=41 and bt<=42) or (spo2<=69 and spo2 >=65)):
            hs=4
        elif((bt>42) or (spo2<65)):
            hs=5
        else:
            hs=1
    elif(st>41 and st<=54):
        if((bt>=38 and bt<=42) or (spo2<=75 and spo2 >=65)):
            hs=4
        elif((bt>42) or (spo2<65)):
            hs=5
        else:
            hs=1
    elif(st>54):
        if((bt>=38 and bt<39) or (spo2<=75 and spo2 >=73)):
            hs=4
        elif((bt>=39) or (spo2<73)):
            hs=5
        else:
            hs=1
    else:
        hs=1
    return hs

def Draw():
    global hr_value,sbp_value,dbp_value,bt_value,st_value,hs_value,spo2_value
    
    hr_frame=tk.Frame(root,width=250,height=60,relief='solid',bd=1)
    hr_frame.place(x=10,y=50)
    hr_text=tk.Label(hr_frame,text='Heart Rate:',font='Helvetica 16')
    hr_text.pack()
    hr_value=tk.Label(hr_frame,text='0',font='Helvetica 16')
    hr_value.pack()
    hr_frame.pack_propagate(0)

    sbp_frame=tk.Frame(root,width=250,height=60,relief='solid',bd=1)
    sbp_frame.place(x=270,y=50)
    sbp_text=tk.Label(sbp_frame,text='Systolic Blood Pressure:',font='Helvetica 16')
    sbp_text.pack()
    sbp_value=tk.Label(sbp_frame,text='0',font='Helvetica 16')
    sbp_value.pack()
    sbp_frame.pack_propagate(0)

    dbp_frame=tk.Frame(root,width=250,height=60,relief='solid',bd=1)
    dbp_frame.place(x=530,y=50)
    dbp_text=tk.Label(dbp_frame,text='Diastolic Blood Pressure:',font='Helvetica 16')
    dbp_text.pack()
    dbp_value=tk.Label(dbp_frame,text='0',font='Helvetica 16')
    dbp_value.pack()
    dbp_frame.pack_propagate(0)

    bt_frame=tk.Frame(root,width=250,height=60,relief='solid',bd=1)
    bt_frame.place(x=10,y=120)
    bt_text=tk.Label(bt_frame,text='Body Temperature:',font='Helvetica 16')
    bt_text.pack()
    bt_value=tk.Label(bt_frame,text='0',font='Helvetica 16')
    bt_value.pack()
    bt_frame.pack_propagate(0)

    st_frame=tk.Frame(root,width=250,height=60,relief='solid',bd=1)
    st_frame.place(x=270,y=120)
    st_text=tk.Label(st_frame,text='Surrounding Temperature:',font='Helvetica 16')
    st_text.pack()
    st_value=tk.Label(st_frame,text='0',font='Helvetica 16')
    st_value.pack()
    st_frame.pack_propagate(0)

    hs_frame=tk.Frame(root,width=250,height=60,relief='solid',bd=1)
    hs_frame.place(x=530,y=120)
    hs_text=tk.Label(hs_frame,text='Heat Stroke Level:',font='Helvetica 16')
    hs_text.pack()
    hs_value=tk.Label(hs_frame,text='0',font='Helvetica 16')
    hs_value.pack()
    hs_frame.pack_propagate(0)

    spo2_frame=tk.Frame(root,width=250,height=60,relief='solid',bd=1)
    spo2_frame.place(x=270,y=190)
    spo2_text=tk.Label(spo2_frame,text='SpO2 Level:',font='Helvetica 16')
    spo2_text.pack()
    spo2_value=tk.Label(spo2_frame,text='0',font='Helvetica 16')
    spo2_value.pack()
    spo2_frame.pack_propagate(0)

def get_data(i):
    global data,hr,sbp,dbp,bt,st,hs,spo2,j
    client, address = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            dataRec = json.loads(data)
            hr = dataRec["hr"]
            sbp = dataRec["sbp"]
            dbp = dataRec["dbp"]
            bt = dataRec["bt"]
            st = dataRec["st"]
            spo2 = dataRec["spo2"]

    bt = round(bt,2)
    hs = HSCalulation(st, bt, spo2)
    now = datetime.now()
    sheet1.write(j,0,now)
    sheet1.write(j,1,age)
    sheet1.write(j,2,gender)
    sheet1.write(j,3,hr)
    sheet1.write(j,4,sbp)
    sheet1.write(j,5,dbp)
    sheet1.write(j,6,bt)
    sheet1.write(j,7,st)
    sheet1.write(j,8,spo2)
    sheet1.write(j,9,hs)
    j = j+1
    
def Refresher():
    get_data()    
    hr_value.configure(text=str(hr)+" bpm")
    sbp_value.configure(text=str(sbp)+" mmHg")
    dbp_value.configure(text=str(dbp)+" mmHg")
    bt_value.configure(text=str(bt)+u"\N{DEGREE SIGN}C")
    st_value.configure(text=str(st)+u"\N{DEGREE SIGN}C")
    hs_value.configure(text=hs)
    spo2_value.configure(text=str(spo2)+"%")
    root.after(5000, Refresher)

hostMACAddress = '00:1f:e1:dd:08:3d' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

sheet1.write(0, 0, 'DateTime')
sheet1.write(0, 1, 'AGE')
sheet1.write(0, 2, 'Gender')
sheet1.write(0, 3, 'HR')
sheet1.write(0, 4, 'SBP')
sheet1.write(0, 5, 'DBP')
sheet1.write(0, 6, 'BT')
sheet1.write(0, 7, 'ST')
sheet1.write(0, 8, 'SpO2')
sheet1.write(0, 9, 'HS')

j = 1
age = 18
gender = 1

root=tk.Tk()
root.title('IoT thesis data collection')
root.geometry("800x270+10+10")
root['bg']='#49A'
Draw()
Refresher()
root.mainloop()
wb.save('D16P2.xls')
