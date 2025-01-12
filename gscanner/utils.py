import cv2 as cv
import numpy as np

def detect_white_paper(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    h,w = gray.shape[:2]

    _, thresh = cv.threshold(gray, 128, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    white_paper_contours = []
    for cnt in contours:
        area = cv.contourArea(cnt)/(h*w)
        if area > .05:  # Adjust this threshold as needed
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            if len(approx) == 4:
                white_paper_contours.append(cnt)
    
    boxes = []
    if len(white_paper_contours) > 0:
        for cnt in white_paper_contours:
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)

            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            box = np.round(box).astype(int)
            boxes.append(box)
        return boxes[0]
    return None

def show_box(img, box):
    for i,p in enumerate(box):
        cv.circle(img, p, 30, (255,0,0), -1) 
        cv.putText(img, str(i), p, cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv.LINE_AA)

def warpPerspective(img, box):
    """
    p2  p3

    p1  p4
    """
    p1,p2,p3,p4 = box
    width = max([p3[0]-p2[0], p4[0]-p1[0]])
    height = max([p1[1]-p2[1], p4[1]-p3[1]])

    # converted_red_pixel_value = [0,0]
    # converted_green_pixel_value = [width,0]
    # converted_black_pixel_value = [0,height]
    # converted_blue_pixel_value = [width,height]
    # converted_points = np.float32([converted_red_pixel_value,converted_green_pixel_value, converted_black_pixel_value,converted_blue_pixel_value])


    target = np.float32([[0,height], [0,0], [width,0], [width,height]])
