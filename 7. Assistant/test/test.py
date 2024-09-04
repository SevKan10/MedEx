from gtts import gTTS
import os

text = "Đã bật thiết bị 1"
tts = gTTS(text=text, lang='vi')  # 'vi' là mã ngôn ngữ cho tiếng Việt
tts.save("output.mp3")
os.system("start output.mp3")  # Đối với Windows, sử dụng 'start', đối với macOS và Linux, sử dụng 'open'
