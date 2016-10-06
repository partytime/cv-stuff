from imutils.perspective import four_point_transform
import argparse
import cv2
import imutils


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
            help = "Path to the image to be scanned")
args = vars(ap.parse_args())

#load image, resize greyscale etc
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# this is a lot of blur if the resolution is bad...
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

#see new
cv2.imshow("Edged", edged)
cv2.waitKey(0)

#find the contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#grab only the 4 largest contours
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)

#loop over the contours
print cnts
for c in cnts:
    #approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    #if it has four points its probably the correct one
    if len(approx) == 4:
        doc = approx
        break

#show the outline of the paper
print "heres the contour"
cv2.drawContours(image, [doc], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)

# apply four point perspective transform
paper = four_point_transform(image, doc.reshape(4, 2))
warped = four_point_transform(gray, doc.reshape(4, 2))
cv2.imshow("paper", paper)
cv2.imshow("gray", warped)
cv2.waitKey(0)
