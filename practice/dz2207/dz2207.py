from flask import Flask, render_template_string, request, redirect, session
import requests
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# URL API для зберігання даних користувачів
PHP_API_URL = "https://justconsole.tech/python/api.php?table=users_new"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Реєстрація</title>
</head>
<body>
    <h1>список користувачів</h1>
    {% for user in users %}
        <p><strong>ім'я:</strong> {{ user.username }} | <strong>email:</strong> {{ user.email }} | <strong>пароль:</strong> {{ user.password }}</p>
    {% endfor %}

    <h2>форма для нових користувачів</h2>
    <form method="POST" action="/register">
        <input type="text" name="username" placeholder="ім'я користувача" required>
        <input type="email" name="email" placeholder="email" required>
        <input type="password" name="password" placeholder="пароль" required>
        <button type="submit">створити користувача</button>
    </form>

    <h2>форма для входу</h2>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="ім'я користувача" required>
        <input type="password" name="password" placeholder="пароль" required>
        <button type="submit">увійти</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    try:
        response = requests.get(PHP_API_URL)
        users = response.json()
        return render_template_string(HTML_TEMPLATE, users=users)
    except requests.exceptions.RequestException as e:
        return f"<p>халепа з апі: {str(e)}</p>"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Зберігаємо пароль у відкритому вигляді (небезпечна практика!)
    data = {
        "username": username,
        "email": email,
        "password": password
    }

    try:
        response = requests.post(PHP_API_URL, json=data)
        if response.status_code == 200:
            return redirect('/')
        else:
            return f"<p>халепа: {response.text}</p>"
    except requests.exceptions.RequestException as e:
        return f"<p>халепа з апі: {str(e)}</p>"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        response = requests.get(PHP_API_URL)
        users = response.json()

        user = next((user for user in users if user['username'] == username), None)

        if user:
            print(f"Знайдений користувач: {user['username']}, Пароль: {user['password']}")  # Діагностика

            # Перевірка пароля без хешування (оскільки збережено у відкритому вигляді)
            if password == user['password']:
                session['user'] = user['username']
                return f"<h1>Ласкаво просимо, {user['username']}!</h1>"
            else:
                return "<p>Невірний пароль!</p>"
        else:
            return "<p>Невірний логін!</p>"
    except requests.exceptions.RequestException as e:
        return f"<p>Помилка при перевірці: {str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5002)
