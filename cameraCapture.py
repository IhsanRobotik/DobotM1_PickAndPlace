import cv2
import os

# IP camera stream URL
url = "http://192.168.100.231:8080/video"

# Open a connection to the IP camera
cap = cv2.VideoCapture(url)

# Ensure the output directory exists
save_path = "./img"
os.makedirs(save_path, exist_ok=True)

# Check if the connection was successful
if not cap.isOpened():
    print("Failed to connect to the camera.")
else:
    count = 0  # Initialize image counter

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.")
            break

        # Show the camera feed
        cv2.imshow("IP Camera", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):  # Press 'q' to save image
            count += 1
            image_file = os.path.join(save_path, f"image{count}.jpg")
            cv2.imwrite(image_file, frame)
            print(f"Image saved to {image_file}")
        elif key == 27:  # Press ESC to exit
            break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
