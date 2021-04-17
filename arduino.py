import cv2
import pyrebase
import  tiltModule as TM

#############################
camw, camh = 960, 720
#############################



firebaseConfig = {
    "apiKey": "AIzaSyA1501tS1oe8YF-F7CCeFosUbCCovPrq9Q",
    "authDomain": "python1-f0771.firebaseapp.com",
    "databaseURL": "https://python1-f0771-default-rtdb.firebaseio.com",
    "projectId": "python1-f0771",
    "storageBucket": "python1-f0771.appspot.com",
    "messagingSenderId": "696223136031",
    "appId": "1:696223136031:web:3fb6e65719ad2edcdfd82a",
    "measurementId": "G-BVK3PECXBR"
  }
firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
vid = cv2.VideoCapture(0)
vid.set(3, camw)
vid.set(4, camh)

detector = TM.tilt(SendToFirebase= True)
firebasevals = []
with open("firebase.csv", 'r') as f:
    dataline = f.readlines()
    for line in dataline:
        print(line)
        lines = line.split('=')
        print(lines[1])
        firebasevals.append(lines[1])
detectionStatus = "unkown"
while True :
    success, frame = vid.read()
    frame = detector.findTilt(frame= frame)[0]
    cv2.imshow("video", frame)
    cv2.waitKey(1)