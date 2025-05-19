import cv2
from ultralytics import YOLO
import torch
import numpy as np
import requests

url = "http://192.168.100.204:8080/shot.jpg"
model = YOLO("best2.pt")
device = 0 if torch.cuda.is_available() else 'cpu'
cv2.namedWindow("YOLO Webcam Inference", cv2.WINDOW_NORMAL)
cv2.namedWindow("Red Detection", cv2.WINDOW_NORMAL)
confidence = 0.5

def get_frame_from_url(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    return frame

def detect_and_show_red_hsv(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV ranges for red (covers both low and high hue reds)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    # Combine two red masks
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Apply mask to original frame
    red_detected = cv2.bitwise_and(frame, frame, mask=red_mask)
    cv2.imshow("Red Detection", red_detected)

while True:
    frame = get_frame_from_url(url)
    results = model.predict(frame, device=device, conf=confidence, verbose=False)

    for result in results:
        if result.obb is not None:
            obb_data = result.obb.xywhr.cpu().numpy()
            class_ids = result.obb.cls.cpu().numpy()
            for box, class_id in zip(obb_data, class_ids): 
                print("hi")

    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Webcam Inference", annotated_frame)

    detect_and_show_red_hsv(frame)  # HSV red detection

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
