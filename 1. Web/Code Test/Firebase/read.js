
const firebaseConfig = {
    apiKey: "AIzaSyDNVI6MfggzOLtCoP1uVAvajd9lKtS22LU",
    authDomain: "ifarme-df868.firebaseapp.com",
    databaseURL: "https://ifarme-df868-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "ifarme-df868",
    storageBucket: "ifarme-df868.appspot.com",
    messagingSenderId: "124564135650",
    appId: "1:124564135650:web:e969f361eb2d8611fb48bb",
    measurementId: "G-V3SCKCZMV9"
  }
  
  const app = firebase.initializeApp(firebaseConfig);
  
  const value = firebase.database();
  
  const dataValue1 = value.ref('tray1/name');

  dataValue1.on('value', (snapshot) => {
    const name1 = snapshot.val();
    if (name1 !== null) {
        // Hiển thị giá trị nhiệt độ
        const nameElement = document.getElementById("value-output1");
        nameElement.textContent = name1;
    } else {
        // Hiển thị thông báo nếu không có dữ liệu
        const nameElement = document.getElementById("value-output1");
        nameElement.textContent = "No name data available";
    }
  });