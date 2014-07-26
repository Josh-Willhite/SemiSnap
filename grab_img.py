import numpy as np
from scipy import stats
import cv2
import subprocess
from collections import deque

#TODO buffer last 10? frames and select the frame with the highest mean value

thresh_q = deque(maxlen=1000)

def alarm():
    subprocess.call(["beep"])


def get_threshold():
    mean_list = [val for val in thresh_q]
    return stats.mode(mean_list)


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


def snap(number_of_frames):
    cap = cv2.VideoCapture(1)
    raw = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
    a = getROI(raw)
    b = getROI(raw)
    #c = getROI(raw)
    #frame_buffer = []

    while True:
        raw = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
        c = b
        b = a
        a = getROI(raw)

        d = diff(c,b,a)

        thresh_q.append(round(d[1][0], 2))

        cv2.imshow('ROI', a)
        if d[1][0] > get_threshold()[0][0] + .15 * get_threshold()[0][0]:
            cv2.imshow('movement', raw)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #frame_buffer.append(frame)

    cap.release()
    cv2.destroyAllWindows()
    '''
    #write images to disk
    count = 0
    for f in frame_buffer:
        print count
        cv2.imwrite('./images/out-%s.png' % str(count), f)
        count += 1
    '''





def main():
    snap(10)


if __name__ == '__main__':
    main()