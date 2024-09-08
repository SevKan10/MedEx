import firebase_admin
from firebase_admin import credentials, db
import json
import os

# Khởi tạo Firebase
cred = credentials.Certificate('medical-examiner.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Tải dữ liệu người dùng từ file (nếu cần)
user_data_file = 'fetched_users.json'
if os.path.exists(user_data_file):
    with open(user_data_file, 'r') as file:
        user_data = json.load(file)
else:
    user_data = []

# Hàm đọc user_id từ file .txt
def read_user_id_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Tách chuỗi và gán các biến từ file
        lines = [line.split(": ")[1] for line in content.splitlines()]
        id_ = lines[0]  # user_id là dòng đầu tiên
        return id_
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        return None
    except Exception as e:
        print(f"Có lỗi xảy ra khi đọc file: {str(e)}")
        return None

# Hàm đẩy dữ liệu Temp, Heart, và STT lên Firebase
def push_data(user_folder, Temp, Heart, STT):
    # Đường dẫn tới file txt chứa thông tin user (thay thế đường dẫn đúng)
    file_path = f"img/{user_folder}/data/{user_folder}.txt"

    # Lấy user_id từ file .txt
    user_id = read_user_id_from_txt(file_path)

    if user_id:
        if user_id in user_data:
            # Đẩy dữ liệu lên Firebase
            ref = db.reference(f'user/{user_id}')
            ref.update({
                'Temp': Temp,
                'Heart': Heart,
                'STT': STT  # Số thứ tự
            })
            print(f"Đã cập nhật dữ liệu cho User ID: {user_id}")
        else:
            print(f"User ID {user_id} không có trong dữ liệu.")
    else:
        print("Không thể lấy user_id từ file.")

# Ví dụ sử dụng
if __name__ == "__main__":
    user_folder = ""  # Thay bằng thư mục người dùng thực tế
    Temp = 80
    Heart = 75
    STT = 1  # Số thứ tự ví dụ
    push_data(user_folder, Temp, Heart, STT)
