from imutils import face_utils
import dlib
import cv2 as cv
import numpy as np

p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cap = cv.VideoCapture(0)

def getWebcamImage():
	_, image =  cap.read()
	image = cv.flip(image, 1)
	return image

def createBlankImage(width, height, rgb_color=(255, 255, 255)):
	# Create black blank image
	image = np.zeros((height, width, 3), np.uint8)

	# Since OpenCV uses BGR, convert the color first
	color = tuple(reversed(rgb_color))
	# Fill image with color
	image[:] = color

	return image

# draws rectangles around mouth and eyes
def drawBoundsOnImage(boundsImage, bounds):
	cv.rectangle(boundsImage, (bounds.leftEye.minX, bounds.leftEye.minY), (bounds.leftEye.maxX, bounds.leftEye.maxY), (0, 0, 0), 1)
	cv.rectangle(boundsImage, (bounds.rightEye.minX, bounds.rightEye.minY), (bounds.rightEye.maxX, bounds.rightEye.maxY), (0, 0, 0), 1)
	cv.rectangle(boundsImage, (bounds.mouth.minX, bounds.mouth.minY), (bounds.mouth.maxX, bounds.mouth.maxY), (0, 0, 0), 1 )

# draws points on the face
def drawLandmarksOnImage(image, bounds):
	shape = bounds.landmarks
	for (x, y) in shape:
		cv.circle(image, (x, y), 2, (0, 0, 0), -1)