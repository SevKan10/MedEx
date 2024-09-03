import firebase_admin
from firebase_admin import credentials, db
import json
import os

# Khởi tạo Firebase
cred = credentials.Certificate('medical-examiner.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Đường dẫn tới file lưu trữ dữ liệu người dùng
user_data_file = 'fetched_users.json'

# Đường dẫn tới file để chỉ định user_id cụ thể
specific_user_id_file = 'user.json'

# Tải dữ liệu người dùng từ file
if os.path.exists(user_data_file):
    with open(user_data_file, 'r') as file:
        user_data = json.load(file)
else:
    user_data = []

# Tải user_id cụ thể từ file
if os.path.exists(specific_user_id_file):
    with open(specific_user_id_file, 'r') as file:
        specific_user_id = json.load(file).get('user_id')
else:
    specific_user_id = None

# Hàm đẩy dữ liệu Temp và Heart cố định lên Firebase
def push_temp_and_heart_to_firebase(user_id):
    ref = db.reference(f'user/{user_id}')
    ref.update({
        'Temp': 80,
        'Heart': 80
    })
    print(f"Đã cập nhật dữ liệu cố định cho User ID: {user_id}")

# Đẩy dữ liệu cho một user cụ thể
def push_data():
    if specific_user_id:
        if specific_user_id in user_data:
            push_temp_and_heart_to_firebase(specific_user_id)
        else:
            print(f"User ID {specific_user_id} không có trong dữ liệu.")
    else:
        print("Không có user_id cụ thể được chỉ định.")

if __name__ == "__main__":
    push_data()
