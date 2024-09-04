import firebase_admin
from firebase_admin import credentials, db
import json
import os

# Khởi tạo Firebase
cred = credentials.Certificate('test/medical-examiner.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Đường dẫn tới file lưu trữ ID người dùng đã lấy về
fetched_users_file = 'test/fetched_users.json'
# Đường dẫn tới file txt để lưu dữ liệu người dùng
output_file = 'test/user_data.txt'

# Tải các ID người dùng đã lấy về từ file
if os.path.exists(fetched_users_file):
    with open(fetched_users_file, 'r') as file:
        fetched_users = json.load(file)
else:
    fetched_users = []

def save_fetched_users():
    with open(fetched_users_file, 'w') as file:
        json.dump(fetched_users, file)

# Hàm ghi dữ liệu người dùng vào file txt
def write_user_data_to_file(user_id, user_data):
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(f"{user_id}\n") #ID
        file.write(f"{user_data.get('Confirmed', 'N/A')}\n") #Xác nhận
        file.write(f"{user_data.get('Confirmed_By', 'N/A')}\n") #Người xác nhận
        file.write(f"{user_data.get('Name', 'N/A')}\n") #Tên
        file.write("\n")

# Hàm lấy người dùng mới
def fetch_new_users():
    # Tham chiếu tới người dùng trong cơ sở dữ liệu
    ref = db.reference('user')
    users = ref.get()

    if users:
        new_users = {}
        for user_id, user_data in users.items():
            if user_id not in fetched_users:
                # Chỉ lưu trữ các trường cần thiết
                filtered_data = {
                    'Confirmed': user_data.get('Confirmed'),
                    'Confirmed_By': user_data.get('Confirmed_By'),
                    'Name': user_data.get('Name')
                }

                # Thêm dữ liệu của người dùng mới vào dictionary new_users
                new_users[user_id] = filtered_data
                fetched_users.append(user_id)

                # Ghi dữ liệu người dùng vào file txt
                write_user_data_to_file(user_id, filtered_data)

        # Lưu lại các ID người dùng đã lấy về
        save_fetched_users()

        return new_users
    return {}

if __name__ == "__main__":
    # Lấy người dùng mới
    new_users = fetch_new_users()

    if new_users:
        print(f"Đã lưu {len(new_users)} người dùng mới vào file {output_file}.")
    else:
        print("Không có người dùng mới.")
