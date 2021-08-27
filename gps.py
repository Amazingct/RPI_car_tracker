# AUTOUPADTED
import cv2
import pyrebase, time
import threading as t
import serial
import time
import pynmea2


port = "/dev/ttyAMA0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)


def get_gps():
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline()
    newdata = newdata.decode("utf-8", "ignore")
    print(newdata)
    if newdata[0:6] == "$GNRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        gps = {"lat": str(lat), "long": str(lng)}
        print(gps)

