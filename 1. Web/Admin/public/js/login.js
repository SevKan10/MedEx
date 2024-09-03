import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import { getDatabase, ref, get } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-database.js";
/*===========================================================================================================================*/

/*Cấu hình Firebase*/
const firebaseConfig = 
{
    apiKey: "AIzaSyD_1V-oo7_fAXN2Iu1O-M_-X3qLaGLXUHo",
    authDomain: "doctors-e0601.firebaseapp.com",
    databaseURL: "https://doctors-e0601-default-rtdb.asia-southeast1.firebasedatabase.app/",
    projectId: "doctors-e0601",
    storageBucket: "doctors-e0601.appspot.com",
    messagingSenderId: "958721343640",
    appId: "1:958721343640:web:81a06f157afc58fe84d0ed"
};
/*===========================================================================================================================*/

/*Khởi tạo Firebase*/ 
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const database = getDatabase(app);
/*===========================================================================================================================*/

/*Xử lý sự kiện submit của form đăng nhập*/
document.getElementById('login-form').addEventListener('submit', async function(event) 
{
    event.preventDefault();
    // Lấy email và mật khẩu từ form
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        // Đăng nhập bằng email và mật khẩu
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Lấy tên bác sĩ từ Realtime Database
        const userRef = ref(database, 'doctors/' + user.email.replace('.', ','));
        const snapshot = await get(userRef);

        if (snapshot.exists()) 
        {
            const doctorName = snapshot.val();
            localStorage.setItem('userEmail', email);
            // Lưu trạng thái đăng nhập vào cookie
            document.cookie = 'adminAuth=true; path=/';
            // Hiển thị tên bác sĩ và chuyển hướng đến trang admin
            alert(`Đăng nhập thành công! Chào bác sĩ ${doctorName}`);
            window.location.href = 'admin.html';
        } 
        else {alert('Không tìm thấy thông tin người dùng.');}
    } 
    catch (error) 
    {
        // Hiển thị lỗi nếu đăng nhập thất bại
        let errorMessage;
        switch (error.code) 
        {
            case 'auth/invalid-email':
                errorMessage = 'Email không hợp lệ.';
                break;
            case 'auth/user-disabled':
                errorMessage = 'Tài khoản đã bị vô hiệu hóa.';
                break;
            case 'auth/user-not-found':
                errorMessage = 'Không tìm thấy tài khoản với email này.';
                break;
            case 'auth/wrong-password':
                errorMessage = 'Mật khẩu không chính xác.';
                break;
            default:
                errorMessage = 'Đăng nhập không thành công. Vui lòng thử lại.';
        }
        alert(`Lỗi: ${errorMessage}`);
    }
});
