document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Lấy dữ liệu từ form
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const symptoms = document.getElementById('symptoms').value;
    const photo = document.getElementById('photo').files[0];

    // Tạo FormData để gửi dữ liệu
    const formData = new FormData();
    formData.append('name', name);
    formData.append('address', address);
    formData.append('symptoms', symptoms);
    formData.append('photo', photo);

    // Gửi dữ liệu đến server (thêm URL đúng cho server của bạn)
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('Đăng ký thành công!');
        // Xử lý dữ liệu phản hồi từ server nếu cần thiết
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
