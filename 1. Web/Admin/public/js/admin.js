import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import { getDatabase, ref, onValue, update, remove, get } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-database.js";
import { getStorage, ref as storageRef, deleteObject } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-storage.js";

/* Firebase Config */
const firebaseConfig = {
    apiKey: "AIzaSyDoWySbs3R0yKWsRTgRK54pLgudr8Srcfo",
    authDomain: "medical-examiner-40e4d.firebaseapp.com",
    databaseURL: "https://medical-examiner-40e4d-default-rtdb.asia-southeast1.firebasedatabase.app/",
    projectId: "medical-examiner-40e4d",
    storageBucket: "medical-examiner-40e4d.appspot.com",
    messagingSenderId: "592499333547",
    appId: "1:592499333547:web:a830daa4140cf1ca515aee"
};

const firebaseConfigDoctor = {
    apiKey: "AIzaSyD_1V-oo7_fAXN2Iu1O-M_-X3qLaGLXUHo",
    authDomain: "doctors-e0601.firebaseapp.com",
    databaseURL: "https://doctors-e0601-default-rtdb.asia-southeast1.firebasedatabase.app/",
    projectId: "doctors-e0601",
    storageBucket: "doctors-e0601.appspot.com",
    messagingSenderId: "958721343640",
    appId: "1:958721343640:web:81a06f157afc58fe84d0ed"
};

/* Firebase Initialization */
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const dbUser = getDatabase(app);
const storage = getStorage(app);

const appDoctor = initializeApp(firebaseConfigDoctor, "doctor");
const dbDoctor = getDatabase(appDoctor);

const email = localStorage.getItem('userEmail');

if (email) {
    displayDoctorName(email);
    handleConfirm(event, email);
} else {
    window.location.href = 'login.html';
}

/* Display Doctor Name */
function displayDoctorName(email) {
    const doctorRef = ref(dbDoctor, 'doctors/' + email.replace('.', ','));

    onValue(doctorRef, (snapshot) => {
        const doctorName = snapshot.val();
        const doctorNameElement = document.getElementById('doctorName');
        if (doctorName) {
            doctorNameElement.textContent = 'Bác sĩ: ' + doctorName;
        } else {
            doctorNameElement.textContent = 'Bác sĩ: Không xác định';
        }
    });
}

/* Fetch and Display Data */
function fetchAndDisplayData() {
    const dataRef = ref(dbUser, 'user/');

    onValue(dataRef, (snapshot) => {
        const data = snapshot.val();
        const dataContainer = document.getElementById('dataContainer');
        dataContainer.innerHTML = '';

        if (data) {
            const sortedData = Object.entries(data).sort(([keyA, valueA], [keyB, valueB]) => {
                const idCCCD_A = valueA.ID_CCCD || '';
                const idCCCD_B = valueB.ID_CCCD || '';
                const isChildA = idCCCD_A.toLowerCase().includes('trẻ em');
                const isChildB = idCCCD_B.toLowerCase().includes('trẻ em');

                if (isChildA && !isChildB) {
                    return -1;
                } else if (!isChildA && isChildB) {
                    return 1;
                } else {
                    return idCCCD_A.localeCompare(idCCCD_B);
                }
            });

            for (const [key, value] of sortedData) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${value.Name || 'N/A'}</td>
                    <td>${value.ID_CCCD || 'N/A'}</td>
                    <td>${value.Address || 'N/A'}</td>
                    <td>${value.Phone || 'N/A'}</td>
                    <td>${value.Email || 'N/A'}</td>
                    <td>${value.Birthday || 'N/A'}</td>
                    <td>${value.Gender || 'N/A'}</td>
                    <td>${value.Symptoms || 'N/A'}</td>
                    <td>${value.Heart || 'N/A'}</td>
                    <td>${value.Temp || 'N/A'}</td>
                    <td>${value.Exam_Date || 'N/A'}</td>
                    <td><img src="${value.ImageURL || 'https://via.placeholder.com/100'}" alt="Image" style="width: 100px;"></td>
                    <td>
                        <button class="confirm-button" data-id="${key}" ${value.Confirmed ? 'disabled' : ''}>
                            ${value.Confirmed ? 'Đã xác nhận' : 'Xác nhận'}
                        </button>
                        <span class="confirmation-name" id="confirmation-${key}">
                            ${value.Confirmed_By || ''}
                        </span>
                    </td>
                    <td>
                        <button class="delete-button" data-id="${key}">Xóa</button>
                    </td>
                `;

                dataContainer.appendChild(row);
            }

            document.querySelectorAll('.confirm-button').forEach(button => {
                button.addEventListener('click', handleConfirm);
            });

            document.querySelectorAll('.delete-button').forEach(button => {
                button.addEventListener('click', handleDelete);
            });
        }
    });
}

/* Handle Confirmation */
function handleConfirm(event = null, email = null) {
    if (!event) return;

    const button = event.target;
    const uniqueID = button.getAttribute('data-id');
    const confirmationNameSpan = document.getElementById(`confirmation-${uniqueID}`);
    email = email || localStorage.getItem('userEmail'); // Get email from localStorage if not provided

    if (!button.disabled) {
        button.disabled = true;
        button.textContent = 'Đã xác nhận';

        const doctorRef = ref(dbDoctor, 'doctors/' + email.replace('.', ','));

        onValue(doctorRef, (snapshot) => {
            const doctorName = snapshot.val() || 'Bác sĩ không xác định';
            confirmationNameSpan.textContent = doctorName;
            updateFirebaseEntry(uniqueID, doctorName);
        }, { onlyOnce: true });
    }
}

/* Update Firebase Entry */
async function updateFirebaseEntry(id, doctorName) {
    try {
        await update(ref(dbUser, 'user/' + id), {
            Confirmed: true,
            Confirmed_By: doctorName
        });

        console.log('Update Success');
    } catch (error) {
        console.error('Update failed', error);
    }
}

/* Handle Delete */
async function handleDelete(event) {
    // Fetch the data-id attribute from the delete button
    const button = event.target;
    const id = button.getAttribute('data-id');

    // Show confirmation dialog
    const confirmed = confirm('Bạn có chắc chắn muốn xóa mục này không?');

    if (confirmed) {
        try {
            // Fetch the data for the specific user
            const userRef = ref(dbUser, 'user/' + id);
            const snapshot = await get(userRef);  // Use 'get' to fetch user data
            const userData = snapshot.val();

            if (userData && userData.ImageURL) {
                // Create a reference to the file to delete
                const imageRef = storageRef(storage, userData.ImageURL);

                // Delete the file from Firebase Storage
                await deleteObject(imageRef);
                console.log('Hình ảnh đã được xóa thành công');
            }

            // Remove the data from Firebase Realtime Database
            await remove(userRef);
            console.log('Xóa dữ liệu thành công');
            alert('Dữ liệu đã được xóa thành công.');
            
            // Refresh data after deletion
            fetchAndDisplayData();
        } catch (error) {
            console.error('Lỗi khi xóa dữ liệu hoặc hình ảnh:', error);
            alert('Lỗi khi xóa dữ liệu hoặc hình ảnh. Vui lòng kiểm tra lại.');
        }
    } else {
        console.log('Xóa bị hủy');
    }
}

/* Delete Firebase Entry */
async function deleteFirebaseEntry(id) {
    const button = event.target;
    const uniqueID = button.getAttribute('data-id');

    if (confirm('Bạn có chắc chắn muốn xóa mục này không?')) {
        try {
            // Fetch the data for the specific user
            const userRef = ref(dbUser, 'user/' + uniqueID);
            const snapshot = await get(userRef);
            const userData = snapshot.val();

            if (userData && userData.ImageURL) {
                // Create a reference to the file to delete
                const imageRef = storageRef(storage, userData.ImageURL);

                // Delete the file from Firebase Storage
                await deleteObject(imageRef);
                console.log('Hình ảnh đã được xóa thành công');
            }

            // Remove the data from Firebase Realtime Database
            await remove(userRef);
            console.log('Xóa dữ liệu thành công');
            
            // Refresh data after deletion
            fetchAndDisplayData();
        } catch (error) {
            console.error('Lỗi khi xóa dữ liệu hoặc hình ảnh:', error);
        }
    }
}

/* Logout Function */
function logout() {
    signOut(auth).then(() => {
        localStorage.removeItem('userEmail');
        window.location.href = 'login.html';
    }).catch((error) => {
        console.error('Lỗi khi đăng xuất:', error);
    });
}

document.getElementById('logoutButton').addEventListener('click', logout);

window.onload = () => {
    fetchAndDisplayData();
};

window.onload = () => {
    fetchAndDisplayData();
};