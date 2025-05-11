import torch
import cv2
from ultralytics import YOLO
import math
import numpy as np

# Load the YOLO model
model = YOLO("best2.pt")

# Open a webcam feed
cv2.namedWindow("YOLO Webcam Inference", cv2.WINDOW_NORMAL)
url = "http://192.168.1.12:8080/video"

confidence = 0.5  # Confidence threshold

# Initialize VideoCapture with the URL
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame from video stream.")
        break

    # Perform inference
    results = model.predict(frame, conf=confidence, verbose=False)

    contourFrame = frame.copy()  # Create a copy of the frame to draw contours

    for result in results:
        if result.masks is not None:
            masks = result.masks.data.cpu().numpy()  # Extract masks
            for mask in masks:
                # Convert mask to uint8 format
                mask_uint8 = (mask * 255).astype(np.uint8)

                # Find contours within the mask
                contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Draw contours on the contourFrame
                for contour in contours:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    # Draw the bounding box
                    cv2.drawContours(contourFrame, [box], 0, (255, 0, 0), 2)

                    # Optionally, draw the contour itself
                    cv2.drawContours(contourFrame, [contour], -1, (0, 255, 0), 1)

    # Display the frame with YOLO annotations
    cv2.imshow("YOLO Webcam Inference", results[0].plot())

    # Display the frame with contours
    cv2.imshow("Contours", contourFrame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()