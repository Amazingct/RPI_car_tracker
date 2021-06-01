from flask import Flask, request, Response, send_file
import cv2
import time, json, os
'''   
import pyrebase
config = {
    "apiKey": "AIzaSyAGvaBLvQAjJAMBLgZkRPYtkhBbgYnqaPU",
    "authDomain": "finalbin-35e3c.firebaseapp.com",
    "databaseURL": "https://finalbin-35e3c-default-rtdb.firebaseio.com",
    "projectId": "finalbin-35e3c",
    "storageBucket": "finalbin-35e3c.appspot.com",
    "messagingSenderId": "887888512503",
    "appId": "1:887888512503:web:b987d613ed083aee569af2",
    "measurementId": "G-GX8J1JVNC5"}

fire_base = pyrebase.initialize_app(config)
auth = fire_base.auth()
database = fire_base.database()
'''


# Major functions
def get_gps():
    pass

def update_gps_firebase():
    pass

def buzzer(state):
    pass

def capture_image():
    image = cv2.VideoCapture(0)
    result = True
    while result:
        ret, frame = image.read()
        image_name = "data/images/capture.jpg"
        cv2.imwrite(image_name, frame)
        result = False
    image.release()
    cv2.destroyAllWindows()


app = Flask(__name__)


@app.route("/capture", methods=['GET'])
def capture():
    capture_image()
    return send_file("data/images/capture.jpg")


@app.route("/alarm", methods=['POST'])
def alarm():
    state = request.args.get('alarm')
    buzzer(int(state))
    return "done"




@app.route("/")
def home():
    return "RPI CAR TRACKER"


if __name__ == '__main__':
    app.run()
