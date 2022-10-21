import cv2
import time
import mediapipe as mp



class handDetector():
    def __init__(self, mode=False, max_hands=2, complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
        return lmList

    def fingersUP(self, lmList = []):
        tipIds = [4, 8, 12, 16, 20]
        finglst = [0, 0, 0, 0, 0]
        if len(lmList) != 0:
            # THUMB
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                finglst[0] = 1
            else:
                finglst[0] = 0
            # Fingers
            for i in range(1, len(tipIds)):
                if lmList[tipIds[i]][2] < lmList[tipIds[i] - 2][2]:
                    finglst[i] = 1
                else:
                    finglst[i] = 0
        return finglst

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector(max_hands=2,trackCon=0.75,detectionCon=0.75)
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()