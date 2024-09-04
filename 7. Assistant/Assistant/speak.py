import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")

# for voice in voices:
#     print("Voices:")
#     print(" - ID: %s" % voice.id)
#     print(" - Name: %s" % voice.name)
#     print(" - Languages: %s" % voice.languages)
#     print(" - Gender: %s" % voice.gender)
#     print(" - Age: %s" % voice.age)
id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"

engine.setProperty("voices",id)

robot = " Đã bật thiết bị 1"
engine.say(robot)

engine.runAndWait()

