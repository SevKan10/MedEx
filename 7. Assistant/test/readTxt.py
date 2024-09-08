user_name = "Khưu Triều Minh Kh"

# Mở file văn bản với mã hóa UTF-8
file_path = f"img/{user_name}/data/{user_name}.txt"  # Thay đổi thành đường dẫn của file thực tế
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        # Đọc nội dung của file
        content = file.read()
        print(content)  # In ra nội dung của file
except UnicodeDecodeError:
    print(f"Không thể giải mã file với mã hóa UTF-8. Thử sử dụng mã hóa khác.")
    try:
        # Thử sử dụng mã hóa khác như 'ISO-8859-1' hoặc 'cp1252'
        with open(file_path, 'r', encoding='cp1252') as file:
            content = file.read()
            print(content)
    except Exception as e:
        print(f"Có lỗi xảy ra khi đọc file với mã hóa khác: {str(e)}")
except FileNotFoundError:
    print(f"Không thể tìm thấy file: {file_path}")
except Exception as e:
    print(f"Có lỗi xảy ra khi đọc file: {str(e)}")
