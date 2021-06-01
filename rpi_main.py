from flask import Flask, request, Response, send_file
import cv2
import pyrebase
config = {
    "apiKey": "AIzaSyBUmN6mlS0IdM9cf5rghIyU_MyZ_vz8SKU",
    "authDomain": "rpi-car-tracker.firebaseapp.com",
    "databaseURL": "https://rpi-car-tracker-default-rtdb.firebaseio.com",
    "projectId": "rpi-car-tracker",
    "storageBucket": "rpi-car-tracker.appspot.com",
    "messagingSenderId": "67371868058",
    "appId": "1:67371868058:web:919cb18cee9eb0a85b2423",
    "measurementId": "G-X2PC0NSXNV"
}

fire_base = pyrebase.initialize_app(config)
auth = fire_base.auth()
database = fire_base.database()


# Major functions
def get_gps():
    pass

def update_gps_firebase(lat, long):
    pass

def buzzer(state):
    if state == 1:
        return "alarm turned on"
    else:
        return "alarm turned off"

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
    return buzzer(int(state))




@app.route("/")
def home():
    return "RPI CAR TRACKER"


if __name__ == '__main__':
    app.run()
