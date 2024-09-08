import os
import pyrebase
import firebase_admin
from firebase_admin import credentials, db
import json
import unidecode

# Cấu hình Firebase
config = {
    "apiKey": "AIzaSyDoWySbs3R0yKWsRTgRK54pLgudr8Srcfo",
    "authDomain": "medical-examiner-40e4d.firebaseapp.com",
    "databaseURL": "https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "medical-examiner-40e4d",
    "storageBucket": "medical-examiner-40e4d.appspot.com",
    "messagingSenderId": "592499333547",
    "appId": "1:592499333547:web:a830daa4140cf1ca515aee"
}

# Khởi tạo Firebase
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# Xác thực Firebase Admin SDK
cred = credentials.Certificate('Get fulldata/medical-examiner.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Đường dẫn tệp đã lấy dữ liệu
fetched_users_file = 'Get fulldata/fetched_users.json'

# Kiểm tra và tải danh sách người dùng đã được lấy trước đó
if os.path.exists(fetched_users_file):
    with open(fetched_users_file, 'r') as file:
        fetched_users = json.load(file)
else:
    fetched_users = []

def save_fetched_users():
    """Lưu danh sách người dùng đã được lấy vào file."""
    with open(fetched_users_file, 'w') as file:
        json.dump(fetched_users, file)

# Hàm để chuyển đổi chuỗi có dấu thành chuỗi không dấu và loại bỏ các ký tự không hợp lệ
def sanitize_filename(name):
    # Chuyển đổi tên có dấu thành không dấu
    name = unidecode.unidecode(name)
    # Loại bỏ các ký tự không hợp lệ, chỉ giữ lại chữ cái, số, dấu cách, gạch dưới và gạch ngang
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()

# Hàm để lưu dữ liệu người dùng và tải ảnh về thư mục tương ứng
def write_user_data_and_image(userID, user_data):
    # Lấy tên người dùng và làm sạch tên
    user_name = sanitize_filename(user_data.get('Name', 'N/A'))
    
    # Tạo thư mục img của người dùng
    user_folder = f'img/{user_name}'
    os.makedirs(user_folder, exist_ok=True)
    
    # Tạo thư mục data bên trong thư mục người dùng
    user_data_folder = os.path.join(user_folder, 'data')
    os.makedirs(user_data_folder, exist_ok=True)

    # Tạo file txt chứa thông tin người dùng
    txt_filename = os.path.join(user_data_folder, f"{user_name}.txt")
    with open(txt_filename, 'w', encoding='utf-8') as file:
        file.write(f"ID: {userID}\n")
        file.write(f"Confirmed: {user_data.get('Confirmed', 'N/A')}\n")
        file.write(f"Confirmed_By: {user_data.get('Confirmed_By', 'N/A')}\n")
        file.write(f"Name: {user_data.get('Name', 'N/A')}\n")
    
    # Tải ảnh về thư mục img của người dùng
    cloudpath = f"images/{userID}"
    local_image_path = os.path.join(user_folder, f"{user_name}.png")
    
    try:
        storage.child(cloudpath).download("", local_image_path)
        print(f"Image for user {userID} downloaded successfully.")
    except Exception as e:
        print(f"An error occurred while downloading the image for user {userID}: {e}")
        
# Hàm lấy người dùng mới từ cơ sở dữ liệu Firebase
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

# Chạy chương trình
if __name__ == "__main__":
    new_users = fetch_new_users()
    if new_users:
        print(f"Saved {len(new_users)} new users with their images.")
    else:
        print("No new users found.")
