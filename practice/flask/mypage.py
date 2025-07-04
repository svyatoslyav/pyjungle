from flask import Flask, render_template, request
fruits = ["Яблуко","Банан","Апельсин","Ківі","Виноград"]
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)