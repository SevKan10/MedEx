document.addEventListener('DOMContentLoaded', function () {
    const isChildCheckbox = document.getElementById('isChild');
    const cccdInput = document.getElementById('cccd');

    isChildCheckbox.addEventListener('change', function () {
        if (isChildCheckbox.checked) {
            cccdInput.value = ''; // Xóa giá trị trường CCCD
            cccdInput.disabled = true; // Vô hiệu hóa trường CCCD
        } else {
            cccdInput.disabled = false; // Kích hoạt lại trường CCCD khi checkbox không được chọn
        }
    });
});
