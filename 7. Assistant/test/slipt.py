# Chuỗi ví dụ
chuoi = "ID: 1725438055358\nConfirmed: None\nConfirmed_By: None\nName: Khưu Triều Minh Khang"

# Tách chuỗi theo dòng và lấy ký tự sau dấu :
dong_tach = [dong.split(": ")[1] for dong in chuoi.splitlines()]

# Gán từng giá trị vào các biến
id_ = dong_tach[0]
confirm = dong_tach[1]
doctor_name = dong_tach[2]
user_name = dong_tach[3]

# In ra các biến để kiểm tra
print("ID:", id_)
print("Confirm:", confirm)
print("Doctor Name:", doctor_name)
print("User Name:", user_name)
