/* Xử lý tác vụ nút check box, cccd và registerFunc */
document.addEventListener('DOMContentLoaded', function() {
    const isChildCheckbox = document.getElementById('isChild');
    const cccdInput = document.getElementById('cccd');
    const registrationForm = document.getElementById('registrationForm');

    isChildCheckbox.addEventListener('change', function() {
        cccdInput.disabled = isChildCheckbox.checked;
        if (isChildCheckbox.checked) {
            cccdInput.value = ''; // Xóa giá trị trường CCCD
        }
    });

    registrationForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Ngăn hành động submit mặc định
        registerFunc(); // Gọi hàm registerFunc
    });
});
/*===========================================================================================================================*/

/*Đăng ký*/
async function registerFunc() 
{
    // Khởi tạo biến
    const fullName = document.getElementById("fullName").value;
    let CCCD = document.getElementById("cccd").value;
    const addressCustomer = document.getElementById("address").value;
    const phoneNumber = document.getElementById("phone").value;
    const emailCustomer = document.getElementById("email").value;
    const dob = document.getElementById("dob").value;
    const gender = document.querySelector('input[name="Giới tính"]:checked').value;
    const symptomsCustomer = document.getElementById("symptoms").value;
    const examDate = document.getElementById("ed").value;
    const photoFile = document.getElementById("photo").files[0]; // Lấy tệp đầu tiên (trong trường hợp chỉ chọn một tệp)

    if (CCCD === "") {CCCD = "Là trẻ em (không có)";}

    /*console.log("Full Name:   ", fullName);
    console.log("CCCD:         ", CCCD);
    console.log("Address:      ", addressCustomer);
    console.log("Phone Number: ", phoneNumber);
    console.log("Email:        ", emailCustomer);
    console.log("Date of Birth:", dob);
    console.log("Gender:       ", gender);
    console.log("Symptoms:     ", symptomsCustomer);
    console.log("Exam Date:    ", examDate);*/

    // Kiểm tra nếu có tệp hình ảnh được chọn
    if (!photoFile) {alert("Vui lòng thêm ảnh!"); return;}

    // Đọc hình ảnh và tải lên Firebase
    const imageDataUrl = await readFile(photoFile);
    await saveToFireBase(fullName, CCCD, addressCustomer, phoneNumber, emailCustomer, dob, gender, symptomsCustomer, examDate, photoFile);
    sendToSheet(fullName, CCCD, addressCustomer, phoneNumber, emailCustomer, dob, gender, symptomsCustomer, examDate, imageDataUrl);
    sendEmail(emailCustomer, fullName, phoneNumber, CCCD, addressCustomer, symptomsCustomer, examDate);
}
/*===========================================================================================================================*/
function readFile(photoFile) 
{
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);
        reader.readAsDataURL(photoFile);
    });
}
/*===========================================================================================================================*/

/*Gửi Mail*/
function sendEmail(emailCustomer, fullName, phoneNumber, CCCD, addressCustomer, symptomsCustomer, examDate)
{
    var params = 
    {
        email: emailCustomer,
        from_name: "MedEX-Wellness Sentinels",
        message: "Chúng tôi xin thông báo, quý khách đã đăng ký khám bệnh thành công!",
        name_customer: fullName,
        phone_number: phoneNumber,
        cccd_number: CCCD,
        address: addressCustomer,
        symptoms: symptomsCustomer,
        exam_date: examDate,
    }
    emailjs.send("service_0295kaf", "template_0i5z4i9", params)
        .then(() => alert("Đăng ký thành công, vui lòng kiểm tra email"))
        .catch((error) => console.error('Error sending email:', error));
}
/*===========================================================================================================================*/

/*Gửi GG Sheet*/
function sendToSheet(fullName, CCCD, addressCustomer, phoneNumber, emailCustomer, dob, gender, symptomsCustomer, examDate) 
{
    const scriptURL = 'https://script.google.com/macros/s/AKfycbwOkDp1w8_0br3avmqVL8Qb-tz8eTjHMW4Rp_wBK1uwkZ9-JowGQ4cSoWnSEag3ynsu/exec';
    
    const formData = new FormData();
    formData.append('Họ và Tên',        fullName);
    formData.append('Số CCCD',          CCCD);
    formData.append('Địa chỉ',          addressCustomer);
    formData.append('Điện thoại',       phoneNumber);
    formData.append('Email',            emailCustomer);
    formData.append('Ngày sinh',        dob);
    formData.append('Giới tính',        gender);
    formData.append('Triệu chứng bệnh', symptomsCustomer);
    formData.append('Ngày Khám',        examDate);

    fetch(scriptURL, { method: 'POST', body: formData })
        .then(response =>{if (response.ok) {console.log("Send success");}
        else {console.log("Send fail");}})
        .catch(error => console.error('error!', error.message));
}
/*===========================================================================================================================*/

/*Kết nối cơ sở dữ liệu Firebase bằng SDK*/ 
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-database.js";
import { getStorage, ref as storageRef, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-storage.js";

const firebaseConfig = {
   apiKey: "AIzaSyC78Puf9SQHvcQeU79vLN0QRdZZ-kXnWsk",
   authDomain: "medex-7ff53.firebaseapp.com",
   databaseURL: "https://medex-7ff53-default-rtdb.asia-southeast1.firebasedatabase.app",
   projectId: "medex-7ff53",
   storageBucket: "medex-7ff53.appspot.com",
   messagingSenderId: "729617022717",
   appId: "1:729617022717:web:0742a442b5abcfd75d0894"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase();

async function saveToFireBase(fullName, CCCD, addressCustomer, phoneNumber, emailCustomer, dob, gender, symptomsCustomer, examDate, photoFile) {
    const storage = getStorage();
    const imageRef = storageRef(storage, 'images/' + fullName);

    try {
        const snapshot = await uploadBytes(imageRef, photoFile);
        console.log('Image uploaded successfully');
        const downloadURL = await getDownloadURL(snapshot.ref);
        await set(ref(db, 'user/' + fullName), {
            ID_CCCD: CCCD,
            Address: addressCustomer,
            Phone: phoneNumber,
            Email: emailCustomer,
            Birthday: dob,
            Gender: gender,
            Symptoms: symptomsCustomer,
            Exam_Date: examDate,
            ImageURL: downloadURL
        });
        console.log("Dữ liệu đã được lưu thành công!");
    } catch (error) {
        console.error("Lỗi tải lên hình ảnh hoặc lưu dữ liệu: ", error);
    }
}
/*===========================================================================================================================*/
