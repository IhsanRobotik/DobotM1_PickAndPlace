import socket
import cv2
import numpy as np
from ultralytics import YOLO
import torch
import math

model = YOLO("best3.pt")
device = 0 if torch.cuda.is_available() else 'cpu'

host = '0.0.0.0'
port = 9876

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)
conn, _ = server.accept()

def process_image(image):
    results = model.predict(image, device=device, conf=0.92, verbose=False)
    output = []
    for result in results:
        if result.obb is not None:
            obb_data = result.obb.xywhr.cpu().numpy()
            class_ids = result.obb.cls.cpu().numpy()
            for box, class_id in zip(obb_data, class_ids):
                x, y, w, h, r = box[:5]
                r = math.degrees(r)
                output.append((x, y, r, int(class_id)))
    return output

while True:
    length_bytes = conn.recv(4)
    if not length_bytes:
        break
    length = int.from_bytes(length_bytes, byteorder='big')
    img_bytes = b''
    while len(img_bytes) < length:
        img_bytes += conn.recv(length - len(img_bytes))
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    results = process_image(frame)
    response = '|'.join([f"{x:.2f},{y:.2f},{r:.2f},{cls}" for x, y, r, cls in results])
    conn.sendall(response.encode())
