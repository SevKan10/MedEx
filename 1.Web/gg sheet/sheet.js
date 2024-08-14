const scriptURL = 'https://script.google.com/macros/s/AKfycbyw7eqm34HkhYq4AqHIL2nXxfu9WJJ_nF7aVSDw_QENK5GrPeDzjkmtuigBZo7f4YRk/exec';
const form = document.forms['contact-form'];

form.addEventListener('submit', e => {
    e.preventDefault();
    const formData = new FormData(form);

    fetch(scriptURL, { method: 'POST', body: formData })
        .then(response => {
            if (response.ok) {
                alert("Cảm ơn! Đơn đăng ký của bạn đã được gửi thành công.");
                window.location.reload();
            } else {
                alert("Có lỗi xảy ra. Vui lòng thử lại.");
            }
        })
        .catch(error => console.error('Lỗi!', error.message));
});
