from flask import Flask, request, Response, send_file
import cv2
import pyrebase, time
import threading as t
import serial
import time
import pynmea2


port = "/dev/ttyAMA0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)

config = {
    "apiKey": "AIzaSyC_DC3erAG6oaHt3v9YdBUEliLm-3nd7Ds",
    "authDomain": "cartracker-f52df.firebaseapp.com",
    "databaseURL": "https://cartracker-f52df-default-rtdb.firebaseio.com",
    "projectId": "cartracker-f52df",
    "storageBucket": "cartracker-f52df.appspot.com",
    "messagingSenderId": "697426173079",
    "appId": "1:697426173079:web:379fa3a26d436672f71dd2",
    "measurementId": "G-L4H00531P4",
    "serviceAccount":"service.json"
}

fire_base = pyrebase.initialize_app(config)
auth = fire_base.auth()
database = fire_base.database()
storage = fire_base.storage()


# Major functions

def capture_image():
    image = cv2.VideoCapture(0)
    result = True
    while result:
        ret, frame = image.read()
        image_name = "data/images/snap.jpeg"
        cv2.imwrite(image_name, frame)
        result = False
    image.release()
    cv2.destroyAllWindows()
    print("image saved")




def get_gps():
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline()
    newdata = newdata.decode("utf-8", "ignore")
    if newdata[0:6] == "$GNRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        gps = {"lat": str(lat), "long": str(lng)}
        print(gps)
        return gps
    else:
        return 0


def update_gps_firebase():
    while True:
        data = get_gps()
        if data != 0:
            database.child("track").update(data)

def update_image():
    while True:
        capture_image()
        time.sleep(1)
        storage.child("snap1.png").put("data/images/snap.png")
        time.sleep(4)
        print("image sent")

def alarm(state):
    pass

def sos():
    pass

def read_alarm_sos():
    while True:
        alarm_sos = database.child("track").get().val()
        alarm_sos = [alarm_sos["alarm"], alarm_sos["sos"]]
        print(alarm_sos)
        alarm(alarm_sos["alarm"])
        if alarm_sos["sos"] == 1:
            sos()




#t.Thread(target=update_gps_firebase).start()
t.Thread(target=update_image).start()
#t.Thread(target=read_alarm_sos).start()
