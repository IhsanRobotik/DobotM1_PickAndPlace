import cv2
import numpy as np
import requests

cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
cv2.namedWindow("Filtered", cv2.WINDOW_NORMAL)

def get_frame_from_url(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    return frame

def nothing(x):
    pass

url = "http://192.168.1.9:8080/shot.jpg"
cv2.namedWindow("HSV Adjust")

# Sliders use 360° for H, 100% for S and V
cv2.createTrackbar("H Lower", "HSV Adjust", 0, 360, nothing)
cv2.createTrackbar("S Lower", "HSV Adjust", 0, 100, nothing)
cv2.createTrackbar("V Lower", "HSV Adjust", 0, 100, nothing)

cv2.createTrackbar("H Upper", "HSV Adjust", 360, 360, nothing)
cv2.createTrackbar("S Upper", "HSV Adjust", 100, 100, nothing)
cv2.createTrackbar("V Upper", "HSV Adjust", 100, 100, nothing)

while True:
    frame = get_frame_from_url(url)
    if frame is None:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Read from sliders in human scale
    hL = cv2.getTrackbarPos("H Lower", "HSV Adjust")
    sL = cv2.getTrackbarPos("S Lower", "HSV Adjust")
    vL = cv2.getTrackbarPos("V Lower", "HSV Adjust")

    hU = cv2.getTrackbarPos("H Upper", "HSV Adjust")
    sU = cv2.getTrackbarPos("S Upper", "HSV Adjust")
    vU = cv2.getTrackbarPos("V Upper", "HSV Adjust")

    # Convert to OpenCV scale
    lower = np.array([int(hL / 2), int(sL * 255 / 100), int(vL * 255 / 100)])
    upper = np.array([int(hU / 2), int(sU * 255 / 100), int(vU * 255 / 100)])

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Filtered", result)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        print("Lower HSV (360,100,100):", (hL, sL, vL))
        print("Upper HSV (360,100,100):", (hU, sU, vU))
        break

cv2.destroyAllWindows()
