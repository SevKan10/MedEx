/* Xử lý tác vụ nút check box và cccd */
document.addEventListener('DOMContentLoaded', function () 
{
    const isChildCheckbox = document.getElementById('isChild');
    const cccdInput = document.getElementById('cccd');

    isChildCheckbox.addEventListener('change', function () 
    {
        if (isChildCheckbox.checked) 
        {
            cccdInput.value = ''; // Xóa giá trị trường CCCD
            cccdInput.disabled = true; // Vô hiệu hóa trường CCCD
        } else {cccdInput.disabled = false; /* Kích hoạt lại trường CCCD khi checkbox không được chọn*/}
    });
});
/*===========================================================================================================================*/

/*Load hàm gọi registerFunc*/
document.addEventListener('DOMContentLoaded', function() 
{
    document.getElementById('registrationForm').addEventListener('submit', function(event) 
    {
        event.preventDefault(); // Ngăn hành động submit mặc định
        registerFunc(); // Gọi hàm registerFunc
    });
});
/*===========================================================================================================================*/

/*Kết nối cơ sở dữ liệu Firebase bằng SDK*/ 
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import "https://www.gstatic.com/firebasejs/10.12.5/firebase-database.js";
// import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-storage.js";

/*Config của FB*/
const firebaseConfig = 
{
    apiKey: "AIzaSyC78Puf9SQHvcQeU79vLN0QRdZZ-kXnWsk",
    authDomain: "medex-7ff53.firebaseapp.com",
    projectId: "medex-7ff53",
    storageBucket: "medex-7ff53.appspot.com",
    messagingSenderId: "729617022717",
    appId: "1:729617022717:web:0742a442b5abcfd75d0894"
}

/*Khởi tạo FB*/
const app = initializeApp(firebaseConfig);
// const storage = getStorage(app);
/*===========================================================================================================================*/

/*Đăng ký*/
function registerFunc() {
    // Khởi tạo biến
    var fullName = document.getElementById("fullName").value;
    const CCCD = document.getElementById("cccd").value;
    var addressCustomer = document.getElementById("address").value;
    const phoneNumber = document.getElementById("phone").value;
    var emailCustomer = document.getElementById("email").value;
    var dob = document.getElementById("dob").value;
    var gender = document.querySelector('input[name="Giới tính"]:checked').value;
    var symptomsCustomer = document.getElementById("symptoms").value;
    var examDate = document.getElementById("ed").value;
    var photoInput = document.getElementById("photo");
    var photoFile = photoInput.files[0]; // Lấy tệp đầu tiên (trong trường hợp chỉ chọn một tệp)

    if (CCCD === "") {
        CCCD = "Là trẻ em (không có)";
    }

    console.log("Full Name:   ", fullName);
    console.log("CCCD:         ", CCCD);
    console.log("Address:      ", addressCustomer);
    console.log("Phone Number: ", phoneNumber);
    console.log("Email:        ", emailCustomer);
    console.log("Date of Birth:", dob);
    console.log("Gender:       ", gender);
    console.log("Symptoms:     ", symptomsCustomer);
    console.log("Exam Date:    ", examDate);

    // Kiểm tra nếu có tệp hình ảnh được chọn
    if (photoFile) 
    {
        console.log("File Name:", photoFile.name);
        console.log("File Size:", photoFile.size);
        console.log("File Type:", photoFile.type);

        var reader = new FileReader();
        reader.onload = function(e) 
        {
            var imageDataUrl = e.target.result;
            console.log("Image Data URL:", imageDataUrl); // URL của hình ảnh đã được mã hóa Base64
            sendToSheet(fullName, CCCD, addressCustomer, phoneNumber, emailCustomer, dob, gender, symptomsCustomer, examDate, imageDataUrl);
            sendEmail(emailCustomer, fullName, phoneNumber, CCCD, addressCustomer, symptomsCustomer, examDate);
        };
        reader.readAsDataURL(photoFile);
    } 
    else {console.log("No photo selected");alert("Vui lòng thêm ảnh!");}
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
    emailjs.send("service_0295kaf", "template_0i5z4i9", params).then(function(response) {alert("Đăng ký thành công, vui lòng kiểm tra email");},
    function(error) {console.error('Error sending email:', error);});;
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
        .then(response => 
        {
            if (response.ok) {console.log("Send success");}
            else {console.log("Send fail");}
        })
        .catch(error => console.error('error!', error.message));
}
/*===========================================================================================================================*/
