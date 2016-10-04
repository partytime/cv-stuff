from searcher import Searcher
import numpy as np
import argparse
import cPickle
import cv2

# construct the arg parser and parse args
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "Path to the directory that contains the images we just indexed")
ap.add_argument("-i", "--index", required = True,
    help = "Path to where we stored our index")
args = vars(ap.parse_args())

# load the index and initialize our searcher
index = cPickle.loads(open(args["index"]).read())
searcher = Searcher(index)

# loop over images in the index, we will use each one as a
# query image

for (query, queryFeatures) in index.items():
    # perform the search using current query
    results = searcher.search(queryFeatures)

    # load the query image and display it
    path = args["dataset"] + "/%s" % (query)
    queryImage = cv2.imread(path)
    cv2.imshow("Query", queryImage)
    print "query: %s" % (query)

    # initialize the two montages to display our results --
    # we have a total of 25 images in the index, but let's only
    # display the top 10 results; 5 images permontage, with
    # images that are 400x166 pixels
    montageA = np.zeros((166 * 5, 400, 3), dtype = "uint8")
    montageB = np.zeros((166 * 5, 400, 3), dtype = "uint8")

    # loop over the top 10 results
    for j in xrange(0, 10):
        # grab the result (using row-major order) and load
        # the result image
        (score, imageName) = results[j]
        path = args["dataset"] + "/%s" % (imageName)
        result = cv2.imread(path)
        print "\t%d. %s : %.3f" % (j + 1, imageName, score)

        # check to see if the first montage should be used
        if j < 5:
            montageA[j * 166:(j + 1) * 166, :] = result

        # otherwise, the second montage should be used
        else:
            montageB[j * 166:(j + 1) * 166, :] = result

        # show the results
        cv2.imshow("results 1-5", montageA)
        cv2.imshow("results 6-10", montageB)
        cv2.waitkey(0)


