import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time

class DetectAttendance:
    def detectAttendance(self):
        path = r'C:\Users\shibi\PycharmProjects\Mini_Project_G9\Samples'
        images = []
        className = []

        myList = os.listdir(path)
        print(myList)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            className.append(os.path.splitext(cl)[0])
        print(className)


        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                try:
                    encode = face_recognition.face_encodings(img)[0]
                except IndexError as e:
                    print(e)
                    exit(1)
                print(len(encode))
                encodeList.append(encode)
            return encodeList


        def markAttendance(name):
            with open('attendance.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S:')
                    f.writelines(f'\n{name}, {dtString}')


        encodeListKnown = findEncodings(images)
        print('Encoding Complete')

        # cap = cv2.VideoCapture(0)

        # while True:
        #     success, img = cap.read()
        #     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        #     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        #     facesCurFrame = face_recognition.face_locations(imgS)
        #     encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        #
        #     for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        #         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        #         faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
        #         print(faceDist)
        #         matchIndex = np.argmin(faceDist)
        #
        #         if matches[matchIndex]:
        #             name = className[matchIndex].upper()
        #             print(name)
        #             y1, x2, y2, x1 = faceLoc
        #             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        #             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #             cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        #             cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        #             markAttendance(name)
        #
        #
        #     cv2.imshow('Webcam', img)
        #     cv2.waitKey(1)

        img_path = r'C:\Users\shibi\PycharmProjects\Mini_Project_G9\shots'
        dir_path = r'C:\Users\shibi\PycharmProjects\Mini_Project_G9\shots'
        imageList = os.listdir(img_path)

        for images in imageList:
            count = 0
            new_path = img_path + '\\' + imageList[count]

            count += 1

            print(new_path)
            img = cv2.imread(new_path)

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDist)
                matchIndex = np.argmin(faceDist)

                if matches[matchIndex]:
                    name = className[matchIndex].upper()
                    print(name)
                    print("Detection complete")
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)
        # delete the files in the shots directory
        print('Program complete')
        # sleep for 2 secs
        time.sleep(2)

        # delete the shots directory
