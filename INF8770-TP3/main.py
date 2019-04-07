import cv2 as cv
import histograms as hst
import sobel as sbl

isFirstIteration = True
isFading = False
isEffect = False
fadeStart = 0
effectStart = 0
fadeEnd = 0
effectEnd = 0
high = 0
index = 0

video = cv.VideoCapture("julia.avi")
video.open("julia.avi")

while(True):
    index += 1
    ret, frame = video.read()
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    if isFirstIteration:
        prevHistograms = hst.histograms(frame)
        prevEdges, prevDilatedEdges = sbl.sobelConvolution(frame)
        prevMaxp = 0
        isFirstIteration = False
    else:
        histograms = hst.histograms(frame)
        edges, dilatedEdges = sbl.sobelConvolution(frame)

        if hst.distance(histograms, prevHistograms) <= 1.9 and not isFading:
            print("Histo -> Cut at frame : " + str(index))
        elif hst.distance(histograms, prevHistograms) <= 2.6:
            if not isFading:
                isFading = True
                fadeStart = index
        else:
            if isFading:
                isFading = False
                fadeEnd = index
                print("Histo -> Fade at frames : " + str(fadeStart) + " to " + str(fadeEnd)) 

        maxp = sbl.maxEdges(edges, prevEdges, dilatedEdges, prevDilatedEdges)
        if abs(maxp - prevMaxp) >= 8:
            isEffect = True
            effectStart = index
            high = maxp
        else:
            if isEffect and abs(maxp - high) >= 1:
                isEffect = False
                effectEnd = index
                if (effectEnd - effectStart) == 1:
                    print("Convo -> Cut at frame : " + str(effectStart))
                else:    
                    print("Convo -> Fade at frames : " + str(effectStart) + " to " + str(effectEnd))
        
        prevMaxp = maxp 

        prevHistograms = histograms
        prevEdges = edges
        prevDilatedEdges = prevDilatedEdges

video.release()
cv.destroyAllWindows()