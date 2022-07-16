import datetime
import os

import cv2
from flask import Flask, render_template, Response, request
from attendance_marking import DetectAttendance

global capture, switch
import os

capture = 0
switch = 1


dir_path = r'C:\Users\shibi\PycharmProjects\Mini_Project_G9\shots'

attendance = DetectAttendance()
# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass


# instatiate flask app
app = Flask(__name__, template_folder='./templates')
app.config["CACHE_TYPE"] = "null"

camera = cv2.VideoCapture(0)


def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        if success:
            if capture:
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame)
                print('Detecting person')
                attendance.detectAttendance()
                for files in os.listdir(dir_path):
                    os.remove(dir_path + '\\' + files)

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
        elif request.form.get('stop') == 'Stop/Start':

            if switch == 1:
                switch = 0
                camera.release()
                cv2.destroyAllWindows()

            else:
                # for i in range(1, 501):
                #     print(i)
                camera = cv2.VideoCapture(0)
                switch = 1
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

camera.release()
cv2.destroyAllWindows()     