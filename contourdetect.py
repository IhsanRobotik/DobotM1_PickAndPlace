import cv2 as cv
from math import atan2, cos, sin, sqrt, pi
import numpy as np

# Open a video stream (replace 0 with a video file path or URL if needed)
cap = cv.VideoCapture("http://192.168.1.12:8080/video")  # Use 0 for the default webcam

if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame from video stream.")
        break

    # Convert frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Convert frame to binary
    _, bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

    # Find all the contours in the thresholded frame
    contours, _ = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    for i, c in enumerate(contours):
        # Calculate the area of each contour
        area = cv.contourArea(c)

        # Ignore contours that are too small or too large
        if area < 3700 or 100000 < area:
            continue

        # cv.minAreaRect returns:
        # (center(x, y), (width, height), angle of rotation)
        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int8(box)  # Ensure box points are integers

        # Check if the box has valid points
        if box is not None and len(box) > 0:
            # Retrieve the key parameters of the rotated bounding box
            center = (int(rect[0][0]), int(rect[0][1]))
            width = int(rect[1][0])
            height = int(rect[1][1])
            angle = int(rect[2])

            if width < height:
                angle = 90 - angle
            else:
                angle = -angle

            label = "  Rotation Angle: " + str(angle) + " degrees"
            textbox = cv.rectangle(frame, (center[0] - 35, center[1] - 25),
                                   (center[0] + 295, center[1] + 10), (255, 255, 255), -1)
            cv.putText(frame, label, (center[0] - 50, center[1]),
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv.LINE_AA)
            cv.drawContours(frame, [box], 0, (0, 0, 255), 2)

    # Display the frame with annotations
    cv.imshow('Output Video Stream', frame)

    # Break on 'q' key press
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv.destroyAllWindows()