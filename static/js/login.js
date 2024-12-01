document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем отправку формы по умолчанию

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const hashedPassword = CryptoJS.SHA512(password).toString(); // Хешируем пароль

    // Первый запрос для идентификации
    const identData = {
        type: "ident",
        username: username
    };

    fetch('/login/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(identData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Сетевая ошибка при идентификации');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'finded') {
            // Если пользователь найден, отправляем второй запрос для аутентификации
            const authData = {
                type: "auth",
                username: username,
                password: hashedPassword
            };

            return fetch('/login/api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(authData)
            });
        } else {
            alert("Пользователь не найден");
            throw new Error('Пользователь не найден');
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Сетевая ошибка при аутентификации');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'pass_valid') {
            alert("Успешный вход!");
            // Редирект на страницу панели управления
            window.location.href = '/dashboard'; // Перенаправляем пользователя на страницу панели управления
        } else if (data.status === 'pass_invalid') {
            alert("Неверный пароль");
        }
    })
    .catch(error => {
        console.error('Ошибка:', error.message);
    });
});
