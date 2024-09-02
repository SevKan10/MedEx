import firebase_admin
from firebase_admin import credentials, storage

# Khởi tạo Firebase với khóa JSON của tài khoản dịch vụ
cred = credentials.Certificate('medex.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'medex-7ff53.appspot.com'
})

def download_file(file_path, destination_file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    
    try:
        blob.download_to_filename(destination_file_name)
        print(f'File {file_path} downloaded to {destination_file_name}.')
    except Exception as e:
        print(f'Error downloading file: {e}')

# Tải ảnh từ Firebase Storage
file_path = 'images/1724344077215.jpg'  # Đường dẫn tệp trong Firebase Storage
destination_file_name = '1724344077215.jpg'  # Đường dẫn tệp lưu trữ cục bộ

download_file(file_path, destination_file_name)
