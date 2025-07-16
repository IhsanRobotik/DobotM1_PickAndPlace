import cv2
import numpy as np
import requests

real_world_width_mm = 695
image_width_pixels = 1920

# hardcoded formula
conversion_factor = real_world_width_mm / image_width_pixels

cv2.namedWindow("Hello", cv2.WINDOW_NORMAL)

def get_frame_from_url(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    return frame

def convert_to_real_coordinates(x_center, y_center):
    x_mm = x_center * conversion_factor
    y_mm = y_center * conversion_factor
    return x_mm, y_mm

url = "http://192.168.100.216:8080/shot.jpg"

lower_green = [83, 49, 63]
upper_green = [123, 69, 83]

lower_yellow = [33, 68, 88]
upper_yellow = [73, 88, 100]

def convert_to_cv_scale(lower, upper):
    lower_cv = np.array([
        int(lower[0] / 2),
        int(lower[1] * 255 / 100),
        int(lower[2] * 255 / 100)
    ])

    upper_cv = np.array([
        int(upper[0] / 2),
        int(upper[1] * 255 / 100),
        int(upper[2] * 255 / 100)
    ])

    return lower_cv, upper_cv

lower_green_cv, upper_green_cv = convert_to_cv_scale(lower_green, upper_green)
lower_yellow_cv, upper_yellow_cv = convert_to_cv_scale(lower_yellow, upper_yellow)

while True:
    frame = get_frame_from_url(url)
    if frame is None:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green_cv, upper_green_cv)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        mask = cv2.inRange(hsv, lower_yellow_cv, upper_yellow_cv)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) < 100:
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

        angle = rect[2]
        if rect[1][0] < rect[1][1]:
            angle += 90

        center = tuple(np.intp(rect[0]))
        print(center[0], center[1])
        x_mm, y_mm = convert_to_real_coordinates(center[0], center[1])
        print(x_mm,y_mm)
        cv2.putText(frame, f"{angle:.2f} deg", center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.circle(frame, center, 4, (0, 255, 255), -1)

    cv2.imshow("Hello", frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
