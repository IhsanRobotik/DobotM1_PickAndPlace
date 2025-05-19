import cv2
from ultralytics import YOLO
import torch
import numpy as np
import requests

url = "http://192.168.100.204:8080/shot.jpg"
model = YOLO("best.pt")
device = 0 if torch.cuda.is_available() else 'cpu'
cv2.namedWindow("YOLO Webcam Inference", cv2.WINDOW_NORMAL)
confidence = 0.5

real_world_width_mm = 621
image_width_pixels = 1920

# y+ robot = x- real world, x+ robot = y+ real world
robot_x_ref_coordinate = -14
robot_y_ref_coordinate = 208.9
real_x_ref_coordinate = 1045.4 
real_y_ref_coordinate = 563.3


# hardcoded formula
conversion_factor = real_world_width_mm / image_width_pixels

def get_frame_from_url(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    return frame

def convert_to_real_coordinates(x_center, y_center):
    x_mm = x_center * conversion_factor
    y_mm = y_center * conversion_factor
    return x_mm, y_mm

while True:
    frame = get_frame_from_url(url)
    results = model.predict(frame, device=device, conf=confidence, verbose=False)

    for result in results:
        if result.obb is not None:
            obb_data = result.obb.xywhr.cpu().numpy()
            class_ids = result.obb.cls.cpu().numpy()  # Get class IDs

            for box, class_id in zip(obb_data, class_ids): 
                x_center, y_center, width, height, angle = box
                class_name = model.names[int(class_id)]  # Get class name

                x_mm, y_mm = convert_to_real_coordinates(x_center, y_center)
                print(f"Real-world coordinates: ({x_mm:.2f}, {y_mm:.2f}) mm")

    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Webcam Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
