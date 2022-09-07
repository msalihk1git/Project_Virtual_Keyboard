
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from pynput.keyboard import Controller
from time import sleep


cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=HandDetector(detectionCon=0.8)

keyboard_keys=[["Q","W","E","R","T","Y","U","I","O","P"],
                ["A","S","D","F","G","H","J","K","L",":"],
                ["Z","X","C","V","B","N","M",",",".","/"]]

final_text=""
keyboard=Controller()




def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1],
                                                   button.size[0],button.size[0]), 20 ,rt=0)
        cv2.rectangle(img, button.pos, (int(x + w), int(y + h)), (255, 144, 30), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    return img


class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos=pos
        self.size=size
        self.text=text

buttonList=[]

for k in range(len(keyboard_keys)):
    for x,key in enumerate(keyboard_keys[k]):
        buttonList.append(Button([100*x+25,100*k+50],key))
# print(buttonList)


while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    img=detector.findHands(img)
    lmlist,bboxinfo=detector.findPosition(img)
    # print(lmlist)
    # img=draw(img,buttonList)
    img = draw(img, buttonList)
    if lmlist:
        for button in buttonList:
            x,y=button.pos
            w,h=button.size
            # print(x,y)
            if x<lmlist[8][0]<x+w and y<lmlist[8][1]<y+h:
                cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,255),cv2.FILLED)
                cv2.putText(img,button.text,(x+20,y+50),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)
                length,_,_ =detector.findDistance(8,12,img)
                # print(length)

                if length<35:
                    keyboard.press(button.text)
                    final_text+=button.text
                    # print(final_text)
    

    cv2.rectangle(img,(80,400),(1000,400),(255,255,255),cv2.FILLED)
    cv2.putText(img,final_text,(60,450),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)




    cv2.imshow("keyboard",img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
