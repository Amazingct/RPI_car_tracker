# AUTOUPADTED
import cv2
import pyrebase, time
import threading as t
import serial
import time
import pynmea2
from vlc import MediaPlayer
from twilio.rest import Client

buzz = 12

def send_sms():

    account_sid = '*C7563713d93ca00e600fb7217e339686*'
    auth_token = '**4a5b63640ba1dfd91942e07350cb**'
    number = "+2348100125089"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        messaging_service_sid='MG12bbd25d1c0e4a48388bf6eb478e0012',
        body="CAR SOS TRIGGERED, CORDINATES ARE: {}".format(str(get_gps())),
        to=number)

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzz, GPIO.OUT)

except :
    print("Error importing RPi.GPIO. This is probably because you need superuser. Try running again with 'sudo'.")

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
    "serviceAccount":"/home/pi/RPI_car_tracker/service.json"
}

fire_base = pyrebase.initialize_app(config)
auth = fire_base.auth()
database = fire_base.database()
storage = fire_base.storage()


# Major functions

def capture_image():
    try:
        image = cv2.VideoCapture(0)
    except:
        image = cv2.VideoCapture(1)

    result = True
    while result:
        ret, frame = image.read()
        image_name = "/home/pi/RPI_car_tracker/data/images/snap.png"
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
        return gps
    else:
        return {"lat": str(0.0), "long": str(0.0)}


def update_gps_firebase():

    while True:
        try:
            data = get_gps()
            print(data)
            if data["lat"] != "0.0" or data["long"] != "0.0":
                database.child("track").update(data)
        except Exception as e:
            print("upada_gps:", e)

def update_image():
    while True:
        try:
            capture_image()
            time.sleep(1)
            storage.child("snap.png").put("/home/pi/RPI_car_tracker/data/images/snap.png")
            time.sleep(4)
            print("image sent")
            time.sleep(15)

        except Exception as e:
            print("upadate_img:", e)



def alarm(state):
    GPIO.output(buzz, state)
    if state == 1:
        MediaPlayer("/home/pi/RPI_car_tracker/sos.mp3").play()

def sos():
    send_sms()

def read_alarm_sos():
    while True:
        try:
            alarm_sos = database.child("track").get().val()
            alarm_sos = [alarm_sos["alarm"], alarm_sos["sos"]]
            print(alarm_sos)
            alarm(int(alarm_sos[0])) # switch alarm/buzzer
            if int(alarm_sos[1]) == 1:
                sos()
        except Exception as e:
            print("read_alarm:", e)



t.Thread(target=update_gps_firebase).start()
t.Thread(target=update_image).start()
t.Thread(target=read_alarm_sos).start()
