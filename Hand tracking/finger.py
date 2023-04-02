# This program counts the no of fingers raised up in your right hand.

import cv2
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
detector = htm.handDetector(max_hands=2,trackCon=0.75,detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]
finglst = [0, 0, 0, 0, 0]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        # #THUMB
        # if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
        #     finglst[0] = 1
        # else:
        #     finglst[0] = 0
        # #Fingers
        # for i in range(1,len(tipIds)):
        #     if lmList[tipIds[i]][2] < lmList[tipIds[i]-2][2]:
        #         finglst[i] = 1
        #     else:
        #         finglst[i] = 0
        finglst = detector.fingersUP(lmList)
        if finglst == [1,0,1,0,0] or finglst == [0,0,1,0,0]:
            print("Fuck You too!!!")
        else:
            print(f"      {finglst.count(1)}")


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
