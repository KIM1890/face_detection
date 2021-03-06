import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# luu y cho camera
cam = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainningData.yml")
# id = 0
# set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (203, 23, 252)

# get data from sqlite by ID


def getProfile(id):
    conn = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE ID="+str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


while True:
    # camera read
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_smooth = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    faces = faceDetect.detectMultiScale(gray_smooth, 1.3, 5)
    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        id, conf = rec.predict(gray[y:y+h, x:x+w])

        # set text to window
        if conf < 50:
            profile = getProfile(id)

            if(profile != None):
                # cv2.PutText(cv2.fromarray(img),str(id),(x+y+h),font,(0,0,255),2);
                cv2.putText(
                    img, "Name: " + str(profile[1]), (x, y+h+30), fontface, fontscale, fontcolor, 2)
                cv2.putText(
                    img, "Age: " + str(profile[2]), (x, y+h+60), fontface, fontscale, fontcolor, 2)
                cv2.putText(
                    img, "Gender: " + str(profile[3]), (x, y+h+90), fontface, fontscale, fontcolor, 2)

        else:
            cv2.putText(
                img, "Unknown", (x, y+h+30), fontface, fontscale, fontcolor, 2)

    cv2.imshow('Face', img)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
