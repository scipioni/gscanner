import cv2 as cv
import imutils
import numpy as np


params = {"canny1": 20, "canny2": 20}

def on_canny1(val):
    global params
    params["canny1"] = val

def on_canny2(val):
    global params
    params["canny2"] = val

def detect_paper_canny(image, debug=False):
    global params

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    edged = cv.Canny(gray, params["canny1"], params["canny2"])

    cnts = cv.findContours(edged.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:5]

    screenCnt = None
    for c in cnts:
        # approximate the contour
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is not None:
        cv.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

    if debug:
        if not params.get("canny_create"):
            cv.namedWindow("canny")
            params["canny"] = True
        if not params.get("canny1_create"):
            cv.createTrackbar("canny1", "canny", params["canny1"], 255, on_canny1)
            params["canny1_create"] = True
        if not params.get("canny2_create"):
            cv.createTrackbar("canny2", "canny", params["canny2"], 255, on_canny2)
            params["canny2_create"] = True
        cv.imshow("canny", edged)
        cv.imshow("image", image)
        cv.waitKey(1)

    return screenCnt


def warp(image, box, ratio):
    warped = four_point_transform(image, box.reshape(4, 2) * ratio)
    # warped = cv.cvtColor(warped, cv.COLOR_BGR2GRAY)
    # T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    # warped = (warped > T).astype("uint8") * 255
    return warped


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )

    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def show(image, title="image"):
    cv.imshow(title, image)
    cv.waitKey(1)


def unfisheye(img):
    DIM = (8000, 6000)
    K = np.array(
        [
            [300772.12680186087, 0.0, 4267.443587842004],
            [0.0, 299655.0365974141, 3428.0867875641834],
            [0.0, 0.0, 1.0],
        ]
    )
    D = np.array(
        [
            [-584.3734549284128],
            [846224.2265958918],
            [-2584558195.32632],
            [4125317093154.449],
        ]
    )
    h, w = img.shape[:2]

    map1, map2 = cv.fisheye.initUndistortRectifyMap(
        K, D, np.eye(3), K, DIM, cv.CV_16SC2
    )
    undistorted_img = cv.remap(
        img, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT
    )
    return undistorted_img
