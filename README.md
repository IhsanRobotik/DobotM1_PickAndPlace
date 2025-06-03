# Dobot M1 Vision-Based Pick and Place

A computer vision pipeline for Dobot M1, using YOLO for object detection and coordinate transformation for robotic pick and place tasks.

## Demo Video
[![Demo Video](https://img.youtube.com/vi/qJpISdlPttE/0.jpg)](https://youtu.be/qJpISdlPttE)

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
   - [Dobot M1 Studio Download Page](https://www.dobot-robots.com/service/download-center)
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

---

# 🇮🇩 Versi Bahasa Indonesia

## Dobot M1 Vision-Based Pick and Place

Sebuah pipeline computer vision untuk Dobot M1, menggunakan YOLO untuk deteksi objek dan transformasi koordinat untuk tugas pick and place robotik.

---

## Fitur

- Deteksi objek secara real-time menggunakan YOLO
- Konversi koordinat dari kamera ke ruang robot Dobot M1
- Komunikasi socket antara sistem visi dan Dobot M1 Studio

---

## Instalasi

### 1. Clone Repository

```sh
git clone https://github.com/IhsanRobotik/DobotM1_PickAndPlace.git
cd DobotM1_PickAndPlace
```

### 2. Instalasi Kebutuhan Python

Proyek ini dibuat dengan Python 11, disarankan menggunakan versi yang sama.  
Sebaiknya gunakan virtual environment untuk mengelola dependensi.

1. **Buat virtual environment:**

    ```sh
    python -m venv venv
    ```

2. **Aktifkan virtual environment:**

    ```sh
    .\venv\Scripts\activate
    ```

3. **Instalasi requirements:**

    ```sh
    pip install -r requirements.txt
    ```

---

## Instalasi Dobot M1 Studio

1. **Unduh dan Instal Dobot M1 Studio**  
   - [Halaman Unduh Dobot M1 Studio](https://www.dobot-robots.com/service/download-center)
   - Ikuti petunjuk instalasi resmi sesuai sistem operasi Anda.

2. **Hubungkan Dobot M1 ke PC**  
   - Gunakan koneksi USB atau jaringan sesuai manual Dobot M1 Studio.

---

## Penggunaan

### 1. Jalankan Vision Inference Server

Jalankan skrip utama Python:

```sh
python mainWebcam.py
```

Ini akan memulai sistem visi dan membuka socket server untuk komunikasi dengan Dobot M1 Studio.

### 2. Jalankan Skrip Pick and Place di Dobot M1 Studio

- Buka Dobot M1 Studio.
- Muat file `Pick and place.script` dari repository ini.
- Jalankan skrip tersebut.  
  Robot akan menerima koordinat dari sistem visi dan melakukan operasi pick and place.

---

## Catatan

- Sesuaikan kalibrasi kamera dan referensi koordinat di `main.py` sesuai kebutuhan.
- Pastikan URL stream kamera di `main.py` sesuai dengan kamera Anda.

---

## Lisensi

MIT License

---

## Kredit

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [Dobot Official](https://www.dobot.cc/)