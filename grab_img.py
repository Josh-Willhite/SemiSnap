import numpy as np
import cv2
import time
import subprocess

threshold = .4

def alarm():
    subprocess.call(["beep"])


def diff(c, b, a):
    d1 = cv2.absdiff(a, b)
    d2 = cv2.absdiff(b, c)
    sum = cv2.bitwise_and(d1, d2)
    return sum


def getROI(frame):
    x0 = 100
    y0 = 100
    x1 = 500
    y1 = 500
    return frame[y0:y1, x0:x1]


def snap(number_of_frames):
    cap = cv2.VideoCapture(1)

    a = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
    b = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
    c = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
    frame_buffer = []

    while(True):
    #for i in range(number_of_frames):
        #ret, frame = cap.read()

        c = b
        b = a
        a = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)

        #width = np.size(frame, 0)
        #height = np.size(frame, 1)
        #text_color = (0,0,255)
        #cv2.putText(frame, str(time.time()), (width/2, height/2), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color)
        #cv2.imshow('frame', a)
        d = diff(c,b,a)
        cv2.imshow('diff', d)
        cv2.imshow('roi', getROI(a))
        if cv2.mean(d)[0] > threshold:
            cv2.imshow('movement', a)
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