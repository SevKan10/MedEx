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

# Đường dẫn file json, có thể chỉnh
fetched_users_file = 'Get fulldata/fetched_users.json'

# Load ID
if os.path.exists(fetched_users_file):
    with open(fetched_users_file, 'r') as file:
        fetched_users = json.load(file)
else:
    fetched_users = []

def save_fetched_users():
    with open(fetched_users_file, 'w') as file:
        json.dump(fetched_users, file)

# Lưu 
def write_user_data_and_image(user_id, user_data):
    user_folder = f'Get fulldata/{user_id}' # Chỉnh đường dẫn ở đây
    os.makedirs(user_folder, exist_ok=True)
    
    # Lưu vào dạng txt
    with open(f"{user_folder}/{user_data.get('Name', 'N/A')}.txt", 'w', encoding='utf-8') as file:
        file.write(f"ID: {user_id}\n")
        file.write(f"Confirmed: {user_data.get('Confirmed', 'N/A')}\n")
        file.write(f"Confirmed_By: {user_data.get('Confirmed_By', 'N/A')}\n")
        file.write(f"Name: {user_data.get('Name', 'N/A')}\n")
    
    # Tải ảnh
    cloudpath = f"images/{user_id}"  
    local_image_path = f"{user_folder}/{user_data.get('Name', 'N/A')}.png"  
    
    try:
        storage.child(cloudpath).download("", local_image_path)
        print(f"Image for user {user_id} downloaded successfully.")
    except Exception as e:
        print(f"An error occurred while downloading the image for user {user_id}: {e}")

# Lấy user mới
def fetch_new_users():
    ref = db.reference('user')
    users = ref.get()

    if users:
        new_users = {}
        for user_id, user_data in users.items():
            if user_id not in fetched_users:
                filtered_data = {
                    'Confirmed': user_data.get('Confirmed'),
                    'Confirmed_By': user_data.get('Confirmed_By'),
                    'Name': user_data.get('Name')
                }

                write_user_data_and_image(user_id, filtered_data)
                
                fetched_users.append(user_id)
                new_users[user_id] = filtered_data

        save_fetched_users()
        return new_users
    return {}

if __name__ == "__main__":
    new_users = fetch_new_users()
    if new_users:
        print(f"Saved {len(new_users)} new users with their images.")
    else:
        print("No new users found.")
