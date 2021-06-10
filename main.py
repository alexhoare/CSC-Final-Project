import tkinter
from tkinter import Tk, Canvas, Frame, BOTH, NW
from PIL import Image, ImageTk

import landmark_recognition
import opencv_helper

import cv2 as cv

def create_circle(canvas, x, y, r, **kwargs):
    canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

image = opencv_helper.getWebcamImage()
initialBounds = landmark_recognition.getBoundsFromImage(image)
imageWidth = initialBounds.imageWidth
imageHeight = initialBounds.imageHeight

root = Tk()
canvas = Canvas(root, width=initialBounds.imageWidth, height=initialBounds.imageHeight, bg='white')
canvas.pack()

print(initialBounds.imageWidth, initialBounds.imageHeight)

while True:
    image = opencv_helper.getWebcamImage()
    bounds = landmark_recognition.getBoundsFromImage(image)

    if not bounds.exists():
        continue

    opencv_helper.drawLandmarksOnImage(image, bounds)
    opencv_helper.drawBoundsOnImage(image, bounds)

    bounds.enlargeFeatures(2)

    canvasScale = 2

    eyeImage = Image.open("eye.gif")

    if bounds.leftEye.dy > 0:
        leftEye = eyeImage.resize((bounds.leftEye.dx * canvasScale, bounds.leftEye.dy * canvasScale))
        tkLeftEye = ImageTk.PhotoImage(image=leftEye)
        canvas.create_image((bounds.leftEye.minX, bounds.leftEye.minY), image=tkLeftEye, anchor=NW)

    if bounds.rightEye.dy > 0:
        rightEye = eyeImage.resize((bounds.rightEye.dx * canvasScale, bounds.rightEye.dy * canvasScale))
        tkRightEye = ImageTk.PhotoImage(image=rightEye)
        canvas.create_image((bounds.rightEye.minX, bounds.rightEye.minY), image=tkRightEye, anchor=NW)

    if bounds.mouth.dy > 0:
        mouthImage = Image.open("mouth.gif").resize((bounds.mouth.dx * canvasScale, bounds.mouth.dy * canvasScale))
        tkMouth = ImageTk.PhotoImage(image=mouthImage)
        canvas.create_image((bounds.mouth.minX, bounds.mouth.minY), image=tkMouth, anchor=NW)

    if bounds.facialWidth > 0:
        x, y = bounds.centerPoint
        y += bounds.facialWidth / 4
        create_circle(canvas, x, y, bounds.facialWidth / 2 * 1.5)


    # uncomment to see facial landmarks

    # for (x, y) in bounds.landmarks:
    #     create_circle(canvas, x, y, 2)
    # canvas.create_rectangle(bounds.mouth.minX, bounds.mouth.minY, bounds.mouth.maxX, bounds.mouth.maxY)
    # canvas.create_rectangle(bounds.leftEye.minX, bounds.leftEye.minY, bounds.leftEye.maxX, bounds.leftEye.maxY)
    # canvas.create_rectangle(bounds.rightEye.minX, bounds.rightEye.minY, bounds.rightEye.maxX, bounds.rightEye.maxY)

    canvas.scale("all", 0, 0, canvasScale, canvasScale)
    canvas.configure(width=imageWidth*canvasScale, height=imageHeight*canvasScale)

    root.update_idletasks()
    root.update()

    canvas.delete("all")

    cv.imshow("image with landmarks", image)
    cv.waitKey(1)