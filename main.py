#! D:\FaceAttendanceSystem\myenv\Scripts\python.exe

import datetime
from urllib import request
import cv2
import cvzone
import face_recognition
import os
import pickle
import numpy as np
import requests

from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancesystem-7fa78-default-rtdb.firebaseio.com/"
})


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources\AttendanceBG.png')

# Importing the mode images into a list
folderModePath = 'Resources\Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load the encoding file
print("Loading Encode File.....")
file = open('EncodeFile.p', 'rb')
encodingListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodingListKnownWithIds
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    # Resize the image to 1/4th of its original size to improve processing speed
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Find face locations and encodings in the resized image
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Overlay the webcam image on the background
    imgBackground[183:183+480, 44:44+640] = img
    imgBackground[15:15+688, 788:788+475] = imgModeList[modeType]

    if faceCurFrame:
        # Loop through all detected faces
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                # Get the face location coordinates from the resized image
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale coordinates to match full-size image

                # Create a bounding box around the face with scaling applied
                bbox = 44 + x1, 183 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading..", (64, 643))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        # Get the data for first frame only
        if counter != 0:
            if counter == 1:
                # Get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the image for cloudinary
                response = requests.get(studentInfo['profile_image'], stream=True)
                array = np.frombuffer(response.content, np.uint8)
                img_bgr = cv2.imdecode(array, cv2.IMREAD_COLOR)
                imgStudent = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2BGR)  

                # Update data for attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])            
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 
                else:
                    modeType = 2
                    counter = 0
                    imgBackground[15:15+688, 788:788+475] = imgModeList[modeType]
            if modeType != 2:
                if 10 < counter <= 20:
                    modeType = 3
                
                imgBackground[15:15+688, 788:788+475] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                
                    cv2.putText(imgBackground, str(studentInfo['department']), (1073, 538), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (991, 475), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (850, 668), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1020, 668), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1170, 668), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    # Center the name
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (475-w)//2
                    cv2.putText(imgBackground, str(studentInfo['name']), (790+offset, 130), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                    resized_img = cv2.resize(imgStudent, (268, 268), interpolation=cv2.INTER_LINEAR)
                    imgBackground[154:154+268, 893:893+268] = resized_img
                counter += 1

                # Active and reset everthing
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[15:15+688, 788:788+475] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    # Display the resulting image
    cv2.imshow("Face Attendance", imgBackground)

    # Check if the user clicked the close button on the window
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to close
        break

# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
