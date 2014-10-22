import cv2
from collections import deque
import numpy as np
import time
from math import hypot

frame_q = deque(maxlen=9)
motion_q = deque(maxlen=9)

#{size, number of tires, direction, speed}

def set_camera(cap):
    cap.set(cv2.cv.CV_CAP_PROP_CONTRAST, 255/255.0)
    cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 28/255.0)
    cap.set(cv2.cv.CV_CAP_PROP_SATURATION, 255/255.0)


def detect_motion():
    if len(frame_q) > 2:
        d1 = cv2.absdiff(frame_q[-1], frame_q[-2])
        d2 = cv2.absdiff(frame_q[-2], frame_q[-3])
        movement = cv2.bitwise_and(d1, d2)
        motion_q.append(movement)


def areas_of_motion():
    def area(cnt):
        return cv2.moments(cnt)['m00']

    def centroid(cnt):
        moments = cv2.moments(cnt)
        if moments['m00'] != 0:
            x = int(moments['m10']/moments['m00'])
            y = int(moments['m01']/moments['m00'])
            return [x,y]
        return ['','']

    def distance(c0, c1):
        return hypot(c1[0] - c0[0], c1[1] - c0[1])

    def min_distance_between_contours(cnts):
        min_distance = 1200
        for cntA in cnts:
            for cntB in cnts:
                if cntA is not cntB:
                    curr_distance = distance(centroid(cntA), centroid(cntB))
                    if  curr_distance < min_distance: min_distance = curr_distance
        return min_distance


    def filter_contours(all_contours):
        cleaned = []
        for cnt in all_contours:
            if area(cnt) != 0:
                cleaned.append(cnt)
        return cleaned

    def consolidate(cntA, cntB):
        all_pts = np.concatenate([cntA, cntB])
        hull_pts = cv2.convexHull(all_pts)
        return hull_pts

    def mid_point(ptA, ptB):
        return [(ptA[0] + ptB[0])/2, (ptA[1] + ptB[1])/2]

    def clean_img():
        eroded_img = None
        if len(motion_q) > 0:
            ret, threshed_img= cv2.threshold(motion_q[-1],5, 255,0)

            kernel = np.ones((3,3), np.uint8)
            eroded_img = cv2.erode(threshed_img, kernel, iterations=1)
        return eroded_img

    cleaned_img = clean_img()
    if cleaned_img is not None:
        contours, hierarchy = cv2.findContours(cleaned_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    else:
        return

    contours = filter_contours(contours)

    if len(contours) > 1:
        centroids = []
        for cnt in contours:
            c = centroid(cnt)
            if type(c[0]) is not str:
                centroids.append(c)


        xs = [x[0] for x in centroids]
        ys = [y[1] for y in centroids]

        centroids_array = np.array([xs,ys])

        idx = np.argsort(centroids_array[0])
        centroids_array = centroids_array[:,idx]

        #print 'NUMPY\n ' + str(centroids_array)
        consolidated_centroids = []
        num_centroids = centroids_array.shape[1]
        for i in range(num_centroids):
            if i + 1 < num_centroids:
                dist = distance(centroids_array[:, i], centroids_array[:,i + 1])
                #print '(%s,%s) DISTANCE: %s' % (str(centroids_array[:, i]), str(centroids_array[:, i + 1]), str(dist))
                if dist < 200:

                    if len(consolidated_centroids) > 0:
                        #add to current consolidated centroid and iterate weight value
                        md_point = mid_point(consolidated_centroids[-1]['centroid'], centroids_array[:,i + 1])
                        consolidated_centroids[-1]['centroid'] = md_point
                        consolidated_centroids[-1]['weight'] += 1
                    else:
                        object_start = centroids_array[:,i]
                        consolidated_centroids.append({'centroid':centroids_array[:,i + 1], 'weight':0})

                else:
                    #start new centroid
                    object_start = centroids_array[:,i]
                    consolidated_centroids.append({'centroid':centroids_array[:,i + 1], 'weight':0})
                #print consolidated_centroids

        for c in consolidated_centroids:
            center = (c['centroid'][0], c['centroid'][1])
            radius = c['weight'] * 4
            cv2.circle(cleaned_img, center, radius, (255,0,0), 3)

        cv2.imshow('centroids', cleaned_img)
    #cv2.circle(cleaned_img, c, 10, (255,0,0), 3)
    #cv2.drawContours(motion_q[-1], contours, -1, (255,0,0))


def main():
    cap = cv2.VideoCapture(0)
    set_camera(cap)

    while True:
        frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
        frame_q.append(frame)

        detect_motion()
        areas_of_motion()



        cv2.imshow('raw', frame)
        if len(motion_q) > 0:
            cv2.imshow('movement', motion_q[-1])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()