import pyrebase
config ={
  "apiKey": "AIzaSyDoWySbs3R0yKWsRTgRK54pLgudr8Srcfo",
  "authDomain": "medical-examiner-40e4d.firebaseapp.com",
  "databaseURL": "https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "medical-examiner-40e4d",
  "storageBucket": "medical-examiner-40e4d.appspot.com",
  "messagingSenderId": "592499333547",
  "appId": "1:592499333547:web:a830daa4140cf1ca515aee"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
localpath="" 
cloudpath="images/1724738748252.png"

try:
    storage.child(cloudpath).download(localpath,filename="1724738748252.png")
    print("Successfull")
except Exception as e: 
    print(f"An error occurred: {e}")