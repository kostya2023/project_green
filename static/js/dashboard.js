// Функция для получения значения куки по имени
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Получаем значение куки "Username"
const username = getCookie('Username');

// Находим элемент с текстом LOGIN_USERNAME и обновляем его
const loginLink = document.querySelector('.header-item'); // Предполагаем, что это первая ссылка
if (username) {
    loginLink.textContent = username; // Меняем текст на значение куки
}

// Функция для отправки AJAX запроса
function sendAjaxRequest(infoType) {
    const requestData = {
        type: "info",
        info: infoType
    };

    fetch('/dashboard/api', {
        method: 'POST', // Используем метод POST
        headers: {
            'Content-Type': 'application/json' // Указываем тип контента
        },
        body: JSON.stringify(requestData) // Преобразуем объект в JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Преобразуем ответ в JSON
    })
    .then(data => {
        console.log(data); // Обработка полученных данных
        // Здесь можно обновить UI на основе ответа от сервера
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}