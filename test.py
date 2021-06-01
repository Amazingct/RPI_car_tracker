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

def update_gps_firebase(lat=0.0, long=0.0):
    database.child("gps").update({"lat": lat, "long": long})


update_gps_firebase(2,8)
