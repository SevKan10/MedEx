import speech_recognition as sr
import pygame.mixer
from gtts import gTTS
import os
from unidecode import unidecode

# Khai báo thư viện và khởi tạo
recognizer = sr.Recognizer()
mic = sr.Microphone()
pygame.mixer.init()

face = 1  # Biến kiểm tra nhận diện khuôn mặt (giả sử đã nhận diện được)

# Hàm để phát âm thanh
def speak(text):
    tts = gTTS(text=text, lang='vi')
    tts.save("audio/output.mp3")
    pygame.mixer.music.load("audio/output.mp3")
    pygame.mixer.music.play()

# Hàm để lắng nghe người dùng
def listen():
    with mic as source:
        print("Robot đang lắng nghe...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio_data, language="vi")
        print(f"Người dùng: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Không nhận dạng được giọng nói.")
        return ""
    except sr.RequestError as e:
        print(f"Lỗi kết nối: {e}")
        return ""

# Hàm chính
def main():
    if face == 1:
        # Giả sử tên người dùng đã được nhận diện và lưu trong biến user_name
        user_name = "Khưu Triều Minh Khang"
        user_folder = unidecode(user_name)

        # Đường dẫn đến file dữ liệu của khách hàng
        file_path = f"img/{user_folder}/data/{user_folder}.txt"

        try:
            # Đọc file dữ liệu của khách hàng
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Tách chuỗi và gán các biến từ file
            line = [dong.split(": ")[1] for dong in content.splitlines()]
            id_ = line[0]
            confirm = line[1]
            doctor_name = line[2]
            user_name = line[3]

            # In ra các thông tin đã tách
            print(f"ID: {id_}")
            print(f"Confirm: {confirm}")
            print(f"Doctor Name: {doctor_name}")
            print(f"User Name: {user_name}")

            # Tạo lời chào và phát âm thanh
            voice = f"Xin chào {user_name}, tôi có thể giúp gì cho bạn?"
            speak(voice)

            # Lắng nghe phản hồi từ người dùng
            user_input = listen()

            # Xử lý phản hồi của người dùng
            if "đặt lịch hẹn" in user_input:
                response = "Bạn muốn đặt lịch hẹn với bác sĩ nào?"
                speak(response)
                # Tiếp tục xử lý...
            elif "cảm ơn" in user_input:
                response = "Rất hân hạnh được phục vụ bạn!"
                speak(response)
            elif user_input == "":
                response = "Tôi không nghe rõ, bạn có thể nói lại không?"
                speak(response)
            else:
                response = "Xin lỗi, tôi không hiểu yêu cầu của bạn."
                speak(response)

        except FileNotFoundError:
            print(f"Không thể tìm thấy file: {file_path}")
            speak("Xin lỗi, tôi không tìm thấy thông tin của bạn.")
        except Exception as e:
            print(f"Có lỗi xảy ra: {str(e)}")
            speak("Đã có lỗi xảy ra. Vui lòng thử lại sau.")

    else:
        print("Không nhận diện được khuôn mặt.")
        # Bạn có thể thêm chức năng xử lý khi không nhận diện được khuôn mặt

if __name__ == "__main__":
    main()
