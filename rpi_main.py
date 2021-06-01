import cv2
import time

# Major functions
def get_gps():
    pass

def buzz():
    pass

def capture_images(no=1, s = 1):
    image = cv2.VideoCapture(0)
    result = True
    while result:
        for n in range(no):
            ret, frame = image.read()
            image_name = "data/images/capture_" + str(n) + ".jpg"
            cv2.imwrite(image_name, frame)
            time.sleep(s)
        result = False
    image.release()
    cv2.destroyAllWindows()


capture_images(3, 2)
