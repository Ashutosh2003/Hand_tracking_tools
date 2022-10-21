import cv2
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
detector = htm.handDetector(max_hands=2,trackCon=0.8,detectionCon=0.8)

#VOL Things
interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
range = volume.GetVolumeRange()
minVol = range[0]
maxVol = range[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        finglst = detector.fingersUP(lmList)
        #print(lmList[4])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[12][1], lmList[12][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1,y1), 10, (255,0,0), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,0), cv2.FILLED)
        cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,0))

        length = np.hypot((x2-x1), (y2-y1))
        length2 = np.hypot((x3-x2), (y3-y2))
        #print(length, length2)
        if length < 25:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        if finglst[2] == 0 and finglst[3] == 0 and finglst[4] == 0:
            cv2.circle(img, (x3, y3), 10, (0, 255, 0), cv2.FILLED)
            vol = np.interp(length,[10,130],[minVol,maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            print(vol)


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break