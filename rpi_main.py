from flask import Flask, request, Response, send_file
import cv2
import pyrebase, time
import threading as t
config = {
    "apiKey": "AIzaSyC_DC3erAG6oaHt3v9YdBUEliLm-3nd7Ds",
    "authDomain": "cartracker-f52df.firebaseapp.com",
    "databaseURL": "https://cartracker-f52df-default-rtdb.firebaseio.com",
    "projectId": "cartracker-f52df",
    "storageBucket": "cartracker-f52df.appspot.com",
    "messagingSenderId": "697426173079",
    "appId": "1:697426173079:web:379fa3a26d436672f71dd2",
    "measurementId": "G-L4H00531P4"

}

fire_base = pyrebase.initialize_app(config)
auth = fire_base.auth()
database = fire_base.database()


# Major functions
def get_gps():
    # get from module
    return {"lat": 33.4, "long": -66.9}

def update_gps_firebase():
    print("Update started..")
    while True:
        database.child("track").update(get_gps())
        time.sleep(1)

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


t.Thread(target=update_gps_firebase).start()

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
