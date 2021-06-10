from imutils import face_utils
import dlib
import cv2 as cv
import numpy as np

from bounds import FacialBounds
import opencv_helper


def getBoundsFromImage(image):
    # convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
    # get faces from grayscale image
    rects = opencv_helper.detector(gray, 0)

    # find landmarks for each face
    for (i, rect) in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = opencv_helper.predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        bounds = None
        bounds = FacialBounds(shape, len(image[0]), len(image))
        return bounds

    return FacialBounds([], len(image[0]), len(image))

def run():
    # create images
    image = opencv_helper.getWebcamImage()
    blankImage = opencv_helper.createBlankImage(len(image[0]), len(image))
    boundsImage = opencv_helper.createBlankImage(len(image[0]), len(image))

    # convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
    # get faces from grayscale image
    rects = opencv_helper.detector(gray, 0)

    # find landmarks for each face
    for (i, rect) in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = opencv_helper.predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        bounds = FacialBounds(shape, len(image[0]), len(image))
        if len(shape) > 0:

            opencv_helper.drawBoundsOnImage(boundsImage, bounds)

        opencv_helper.drawLandmarksOnImage(image, shape)
        opencv_helper.drawLandmarksOnImage(blankImage, shape)

    # show all images
    cv.imshow("Output", image)
    cv.imshow("Blank", blankImage)
    cv.imshow("Bounds", boundsImage)