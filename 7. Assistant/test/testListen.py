import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    print("Robot listening")
    recognizer.adjust_for_ambient_noise(source)
    audio_data = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio_data, language="vi")
except:
    text = ""

print(text.lower())