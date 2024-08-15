//SDK
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

        // Khởi tạo Firebase
        firebase.initializeApp(firebaseConfig);

        // Hàm lưu giá trị vào Firebase
        function saveToFirebase() {
            var database = firebase.database();
            var name = document.getElementById("txtName").value;
            var accept = document.getElementById("chAcpt").checked;
            var temp = document.getElementById("txtTemp").value;
            var hum = document.getElementById("txtHum").value;
            var tray = document.getElementById("tray").value;

            // Đường dẫn trong Firebase Realtime Database để lưu giá trị
            var firebasePath = "/plants"; // Thay đổi đường dẫn tùy theo nhu cầu của bạn

            // Tạo đối tượng dữ liệu để lưu vào Firebase
            var dataToSave = {
                name: name,
                accept: accept,
                temp: temp,
                hum: hum,
                tray: tray
            };

            // Thực hiện lưu dữ liệu vào Firebase
            database.ref(firebasePath).push(dataToSave)
                .then(function () {
                    console.log("Dữ liệu đã được lưu vào Firebase.");
                    // Sau khi lưu xong, bạn có thể thực hiện các hành động khác, chẳng hạn như chuyển hướng người dùng.
                })
                .catch(function (error) {
                    console.error("Lỗi khi lưu dữ liệu vào Firebase: " + error);
                });
        }