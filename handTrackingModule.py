import cv2
import mediapipe as mp
import time



class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw = False ):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
               # print(id, cy, cx)
                lmlist.append([id, cx, cy])
                if draw :
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                # id == 4 :
                #   cx1, cy1 = cx, cy
                # if id == 8 :
                #   cv2.line(frame, (cx1, cy1), (cx, cy), (255, 0, 255), 3)
        return lmlist


def main() :
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        list = detector.findPosition(img)
        if len(list) != 0 :
            print(list[4])
        cTime = time.time()
        if pTime != cTime :
            fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 2)
        cv2.imshow('video', img)
        cv2.waitKey(1)

if __name__ == "__main__" :
    main()