import sys

import cv2
import imutils
import numpy as np

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


def undistort(img_path):
    img = cv2.imread(img_path)
    img_small = imutils.resize(img, height=600)
    h, w = img.shape[:2]

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
        K, D, np.eye(3), K, DIM, cv2.CV_16SC2
    )
    undistorted_img = cv2.remap(
        img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT
    )

    frame = imutils.resize(undistorted_img, height=600)
    cv2.imshow("original", img_small)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        undistort(p)
