import cv2
import handTrackingModule as htm
import pyrebase
# this module is used to find the tilt of your hand


class tilt():
    def __init__(self, detection = True, SendToFirebase = False, maxhands = 1, detectionCon = 0.5, trackconf = 0.5):
        self.detector = htm.handDetector(detectionCon=detectionCon, maxHands=maxhands) #hand module used to detect and identify the points on the hand
        self.firebasevalue = SendToFirebase # firebase confermation
    def findTilt(self, frame):
        firebaseConfig = { # firebase configaration to the firebase database
             "apiKey": "AIzaSyA1501tS1oe8YF-F7CCeFosUbCCovPrq9Q",
             "authDomain": "python1-f0771.firebaseapp.com",
             "databaseURL": "https://python1-f0771-default-rtdb.firebaseio.com",
             "projectId": "python1-f0771",
             "storageBucket": "python1-f0771.appspot.com",
             "messagingSenderId": "696223136031",
             "appId": "1:696223136031:web:8aa3053818556f79dfd82a",
             "measurementId": "G-VYSJV75J0R"
        }
        self.firebase = pyrebase.initialize_app(firebaseConfig)
        self.database = self.firebase.database()
        frame = self.detector.findHands(frame)
        location = self.detector.findPosition(frame)
        if len(location) != 0:
            # getting the locations
            i, x, y = location[0]
            i, x1, y1 = location[9]
            i, indexX, indexY = location[12]
            x2, y2 = ((x + x1) // 2), ((y + y1) // 2)
            bx1, bx2 = x2 + 40, x2 - 40
            status = 0
            # checking
            # print(indexY)
            # 110, 850
            # checking cv2.line(frame, (0, indexY), (960, indexY), (255, 0, 0), 4)  # horizontal center line
            # h, w, c = frame.shape
            # print(h)
            cv2.line(frame, (0, 110), (960, 110), (255, 0, 0), 4)  # horizontal center line
            cv2.line(frame, (0, 430), (960, 430), (255, 0, 0), 4)  # horizontal center line
            cv2.line(frame, (x2, 0), (x2, 720), (255, 0, 0), 4)  # vertical center line
            cv2.line(frame, (x, y), (x1, y1), (0, 255, 0), 2)  # center line
            cv2.line(frame, (0, y2), (960, y2), (255, 0, 0), 4)  # horizontal center line
            detectionStatus = "hand detected"
            if self.firebasevalue == True:
                self.database.child("data").child("detection").update({"detectionStatus": detectionStatus})
            if indexX > bx1:
                cv2.putText(frame, "status : right ", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                cv2.line(frame, (bx1, 0), (bx1, 720), (0, 255, 0), 2, )  # threshold 1
                cv2.line(frame, (bx2, 0), (bx2, 720), (0, 255, 0), 2, )  # threshold 2
                status = "right"
                if self.firebasevalue == True:
                    self.database.child("data").child("direction").update({"directionStatus": status})
            elif indexX < bx2:
                cv2.putText(frame, "status : left ", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                cv2.line(frame, (bx1, 0), (bx1, 720), (0, 255, 0), 2, )  # threshold 1
                cv2.line(frame, (bx2, 0), (bx2, 720), (0, 255, 0), 2, )  # threshold 2
                status = "left"
                if self.firebasevalue == True:
                    self.database.child("data").child("direction").update({"directionStatus": status})
            elif indexY < 110:
                cv2.putText(frame, "status : up ", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                cv2.line(frame, (bx1, 0), (bx1, 720), (0, 255, 0), 2, )  # threshold 1
                cv2.line(frame, (bx2, 0), (bx2, 720), (0, 255, 0), 2, )  # threshold 2
                status = "up"
                if self.firebasevalue == True:
                    self.database.child("data").child("direction").update({"directionStatus": status})
            elif y > 430:
                cv2.putText(frame, "status : down ", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                cv2.line(frame, (bx1, 0), (bx1, 720), (0, 255, 0), 2, )  # threshold 1
                cv2.line(frame, (bx2, 0), (bx2, 720), (0, 255, 0), 2, )  # threshold 2
                status = "down"
                if self.firebasevalue == True:
                    self.database.child("data").child("direction").update({"directionStatus": status})
            else:
                cv2.putText(frame, "status : normal ", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                cv2.line(frame, (bx1, 0), (bx1, 720), (0, 0, 255), 2, )  # threshold 1
                cv2.line(frame, (bx2, 0), (bx2, 720), (0, 0, 255), 2, )  # threshold 2
                status = "stationary"
                if self.firebasevalue == True:
                    self.database.child("data").child("direction").update({"directionStatus": status})
            cv2.circle(frame, (x2, y2), 8, (0, 255, 0), cv2.FILLED)  # center point
        else:
            detectionStatus = "hand not detected"
            status = "not detected"
            if self.firebasevalue == True:
                self.database.child("data").child("detection").update({"detectionStatus": detectionStatus})
                self.database.child("data").child("direction").update({"directionStatus": "null"})
            cv2.putText(frame, "status : not detected", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        return frame, status

def main() :
    #############################
    camw, camh = 960, 720
    #############################

    cap = cv2.VideoCapture(0)
    cap.set(3, camw)
    cap.set(4, camh)
    detector = tilt()
    while True:
        success, img = cap.read()
        value = detector.findTilt( frame= img)[1]
        print(value)
        cv2.imshow('video', img)
        cv2.waitKey(1)
if __name__ == '__main__':
    main()