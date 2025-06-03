# Dobot M1 Vision-Based Pick and Place

A computer vision pipeline for Dobot M1, using YOLO for object detection and coordinate transformation for robotic pick and place tasks.

---

## Features

- Real-time object detection using YOLO
- Coordinate conversion from camera to Dobot M1 robot space
- Socket communication between vision system and Dobot M1 Studio

---

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/IhsanRobotik/DobotM1_PickAndPlace.git
cd DobotM1_PickAndPlace
```

### 2. Install Python Requirements

This project was build with python 11, you might be able to use other version but its recomended to use the same version.
Also it is recommended to use a Python virtual environment to manage dependencies.

1. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

2. **Activate the virtual environment:**

    ```sh
    .\venv\Scripts\activate
    ```

3. **Install the requirements:**

    ```sh
    pip install -r requirements.txt
    ```
---

## Dobot M1 Studio Setup

1. **Download and Install Dobot M1 Studio**  
   - [Dobot M1 Studio Download Page](https://www.dobot.cc/downloadcenter/dobot-m1.html)
   - Follow the official installation instructions for your operating system.

2. **Connect Dobot M1 to your PC**  
   - Use USB or network connection as described in the Dobot M1 Studio manual.

---

## Usage

### 1. Start the Vision Inference Server

Run the main Python script:

```sh
python main.py
```

This will start the vision system and open a socket server to communicate with Dobot M1 Studio.

### 2. Run the Pick and Place Script in Dobot M1 Studio

- Open Dobot M1 Studio.
- Load the `Pick and place.script` file from this repository.
- Run the script.  
  The robot will receive coordinates from the vision system and perform pick and place operations.

---

## Notes

- Adjust camera calibration and reference coordinates in `main.py` as needed for your setup.
- Make sure the camera stream URL in `main.py` matches your actual camera.

---

## License

MIT License

---

## Acknowledgements

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [Dobot Official](https://www.dobot.cc/)