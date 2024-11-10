from gtts import gTTS
import os

text = "Xin chào đặng đình vũ, số thư tự của bạn là 2, bạn vui lòng đặt tay lên cảm biến để đo nhịp tim"
tts = gTTS(text=text, lang='vi')  # 'vi' là mã ngôn ngữ cho tiếng Việt
tts.save("xin chào(thầy Vũ).mp3")
# os.system("start output.mp3")  # Đối với Windows, sử dụng 'start', đối với macOS và Linux, sử dụng 'open'
