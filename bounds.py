import math

class Bounds:
	def __init__(self, minX, minY, maxX, maxY):
		self.minX = minX
		self.minY = minY
		self.maxX = maxX
		self.maxY = maxY

		self.dx = abs(maxX - minX)
		self.dy = abs(maxY - minY)

class FacialBounds:
	def __init__(self, landmarks, imageWidth, imageHeight):
		self.landmarks = landmarks
		if (len(landmarks) > 0):
			self.processFeatures()
		self.imageWidth = imageWidth
		self.imageHeight = imageHeight
		pass
	
	def processFeatures(self):
		self.processEyes()
		self.processMouth()
		self.processFace()

	def processFace(self):
		x1, y1 = self.landmarks[0]
		x2, y2 = self.landmarks[16]

		self.facialWidth = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		self.centerPoint = (x1 + x2) / 2, (y1 + y2) / 2


	def processEyes(self):
		leftMinX = self.landmarks[36][0]
		leftMaxX = self.landmarks[39][0]
		leftMinY= max(self.landmarks[37][1], self.landmarks[38][1])
		leftMaxY = min(self.landmarks[40][1], self.landmarks[41][1])

		self.leftEye = Bounds(leftMinX, leftMinY, leftMaxX, leftMaxY)

		rightMinX = self.landmarks[42][0]
		rightMaxX = self.landmarks[45][0]
		rightMinY= max(self.landmarks[44][1], self.landmarks[43][1])
		rightMaxY  = min(self.landmarks[46][1], self.landmarks[47][1])

		self.rightEye = Bounds(rightMinX, rightMinY, rightMaxX, rightMaxY)

	def processMouth(self):
		minX = self.landmarks[48][0]
		maxX = self.landmarks[54][0]
		minY = self.landmarks[51][1]
		maxY = self.landmarks[57][1]

		self.mouth = Bounds(minX, minY, maxX, maxY)


	def scale(self, scaleFactor):
		self.mouth = Bounds(2 * self.mouth.minX, 2 * self.mouth.minY, 2 * self.mouth.maxX, 2 * self.mouth.maxY)
		self.rightEye = Bounds(2 * self.rightEye.minX, 2 * self.rightEye.minY, 2 * self.rightEye.maxX, 2 * self.rightEye.maxY)
		self.leftEye = Bounds(2 * self.leftEye.minX, 2 * self.leftEye.minY, 2 * self.leftEye.maxX, 2 * self.leftEye.maxY)
		self.imageWidth *= 2
		self.imageHeight *= 2
	
	def enlargeFeatures(self, scaleFactor):
		self.mouth = self.getNewBoundsAfterScale(self.mouth, scaleFactor)
		self.rightEye = self.getNewBoundsAfterScale(self.rightEye, scaleFactor)
		self.leftEye = self.getNewBoundsAfterScale(self.leftEye, scaleFactor)

	def getNewBoundsAfterScale(self, oldBounds, scaleFactor):
		ddx = oldBounds.dx * (scaleFactor - 1) / 2
		ddy = oldBounds.dy * (scaleFactor - 1) / 2

		newBounds = Bounds(round(oldBounds.minX - ddx), round(oldBounds.minY - ddy), round(oldBounds.maxX + ddx), round(oldBounds.maxY + ddy))
		return newBounds

	def exists(self):
		return len(self.landmarks) > 0
