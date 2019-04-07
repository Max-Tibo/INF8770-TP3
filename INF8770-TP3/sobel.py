import numpy as np
import cv2 as cv

# https://github.com/gabilodeau/INF8770/blob/master/Gradients%20et%20extraction%
# 20d'arêtes%20sur%20une%20image.ipynb
def bgr2gray(image):
    grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    col = grayImage[:, 0]
    grayImage = np.column_stack((col, grayImage))
    col = grayImage[:, len(grayImage[0])-1]
    grayImage = np.column_stack((grayImage, col))
    row = grayImage[0, :]
    grayImage = np.row_stack((row, grayImage))
    row = grayImage[len(grayImage)-1, :]
    grayImage = np.row_stack((grayImage, row))

    return grayImage

# https://github.com/wliang6/Sobel-Filter-Implementation/tree/master/Code
# https://docs.opencv.org/3.2.0/d7/d4d/tutorial_py_thresholding.html
# https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/
def sobelConvolution(image):
    image = bgr2gray(image)
    sobelx = cv.Sobel(image, cv.CV_64F, 1, 0, ksize = 3)
    sobely = cv.Sobel(image, cv.CV_64F, 0, 1, ksize = 3)

    fGradient = np.sqrt(np.power(sobelx, 2) + np.power(sobely, 2))
    edges = cv.threshold(fGradient, 127, 255, cv.THRESH_BINARY)[1]
    kernel = np.ones((3, 3), np.uint8)
    dilatedEdges = cv.dilate(edges, kernel, iterations = 1)
    return edges, dilatedEdges

def maxEdges(edges, prevEdges, dilatedEdges, prevDilatedEdges):
    edgesIn = 1 - (np.sum(prevDilatedEdges * edges) / np.sum(edges))
    edgesOut = 1 - (np.sum(prevEdges * dilatedEdges) / np.sum(prevEdges))

    return max(edgesIn, edgesOut)
 