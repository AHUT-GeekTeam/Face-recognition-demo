#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import base64
import cv2
from multiprocessing import Process,Queue
from aip import AipFace

APP_ID = '******'
API_KEY = '******'
SECRET_KEY = '******'
imageType = "BASE64"
groupIdList = '******'
filePath = "face.jpg"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
x_const = int(video.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
y_const = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)

def video_show(i = 1):
 # cv2.namedWindow("face", cv2.WINDOW_NORMAL) 
 # cv2.setWindowProperty("face", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
 while True:
    time = cv2.getTickCount()
    ret,cap = video.read()
    i = i + 1
    if i == 20:
         i = 0
         if Tx.empty():
           cv2.imwrite("face.jpg",cap)
           Tx.put(i)
    try:
         Rx.get_nowait()
         cv2.putText(cap,"Access",(x_const-85,y_const - 150), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 2)
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
    cv2.putText(cap, "FPS:%s"%int(cv2.getTickFrequency()/(cv2.getTickCount()-time)), (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.imshow('face',cap)
    a = cv2.waitKey(1)
    if a == ord('c') or a == ord('C'):
        break
 video.release()
 cv2.destroyAllWindows()

def face_compare(Tx,Rx):
 while True:
     Tx.get()
     with open(filePath,"rb") as f:
          data = base64.b64encode(f.read())
     image = str(data,'UTF-8')
     options = {"liveness_control":"HIGH"}
     result = client.search(image, imageType, groupIdList,options)
     if "SUCCESS" in result["error_msg"] and result["result"]["user_list"][0]["score"] >= 80:
          Rx.put(True)

if __name__ == '__main__':
    Tx = Queue(1)
    Rx = Queue(1)
    p = Process(target = face_compare,args = (Tx,Rx),daemon = True)
    p.start()
    video_show()
