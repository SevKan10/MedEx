import speech_recognition as sr
import pygame.mixer
from gtts import gTTS
import os
import time
from unidecode import unidecode  
from datetime import date, datetime
import pytz

# --------------------------------------- Khai báo thư viện
recognizer = sr.Recognizer()
mic = sr.Microphone()
pygame.mixer.init()

today = date.today()
now = datetime.now()
tz_VN = pytz.timezone('Asia/Ho_Chi_Minh')
###############################################################################
flagFace = 1  # Biến kiểm tra nhận diện khuôn mặt                             #
user_name = "Khưu Triều Minh Khang"  # Thông tin khách hàng (tên có dấu)      #
user_folder = unidecode(user_name)                                            #
                                #biến test                                    #
                                # main(unidecode(user_name), 1)               #
###############################################################################

def robotListen():
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

def robotSpeak(text):
    # Sử dụng timestamp để tạo tên file duy nhất
    timestamp = int(time.time())  # Lấy thời gian hiện tại (giây)
    file_name = f"audio/output_{timestamp}.mp3"  # Tạo tên file duy nhất
    
    tts = gTTS(text=text, lang='vi')
    tts.save(file_name)
    
    # Phát file âm thanh
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    
    # Đợi cho đến khi âm thanh kết thúc
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)  # Kiểm tra cứ sau 0.1 giây xem âm thanh đã phát xong chưa

def greet_user(file_path, STT):
    try:
        # Đọc file dữ liệu của khách hàng
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Tách chuỗi và gán các biến từ file
        line = [dong.split(": ")[1] for dong in content.splitlines()]
        confirm = line[1]
        doctor_name = line[2]
        user_name = line[3]

        voice = f"Xin chào {user_name}, tôi là rô bốt hỗ trợ khám bệnh"
        robotSpeak(voice)

        if confirm == "True":
            voice = f"bạn đã được bác sĩ {doctor_name} xác nhận khám bệnh, số thứ tự của bạn là {STT}. Bạn vui lòng để tay lên cảm biến nhịp tim để tiến hành đo."
            robotSpeak(voice)
        else:
            voice = f"bạn chưa được bác sĩ nào xác nhận khám bệnh, số thứ tự của bạn là {STT}. Bạn vui lòng để tay lên cảm biến nhịp tim để tiến hành đo, sau đó đi đến quầy để được hỗ trợ thêm."
            robotSpeak(voice)

    except FileNotFoundError:
        print(f"Không thể tìm thấy file: {file_path}")
        robotSpeak("Xin lỗi, tôi không tìm thấy thông tin của bạn.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")
        robotSpeak("Đã có lỗi xảy ra. Vui lòng thử lại sau.")

def heartAndTemp(temp, heart):
    voice = f"nhiệt độ của bạn là {temp}, nhịp tim của bạn là {heart}"
    robotSpeak(voice)

def pressureFinish():
    voice = f"quá trình đo đã hoàn tất mời bạn ngồi đợi đến lượt khám, rô bốt xin cảm ơn"
    robotSpeak(voice)

def ask_questions():
    while True:
        # Lắng nghe phản hồi từ người dùng
        user_input = robotListen()

        # Xử lý phản hồi của người dùng
        if "khoa thần kinh" in user_input:
            response = "Khoa thần kinh nằm ở lối đi bên phải dãy 1"
            robotSpeak(response)
        elif "khoa nội" in user_input:
            response = "Khoa nội nằm ở lối đi bên phải dãy 2"
            robotSpeak(response)
        elif "khoa ngoại" in user_input:
            response = "Khoa ngoại nằm ở lối đi bên trái dãy 1"
            robotSpeak(response)
        elif "hôm nay" in user_input or "mấy giờ":
            datetime_VN = datetime.now(tz_VN)
            response = datetime_VN.strftime("%m/%d/%Y, %H:%M:%S")
            robotSpeak(response)
        elif user_input == "":
            response = "Tôi không nghe rõ, bạn có thể nói lại không?"
            robotSpeak(response)
        else:
            response = "Xin lỗi, tôi không hiểu yêu cầu của bạn."
            robotSpeak(response)

        # Nếu người dùng muốn thoát khỏi vòng lặp, thêm điều kiện dừng
        if "thoát" in user_input:
            robotSpeak("Xin chào và hẹn gặp lại!")
            break

def main(user_folder, flagFace, STT):
    file_path = f"img/{user_folder}/data/{user_folder}.txt"

    if flagFace == 1:
        # Chào người dùng
        greet_user(file_path, STT)
        # Sau đó tiếp tục vòng lặp hỏi đáp
        ask_questions()
    else:
        print("Không nhận diện được khuôn mặt.")
        robotSpeak("Không nhận diện được khuôn mặt.")

if __name__ == "__main__":
    main(unidecode(user_name), 1, 1)
