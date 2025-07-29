from os import access

from flask import Flask, render_template, request, session, render_template_string
import requests
fruits = ["Яблуко","Банан","Апельсин","Ківі","Виноград"]
api = "https://bored-api.appbrewery.com/random"
PHP_API_URL = "https://justconsole.tech/python/api.php?table=users"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uk">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Паролі користувачів</title>

</head>
<body>

<h1>Паролі користувачів</h1>
{% for user in users %}

<p><strong>ім'я користувача:</strong> {{ user.username }} | <strong>пароль:</strong> {{ user.password}}</p>
{% endfor %}

</body>
</html>
"""


conversion_factors = {
'cm': {'m': 0.01, 'km': 0.00001, 'inch': 0.393701, 'foot': 0.0328084},
'm': {'cm': 100, 'km': 0.001, 'inch': 39.3701, 'foot': 3.28084},
'km': {'cm': 100000, 'm': 1000, 'inch': 39370.1, 'foot': 3280.84},
'inch': {'cm': 2.54, 'm': 0.0254, 'km': 0.0000254, 'foot': 0.0833333},
'foot': {'cm': 30.48, 'm': 0.3048, 'km': 0.0003048, 'inch': 12}
}

mass_convertion={
    "kg":1,
    "g":0.001,
    "c":100,
    "t":1000,
    "pd":0.45359237,
    "sm":1.989*(10**30)
}

def conv_mass(value,from_unit,to_unit):
    global mass_convertion
    if from_unit==to_unit:
        return value
    return value * (mass_convertion.get(from_unit)/mass_convertion.get(to_unit))

def convert_units(value, from_unit, to_unit):
    global conversion_factors
    if from_unit == to_unit:
        return value
    return round(value * conversion_factors.get(from_unit, {}).get(to_unit, 1), 2)

app = Flask(__name__)
app.secret_key="secret_key"

@app.route("/")
def hello():
    name = "свят"
    age = 16
    hobby = "стрільба з лука"
    place = "антарктида"
    return render_template("index.html", name = name, age=age, hobby=hobby, place=place, fruits=fruits)

@app.route("/about")
def abt():
    return render_template("abt.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/form/greet", methods=["POST"])
def greet():
    name = request.form['name']
    age = int(request.form['age'])
    color = request.form['color']
    return render_template("greet.html", name = name, age=age, color = color)

@app.route("/character")
def char():
    return render_template("character.html")

@app.route("/klas", methods=["GET", "POST"])
def klas():
    age = None
    message = ""
    if request.method == "POST":
        age =int(request.form["age"])
        if age < 12:
            message = "👶👶 Ти ще дитина! Насолоджуйся!"
        elif 12 <= age < 18:
            message = "🧑‍🎓👩‍🎓 Ти підліток! Час вчитися та розвиватися."
        else:
            message = "👩‍💼🧑‍💼 Ти доросла людина! Відповідальність – твій друг!"
    return render_template("klas.html", message=message)

@app.route("/convert", methods=["GET", "POST"])
def convert():
    result=None
    if request.method == "POST":
        val=float(request.form["value"])
        from_v=request.form["from_unit"]
        to_v=request.form["to_unit"]
        result=convert_units(val, from_v, to_v)
    return render_template("/convert.html", result=result)

@app.route("/dzconverter", methods=["GET", "POST"])
def dzconv():
    result=None
    if request.method=="POST":
        val = float(request.form["value"])
        from_u = request.form["from_unit"]
        to_u = request.form["to_unit"]
        result=round(conv_mass(val,from_u,to_u), 3)
    return render_template("dzconverter.html", result=result)

@app.route("/secret")
def secret():
    return render_template("scripting.html")

@app.route("/clicker")
def clicker():
    if "clicks" not in session:
        session["clicks"] = 0
    return render_template_string("""
    <h1>Кількість кліків: {{ clicks }}</h1>
    <a href="/clicker/click">Натисни!</a><br>
    <a href="/clicker/minus">Мінус</a>
    """, clicks=session["clicks"])


@app.route("/clicker/click")
def click():
    session["clicks"] += 1
    return clicker()

@app.route("/clicker/minus")
def minusclick():
    session["clicks"] -= 1
    return clicker()

@app.route("/sessionclicker")
def sessionclicker():
    if "clicks" not in session:
        session["clicks"] = 0
    return render_template("sessionclicker.html", clicks=session["clicks"])

@app.route("/add")
def addclicker():
    session["clicks"] += 1
    return sessionclicker()

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    lastres = None
    if "lastres" not in session:
        session["lastres"]=None
    if request.method == "POST":
        inp = request.form["inp"]
        lastres = eval(inp)
        session["lastres"] = lastres
    return render_template("calculator.html", lastres = lastres)

@app.route("/req", methods=["GET", "POST"]  )
def req():
    response = requests.get(api)
    data = response.json()
    task = data['activity']
    return render_template("req.html", task=task)

@app.route("/hack", methods=["GET", "POST"])
def get_users():
    try:
        response = requests.get(PHP_API_URL)
        users = response.json() #Отримуємо список користувачів
        return render_template_string(HTML_TEMPLATE, users=users)
    except requests.exceptions.RequestException as e:
        return f"<p>Помилка при підключенні до сервера: {str(e)}</p>"

@app.route("/auth", methods=["GET", "POST"])
def auth():
    response = requests.get(PHP_API_URL)
    users = response.json()
    access= None
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        for user in users:
            if login in user.get("username"):
                if password == user.get("password"):
                    access = "approved"
                    return render_template("auth.html", access = access)
                else:
                    access = "deny"
            else:
                access="deny"
    return render_template("auth.html", access=access)

if __name__ == "__main__":
    app.run(debug=True)