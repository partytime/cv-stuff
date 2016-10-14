# import the necessary packages
import argparse
import cv2
import numpy

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to the input image")
ap.add_argument("-c", "--cascade",
    default="haarcascade_frontalcatface.xml",
    help="path to cat detector haar cascade")
args = vars(ap.parse_args())

# load the input image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# load the cat detector Haar cascade, then detect cat faces
# in the input image
detector = cv2.CascadeClassifier(args["cascade"])
print detector
rectList = []
why = numpy.arange(1.1,1.5,0.1)
for mn in xrange(1,10,):
    print "trying minNeighbor", mn
    for sf in why:
        print "trying scaleFactor", sf
        rects = detector.detectMultiScale(gray, scaleFactor=sf,
                minNeighbors=mn, minSize=(75, 75))
        if len(rects) > 0:
            print 'found rects'
            rectList.append(rects)

print rectList
#draw over the kitty faces
for r in rectList:
    print 'trying', r
    #for (i, (x, y, w, h)) in enumerate(rects):
    for (x, y, w, h) in r:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #cv2.putText(image, "Cat #{}".format(1 + 1), (x, y - 10),
            #cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

        #show em
        cv2.imshow("Cat faces", image)
        cv2.waitKey(0)
