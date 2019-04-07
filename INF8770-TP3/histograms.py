import cv2 as cv

# https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-
# using-opencv-python/?fbclid=IwAR17bwr2M9b0vqxoROzA5JhLN7uONB3n0GpNeTQeuNYzxYFdT-y4aAlTDho
def histograms(image):
    histograms = []

    histogramB = cv.calcHist([image], [0], None, [64], [0, 256])
    histograms.append(histogramB)
    histogramG = cv.calcHist([image], [1], None, [64], [0, 256])
    histograms.append(histogramG)
    histogramR = cv.calcHist([image], [2], None, [64], [0, 256])
    histograms.append(histogramR)

    return histograms

def distance(histogramsA, histogramsB):
    totalDistance = 0
    for i in range(0, 3):
        totalDistance += cv.compareHist(histogramsA[i], histogramsB[i], cv.HISTCMP_CORREL)

    return totalDistance