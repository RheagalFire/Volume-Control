#!/usr/bin/env python
# coding: utf-8

# In[6]:


import time
import cv2
import numpy as np
import HandTrackingModule as htm
import math

cap=cv2.VideoCapture(0)
wCam,hCam=640,480
cap.set(3,wCam)#frame width 
cap.set(4,hCam)#frame Hieght
pTime=0

detector=htm.handDetector(detectionCon=0.8)
## Head over to this https://github.com/AndreMiras/pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
minVol=volRange[0]
maxVol=volRange[1]
###############################################################
print(minVol)
print(maxVol)


volBar = 400
################################################################
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if(len(lmlist)!=0):
        #print(lmlist[4],lmlist[8])
        
        x1,y1=lmlist[4][1],lmlist[4][2]#4 is index finger
        x2,y2=lmlist[8][1],lmlist[8][2]#8 is Thumb
        cv2.circle(img,(x1,y1),8,(255,0,255),cv2.FILLED)#Draw a circle around the index and thumb finger
        cv2.circle(img,(x2,y2),8,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cx,cy=(x1+x2)//2,(y1+y2)//2
        
        cv2.circle(img,(cx,cy),8,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)#Line between thumb and index finger
        #print(length)
        #Hand range 50-300
        #Vol range -65-0
        
        volBar = np.interp(length, [10, 200], [400, 150])#Volume Bar  
        vol=np.interp(length,[10,200],[minVol,maxVol])
        #print(int(length),vol)
        volume.SetMasterVolumeLevel(vol,None)
        if(length<50):
            cv2.circle(img,(cx,cy),8,(0,255,0),cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Img",img)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
cap.release()
cv2.destroyAllWindows()


# In[ ]:




