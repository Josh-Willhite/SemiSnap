import numpy as np
from scipy import stats
import cv2
import subprocess
import time
from time import strftime
from Queue import Queue
from collections import deque
import threading
from tweet_image import post_vehicle_image


thresh_q = deque(maxlen=500)
trigger_level = .25
min_img_cap_time = 1.5

img_write_q = Queue()

def alarm():
    subprocess.call(["beep"])


def get_threshold():
    mean_list = [val for val in thresh_q]
    return stats.mode(mean_list)[0][0]


def diff(c, b, a):
    d1 = cv2.absdiff(a, b)
    d2 = cv2.absdiff(b, c)
    background_removed = cv2.bitwise_and(d1, d2)
    return background_removed, cv2.mean(background_removed)


def getROI(frame):
    width = np.size(frame, 1)
    height = np.size(frame, 0)

    #select upper portion of frame
    x0 = 0
    y0 = 0
    x1 = width
    y1 = height/2

    return frame[y0:y1, x0:x1]


def snap():
    print "waiting to detect vehicle"
    cap = cv2.VideoCapture(0)
    raw = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
    a = raw
    b = raw
    last_time = time.time()

    while True:
        curr_time = time.time()
        raw = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
        c = b
        b = a
        a = raw

        d = diff(c,b,a)[1][0]

        thresh_q.append(round(d, 2))
        curr_mode = get_threshold()
        curr_threshold = curr_mode + trigger_level * curr_mode


        if d > curr_threshold and len(thresh_q) > 50 and (curr_time - last_time) > min_img_cap_time:
            width = np.size(raw, 1)
            height = np.size(raw, 0)
            last_time = curr_time
            text_color = (0, 0, 0)
            cv2.putText(raw, strftime("%a, %d %b %Y %H:%M:%S"), (0, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, text_color)
            cv2.imshow('movement', raw)
            img_write_q.put(raw)
            #print "TIME: " + str(last_time)
            #print "FRAME MEAN: " + str(d)
            #print "Current Threshold: "  + str(curr_threshold)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def write_img():
    print "waiting to write images"
    while True:
        if not img_write_q.empty():
            frame = img_write_q.get()
            cv2.imwrite('./images/%s.png' % time.time(), frame)


if __name__ == '__main__':
    cv_thread = threading.Thread(target=snap)
    cv_thread.start()

    write_thread = threading.Thread(target=write_img)
    write_thread.start()

    tweet_thread = threading.Thread(target=post_vehicle_image())
    write_thread.start()