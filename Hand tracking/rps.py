import cv2
import HandTrackingModule as htm
import time
import keyboard
import random
import platform

cap = cv2.VideoCapture(0)
detector = htm.handDetector(mode=True, max_hands=1,trackCon=0.75,detectionCon=0.75)

validmoves = [[1,1,1,1,1,], [0,1,1,0,0], [0,0,0,0,0]]
moves = ['Rock', 'Paper', 'Scissor']
CPUscr = 0
Plscr = 0

def checkmove(move):
    if move.count(1) == 5:
        #print('Paper')
        return 1
    if move.count(1) == 2:
        #print('Scissor')
        return 2
    if move.count(1) == 0:
        #print('Rock')
        return 0
while True:
    while True:
        success, img = cap.read()
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            finglst = detector.fingersUP(lmList)
            #print(finglst)
            if finglst in validmoves:
                current_moves = []
                pmoV_i = checkmove(finglst)
                cmoV_i = random.randint(0, 2)
                current_moves.append(pmoV_i)
                current_moves.append(cmoV_i)
                pmov = moves[pmoV_i]
                cmoV = moves[cmoV_i]
                print(f'CPU move: {cmoV}')
                print(f'Player Move: {pmov}')
                if pmoV_i == cmoV_i:
                    print("Tie")
                else:
                    if current_moves != [0,2] and current_moves != [2,0]:
                        if pmoV_i > cmoV_i:
                            print("Player wins")
                            Plscr += 1
                        else:
                            print("CPU wins")
                            CPUscr += 1
                    else:
                        if pmoV_i < cmoV_i:
                            print('Player wins')
                            Plscr += 1
                        else:
                            print("CPU wins")
                            CPUscr += 1
                print(f'CPU Score: {CPUscr}\nPlayer Score: {Plscr}\n________________')
                break
    #time.sleep(2)
    if platform.system() == 'Linux':

        from pynput.keyboard import Key, Listener
 
        def show(key):

            if key == Key.delete:
                # Stop listener
                quit()
            else:
                return False
                
        # Collect all event until released
        with Listener(on_press = show) as listener:  
            listener.join()
    else:
        if keyboard.read_key() == "q":
            quit()

