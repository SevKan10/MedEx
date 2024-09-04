import pyrebase
import firebase_admin
from firebase_admin import credentials, db
import json
import os

config = {
    "apiKey": "AIzaSyDoWySbs3R0yKWsRTgRK54pLgudr8Srcfo",
    "authDomain": "medical-examiner-40e4d.firebaseapp.com",
    "databaseURL": "https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "medical-examiner-40e4d",
    "storageBucket": "medical-examiner-40e4d.appspot.com",
    "messagingSenderId": "592499333547",
    "appId": "1:592499333547:web:a830daa4140cf1ca515aee"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

cred = credentials.Certificate('test/medical-examiner.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

fetched_users_file = 'Get fulldata/fetched_users.json'

if os.path.exists(fetched_users_file):
    with open(fetched_users_file, 'r') as file:
        fetched_users = json.load(file)
else:
    fetched_users = []

def save_fetched_users():
    with open(fetched_users_file, 'w') as file:
        json.dump(fetched_users, file)

def get_next_folder_number():
    existing_folders = [d for d in os.listdir('Get fulldata') if os.path.isdir(os.path.join('Get fulldata', d))]
    if existing_folders:
        max_number = max([int(folder) for folder in existing_folders if folder.isdigit()])
    else:
        max_number = 0
    return max_number + 1

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()

def write_user_data_and_image(userID, user_data):
    folder_number = get_next_folder_number()
    user_folder = f'Get fulldata/{folder_number}'
    os.makedirs(user_folder, exist_ok=True)
    
    # Lưu vào dạng txt với tên là tên người dùng
    user_name = sanitize_filename(user_data.get('Name', 'N/A'))
    txt_filename = f"{user_folder}/{user_name}.txt"
    
    with open(txt_filename, 'w', encoding='utf-8') as file:
        file.write(f"ID: {userID}\n")
        file.write(f"Confirmed: {user_data.get('Confirmed', 'N/A')}\n")
        file.write(f"Confirmed_By: {user_data.get('Confirmed_By', 'N/A')}\n")
        file.write(f"Name: {user_data.get('Name', 'N/A')}\n")
    
    # Tải ảnh
    cloudpath = f"images/{userID}"
    local_image_path = f"{user_folder}/{user_name}.png"
    
    try:
        storage.child(cloudpath).download("", local_image_path)
        print(f"Image for user {userID} downloaded successfully.")
    except Exception as e:
        print(f"An error occurred while downloading the image for user {userID}: {e}")

def fetch_new_users():
    ref = db.reference('user')
    users = ref.get()

    if users:
        new_users = {}
        for userID, user_data in users.items():
            if userID not in fetched_users:
                filtered_data = {
                    'Confirmed': user_data.get('Confirmed'),
                    'Confirmed_By': user_data.get('Confirmed_By'),
                    'Name': user_data.get('Name')
                }

                write_user_data_and_image(userID, filtered_data)
                
                fetched_users.append(userID)
                new_users[userID] = filtered_data

        save_fetched_users()
        return new_users
    return {}

if __name__ == "__main__":
    new_users = fetch_new_users()
    if new_users:
        print(f"Saved {len(new_users)} new users with their images.")
    else:
        print("No new users found.")
