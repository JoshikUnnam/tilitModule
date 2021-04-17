import cv2
import mediapipe as medpie
import time
import numpy as np

cap = cv2.VideoCapture(0)
mphands = medpie.solutions.hands
hand = mphands.Hands(max_num_hands=2)
mpDraw = medpie.solutions.drawing_utils

pTime = 0
cTime = 0

while True :
    success, frame = cap.read()
    print(frame.shape[1], frame.shape[0])

    my_img_1 = np.zeros((480, 640, 3), dtype="uint8")
    cv2.imshow('Single Channel Window', my_img_1)
    RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(RGBframe)
    if results.multi_hand_landmarks :
        for handlms in results.multi_hand_landmarks :

            for id , lm in enumerate(handlms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cy, cx)

                # id == 4 :
                #   cx1, cy1 = cx, cy
                #if id == 8 :
                #   cv2.line(frame, (cx1, cy1), (cx, cy), (255, 0, 255), 3)
                cv2.circle(frame, (cx, cy), 7,(0, 0, 255),cv2.FILLED )
                #mpDraw.draw_landmarks(frame, handlms, mphands.HAND_CONNECTIONS)
    cTime = time.time()
    if cTime != pTime :
        fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 2)
    cv2.imshow('video', frame)
    cv2.waitKey(1)

