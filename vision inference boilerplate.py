import cv2
from ultralytics import YOLO
import torch
import numpy as np
import requests
import math

cam = cv2.VideoCapture(1)

url = "http://192.168.100.201:8080/shot.jpg"
model = YOLO("best3.pt")
device = 0 if torch.cuda.is_available() else 'cpu'
cv2.namedWindow("YOLO Webcam Inference", cv2.WINDOW_NORMAL)
confidence = 0.92

real_world_width_mm = 565
image_width_pixels = 640

# y+ robot = x- real world, x+ robot = y+ real world
robot_x_ref_coordinate = -14
robot_y_ref_coordinate = 208.9
real_x_ref_coordinate = 1045.4 
real_y_ref_coordinate = 563.3


# hardcoded formula
conversion_factor = real_world_width_mm / image_width_pixels

robot_x_ref_coordinate = 204.6
robot_y_ref_coordinate = -119
real_x_ref_coordinate = 233.14
real_y_ref_coordinate = 127.2

# def convert_to_robot_coordinates(x_mm, y_mm):
#     # Real world offsets relative to a known reference
#     delta_x = y_mm - real_x_ref_coordinate
#     delta_y = x_mm - real_y_ref_coordinate

#     # Apply coordinate transformation based on direction mapping
#     robot_x = robot_x_ref_coordinate + delta_y  # x+ robot = y+ real
#     robot_y = robot_y_ref_coordinate + delta_x  # y+ robot = x+ real

#     return robot_x, robot_y

def convert_to_robot_coordinates(x_mm, y_mm):
    # Real world offsets relative to a known reference
    delta_x = x_mm - real_x_ref_coordinate
    delta_y = y_mm - real_y_ref_coordinate

    # Apply coordinate transformation based on new direction mapping:
    # +y real = +x robot, +x real = +y robot
    robot_x = robot_x_ref_coordinate + delta_y
    robot_y = robot_y_ref_coordinate + delta_x

    return robot_x, robot_y

def get_frame_from_url(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    return frame

def convert_to_real_coordinates(x_center, y_center):
    x_mm = x_center * conversion_factor
    y_mm = y_center * conversion_factor
    return x_mm, y_mm

def calculate_rotation(box):
    x, y, w, h, r = box[:5] 
    if w < h:
        w, h = h, w
        r += math.pi / 2  # Adjust rotation angle by 90 degrees

    # Convert rotation angle to degrees
    r = math.degrees(r)

    # Calculate the endpoint of the line
    x_end = x + w * math.cos(math.radians(r))
    y_end = y + w * math.sin(math.radians(r))

    # Draw the line
    cv2.line(frame, (int(x), int(y)), (int(x_end), int(y_end)), (0, 255, 0), 2)
    return r

while True:
    ret, frame = cam.read()
    if not ret or frame is None:
        continue
    # print(frame.shape)
    results = model.predict(frame, device=device, conf=confidence, verbose=False)

    for result in results:
        if result.obb is not None:
            obb_data = result.obb.xywhr.cpu().numpy()
            class_ids = result.obb.cls.cpu().numpy()  # Get class IDs

            for box, class_id in zip(obb_data, class_ids): 
                x_center, y_center, width, height, angle = box
                class_name = model.names[int(class_id)]  # Get class name

                x_mm, y_mm = convert_to_real_coordinates(x_center, y_center)

                print(f"Class: {class_name}, X: {x_mm:.2f} mm, Y: {y_mm:.2f} mm")
                r = calculate_rotation(box)
                # print(f"Rotation: {r:.2f} degrees")
                robot_x, robot_y = convert_to_robot_coordinates(x_mm, y_mm)
                # print(f"Robot Coordinates: X: {robot_x:.2f}, Y: {robot_y:.2f}", r)


    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Webcam Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
