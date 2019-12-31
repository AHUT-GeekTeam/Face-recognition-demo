#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import base64
import cv2
from multiprocessing import Process,Queue
from aip import AipFace

APP_ID = '******'
API_KEY = '******'
SECRET_KEY = '******'
groupIdList = '******'
imageType = "BASE64"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
x_const = int(video.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
y_const = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
scalar = 5

def video_show(i = 1):
 # cv2.namedWindow("face", cv2.WINDOW_NORMAL) 
 # cv2.setWindowProperty("face", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
 while True:
    time = cv2.getTickCount()
    _,cap = video.read()
    img = cv2.resize(cap,(int(x_const*2/scalar),int(y_const*2/scalar)))
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray,scaleFactor=1.1,minNeighbors=5)
    i = i + 1
    if i == 20:
        i = 0
        if Tx.empty() and len(faces):
            Tx.put(str(base64.b64encode(cv2.imencode(".jpg",img)[1].tostring()),'UTF-8'))

    for (x,y,w,h) in faces:
        x *= scalar
        y *= scalar
        w *= scalar
        h *= scalar
        cv2.rectangle(cap,(x,y),(x+w,y+h),(255,0,0),2)

    try:
        Rx.get_nowait()
        cv2.putText(cap,"Access",(x_const-85,y_const-150),cv2.FONT_HERSHEY_SIMPLEX,1.6,(0,0,255),2)
        '''put your main code here'''
    except:
        pass

    cv2.line(cap,(x_const-100,y_const+100),(x_const-100,y_const+80),(0,255,0),2)
    cv2.line(cap,(x_const-100,y_const+100),(x_const-80,y_const+100),(0,255,0),2)
    cv2.line(cap,(x_const+100,y_const+100),(x_const+80,y_const+100),(0,255,0),2)
    cv2.line(cap,(x_const+100,y_const+100),(x_const+100,y_const+80),(0,255,0),2)
    cv2.line(cap,(x_const+100,y_const-100),(x_const+100,y_const-80),(0,255,0),2)
    cv2.line(cap,(x_const+100,y_const-100),(x_const+80,y_const-100),(0,255,0),2)
    cv2.line(cap,(x_const-100,y_const-100),(x_const-100,y_const-80),(0,255,0),2)
    cv2.line(cap,(x_const-100,y_const-100),(x_const-80,y_const-100),(0,255,0),2)
    cv2.line(cap,(x_const-100,y_const-100+i*10),(x_const+100,y_const-100+i*10),(0,255,0),2)
    cv2.putText(cap, "FPS:%d"%int(cv2.getTickFrequency()/(cv2.getTickCount()-time)), (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.imshow('face',cap)
    a = cv2.waitKey(1)
    if a == ord('c') or a == ord('C'):
        break
 video.release()
 cv2.destroyAllWindows()

def face_compare(Tx,Rx):
 while True:
     options = {"liveness_control":"HIGH"}
     try:
         result = client.search(Tx.get(), imageType, groupIdList,options)
     except:
         continue
     if "SUCCESS" in result["error_msg"] and result["result"]["user_list"][0]["score"] >= 80:
          Rx.put(True)

if __name__ == '__main__':
    Tx = Queue()
    Rx = Queue()
    p = Process(target = face_compare,args = (Tx,Rx),daemon = True)
    p.start()
    video_show()
