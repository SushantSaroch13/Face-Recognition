# Face Recognition Attendance System

A **real-time face recognition based attendance system** built using Python and computer vision.
The system detects and recognizes faces from a webcam feed and automatically records attendance in a cloud database.

This project integrates **computer vision, machine learning, and cloud services** to create an automated attendance management solution.

---

## Features

* Real-time face detection using webcam
* Face recognition based attendance marking
* Cloud-based student database
* Automatic attendance tracking with timestamps
* Student profile display with image and details
* Prevents duplicate attendance within a short time window

---

## Technologies Used

| Technology                 | Purpose                             |
| -------------------------- | ----------------------------------- |
| OpenCV                     | Image processing and webcam capture |
| face_recognition           | Face encoding and recognition       |
| Firebase Realtime Database | Storing attendance and student data |
| Cloudinary                 | Hosting student profile images      |
| NumPy                      | Numerical operations                |

---

## System Workflow

1. Student images are collected and stored locally.
2. The **encoder script** generates facial encodings for each student.
3. Encodings are saved into a serialized file.
4. The main application captures webcam frames.
5. Faces are detected and compared with stored encodings.
6. When a match is found:

   * Student information is retrieved from the database.
   * Attendance is updated.
   * Student details are displayed on the UI.
---

## Main Components

### `Encoder.py`

* Reads student images from the **images folder**
* Generates face encodings using the face recognition model
* Stores encodings and student IDs in a serialized file.

Output file:

```
EncodeFile.p
```

---

### `AddDataDatabase.py`

* Uploads student data to the cloud database.

* Uploads profile images to the cloud storage.

* Stores student information including:

* Name

* Department

* Year

* Attendance count

* Last attendance timestamp

---

### `main.py`

Main application responsible for:

* Capturing webcam frames
* Detecting and recognizing faces
* Fetching student information from database
* Updating attendance records
* Displaying student information on screen

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/FaceAttendanceSystem.git
cd FaceAttendanceSystem
```

Install dependencies:

```bash
pip install opencv-python
pip install face_recognition
pip install cvzone
pip install firebase-admin
pip install numpy
pip install requests
```

---

## Running the System

### Step 1 — Encode Student Faces

```
python Encoder.py
```

This generates the file:

```
EncodeFile.p
```

---

### Step 2 — Upload Student Data

```
python AddDataDatabase.py
```

This uploads student information and images to the cloud database.

---

### Step 3 — Start Attendance System

```
python main.py
```

The webcam will start and automatically recognize students.

---

## Example Student Data

```
{
  "name": "Sushant Saroch",
  "department": "ECE",
  "year": 4,
  "total_attendance": 8,
  "standing": "G"
}
```

---

## Applications

* Automated classroom attendance
* Office employee attendance systems
* Smart campus systems
* Identity verification systems

---

## Future Improvements

* Mobile app integration
* Multiple camera support
* Attendance analytics dashboard
* Masked face recognition

---

## Author

**Sushant Saroch**
Electronics & Communication Engineer

Interests:

* Embedded Systems
* Artificial Intelligence
* Computer Vision
* IoT Hardware Development

---

⭐ If you find this project useful, consider starring the repository.
