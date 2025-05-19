import os
import cv2
import numpy as np
import requests
from datetime import datetime

url = "http://192.168.100.204:8080/shot.jpg"
cv2.namedWindow("YOLO Webcam Inference", cv2.WINDOW_NORMAL)

def get_frame_from_url(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    return frame

def save_frame(frame, directory="./captured"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(directory, filename)
    cv2.imwrite(filepath, frame)
    print(f"Frame saved to {filepath}")

def main():
    while True:
        frame = get_frame_from_url(url)
        if frame is None:
            print("Failed to get frame.")
            continue

        cv2.imshow("YOLO Webcam Inference", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            save_frame(frame)
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()