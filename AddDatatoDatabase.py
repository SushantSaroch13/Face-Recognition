#! D:\FaceAttendanceSystem\myenv\Scripts\python.exe

import cloudinary
import cloudinary.uploader
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Cloudinary
cloudinary.config(
    cloud_name='dkzv4x0sg',
    api_key='798985962888575',
    api_secret='LAUhEvHFHlOn6Mfd6nQqY-qSPWU'
)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancesystem-7fa78-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

# Sample Data (Update with actual image paths)
data = {
    "1234": {
        "name": "Elon Musk",
        "department": "CSE",
        "starting_year": 2007,
        "total_attendance": 6,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34",
        "profile_image_path": "Images/1234.png"
    },
    "4321": {
        "name": "John Cena",
        "department": "Wrestling",
        "starting_year": 2006,
        "total_attendance": 2,
        "standing": "B",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34",
        "profile_image_path": "Images/4321.png"
    },
    "4132": {
        "name": "Sushant Saroch",
        "department": "ECE",
        "starting_year": 2021,
        "total_attendance": 8,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34",
        "profile_image_path": "Images/4132.png"
    },
    "0012": {
        "name": "Dhrauv",
        "department": "ECE",
        "starting_year": 2021,
        "total_attendance": 0,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34",
        "profile_image_path": "Images/0012.png"
    }
}

# Upload Images to Cloudinary and Add URLs to Student Data
def upload_image_to_cloudinary(image_path):
    try:
        response = cloudinary.uploader.upload(
            image_path,
            folder="students_images",  # Save in the "students_images" folder
            use_filename=True,  # Keep the original file name
            unique_filename=False  # Prevent Cloudinary from appending a unique string to the file name
        )
        return response.get('secure_url')
    except Exception as e:
        print(f"Failed to upload image: {e}")
        return None

# Update Student Data with Image URLs and Push to Firebase
for key, value in data.items():
    image_path = value.pop("profile_image_path", None)
    if image_path:
        image_url = upload_image_to_cloudinary(image_path)
        if image_url:
            value["profile_image"] = image_url  # Add the image URL to student data
        else:
            value["profile_image"] = "Image upload failed"
    else:
        value["profile_image"] = "No image provided"
    
    # Push updated student data to Firebase
    ref.child(key).set(value)
    print(f"Uploaded data for student {key}: {value}")