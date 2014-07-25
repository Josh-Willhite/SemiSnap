import numpy as np
import cv2
import time

def snap(number_of_frames):
    cap = cv2.VideoCapture(0)

    for i in range(number_of_frames):
        ret, frame = cap.read()
        width = np.size(frame, 0)
        height = np.size(frame, 1)
        text_color = (0,0,255)
        cv2.putText(frame, str(time.time()), (width/2, height/2), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=1, lineType=cv2.CV_AA)
        cv2.imwrite('./images/out-%s.png' % str(i), frame)

    cap.release()
    cv2.destroyAllWindows()


def main():
    snap(10)

if __name__ == '__main__':
    main()