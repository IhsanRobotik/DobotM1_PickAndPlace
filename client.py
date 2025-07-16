import socket
import requests
import numpy as np
import cv2

url = "http://192.168.100.216:8080/shot.jpg"

def get_frame_from_url(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    return frame

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9876))  # Connect to inference server

while True:
    frame = get_frame_from_url(url)
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = img_encoded.tobytes()
    length = len(img_bytes)
    client.sendall(length.to_bytes(4, byteorder='big'))
    client.sendall(img_bytes)

    response = client.recv(4096).decode()
    objects = response.split('|')
    for obj in objects:
        if not obj:
            continue
        x, y, r, cls = obj.split(',')
        print(f"X: {x}, Y: {y}, R: {r}, Class: {cls}")
