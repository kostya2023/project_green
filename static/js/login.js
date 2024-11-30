// Получаем CSRF-токен из метатега
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// Функция для отправки AJAX-запросов с CSRF-токеном
function sendRequest(url, method, data) {
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrfToken // Добавляем CSRF токен в заголовок
    };

    return fetch(url, {
        method: method,
        headers: headers,
        body: JSON.stringify(data)
    });
}

// Обработчик события отправки формы
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const username = document.getElementById('username').value; // Получаем имя пользователя
    const password = document.getElementById('password').value; // Получаем пароль

    // Хэшируем пароль с использованием CryptoJS
    const hashedPassword = CryptoJS.SHA512(password).toString();

    // Создаем объект для отправки
    const requestData = {
        type: "ident", // Начнем с типа "ident"
        username: username,
    };

    // Отправляем AJAX запрос для аутентификации
    sendRequest('/login/api', 'POST', requestData)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Обработка ответа от сервера
            if (data.error) {
                alert(`Ошибка: ${data.message}`);
            } else {
                alert(`Статус: ${data.status}, Пользователь: ${data.username || username}`); // Используем username, если data.username не определен
                // Отправляем новый запрос с type: "auth"
                const authRequestData = {
                    type: "auth", // Изменяем тип на "auth"
                    username: username,
                    passwd: hashedPassword // Используем тот же хэшированный пароль
                };
                return sendRequest('/login/api', 'POST', authRequestData);
            }
        })
        .then(response => {
            if (response) {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.error) {
                alert(`Ошибка: ${data.message}`);
            } else if (data) {
                alert(`Аутентификация успешна! Статус: password_valid, Пользователь: ${data.username || username}`); // Используем username, если data.username не определен
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке запроса.');
        });
});
