import numpy as np
import cv2

def snap(number_of_frames):
    cap = cv2.VideoCapture(0)

    for i in range(number_of_frames):
        ret, frame = cap.read()
        cv2.imwrite('out-%s.png' % str(i), frame)

    cap.release()
    cv2.destroyAllWindows()


def main():
    snap(10)

if __name__ == '__main__':
    main()