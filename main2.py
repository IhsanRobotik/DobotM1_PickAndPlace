import cv2
from ultralytics import YOLO
import torch
import numpy as np
import requests
import math
from serverClass import Server
import time

# variable declaration
x_mm = 0
y_mm = 0

# hardcoded values
confidence = 0.8
real_world_width_mm = 640
image_width_pixels = 1920

# y+ robot = x- real world, x+ robot = y+ real world
robot_x_ref_coordinate = 172
robot_y_ref_coordinate = -180
real_x_ref_coordinate = 450.60
real_y_ref_coordinate = 161.60


# hardcoded formula
conversion_factor = real_world_width_mm / image_width_pixels

server = Server()
server.start()

url = "http://192.168.100.231:8080/shot.jpg"
model = YOLO("best.pt")
device = 0 if torch.cuda.is_available() else 'cpu'
cv2.namedWindow("YOLO Webcam Inference", cv2.WINDOW_NORMAL)

def get_frame_from_url(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    return frame

def convert_to_real_coordinates(x_center, y_center):
    x_mm = x_center * conversion_factor
    y_mm = y_center * conversion_factor
    return x_mm, y_mm

def convert_to_robot_coordinates(x_mm, y_mm):
    # Real world offsets relative to a known reference
    delta_x = x_mm - real_x_ref_coordinate
    delta_y = y_mm - real_y_ref_coordinate

    # Apply coordinate transformation based on direction mapping
    robot_x = robot_x_ref_coordinate + delta_y  # x+ robot = y+ real
    robot_y = robot_y_ref_coordinate - delta_x  # y+ robot = x- real

    return robot_x, robot_y


while True:
    frame = get_frame_from_url(url)

    # height, width, _ = frame.shape
    # print(width, height)

    results = model.predict(frame, device=device, conf=confidence, verbose=False)

    for result in results:
        if result.obb is not None:
            obb_data = result.obb.xywhr.cpu().numpy()
            class_ids = result.obb.cls.cpu().numpy()  # Get class IDs

            for box, class_id in zip(obb_data, class_ids):
                x_center, y_center, width, height, angle = box
                angle = math.degrees(angle)
                class_name = model.names[int(class_id)]  # Get class name

                # Display x_center and y_center on the annotated frame
                text = f"({x_center:.2f}, {y_center:.2f})"
                cv2.circle(frame, (int(x_center), int(y_center)), 5, (0, 255, 0), -1)

                # Convert to real-world coordinates
                x_mm, y_mm = convert_to_real_coordinates(x_center, y_center)
                robot_x, robot_y = convert_to_robot_coordinates(x_mm, y_mm)

                # print(f"Class: {class_name}, Angle: {angle}, Center: {text}")
                # print(f"Real Coordinates: ({x_mm:.2f}, {y_mm:.2f}) mm")

                print(f"Robot Coordinates: ({robot_x:.2f}, {robot_y:.2f}) mm")
            # server.send_message(f"Class: {class_name}, Angle: {angle}, Center: {text}")


    dobot_message = server.read_message()
    if dobot_message == "ok":
        server.send_message(f"{float(robot_x), float(robot_y)}")

    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Webcam Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
