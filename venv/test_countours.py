# import numpy as np
# import cv2 as cv

# def get_countours():
#     im = cv.imread('testimg.png')
#     # img = im.copy()
#     # assert img is not None, 'img is none'
#     assert im is not None, "file could not be read, check with os.path.exists()"
#     imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
#     ret, thresh = cv.threshold(imgray, 127, 255, 0)
#     contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#     img = cv.drawContours(im, contours, -1, (0, 255, 0), 3)
#     return im
#
# def show_image(image):
#     cv.imshow('image',image)
#
import cv2

def show_image(image):
    cv2.imwrite('boxes.jpg',image)

image = cv2.imread('testimg.png')
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, im = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy  = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(image, contours, -1, (0,255,75), 2)


if __name__ == '__main__':
    show_image(img)
