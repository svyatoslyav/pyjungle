from flask import Flask, render_template, request
fruits = ["Яблуко","Банан","Апельсин","Ківі","Виноград"]

conversion_factors = {
'cm': {'m': 0.01, 'km': 0.00001, 'inch': 0.393701, 'foot': 0.0328084},
'm': {'cm': 100, 'km': 0.001, 'inch': 39.3701, 'foot': 3.28084},
'km': {'cm': 100000, 'm': 1000, 'inch': 39370.1, 'foot': 3280.84},
'inch': {'cm': 2.54, 'm': 0.0254, 'km': 0.0000254, 'foot': 0.0833333},
'foot': {'cm': 30.48, 'm': 0.3048, 'km': 0.0003048, 'inch': 12}
}

def convert_units(value, from_unit, to_unit):
    global conversion_factors
    if from_unit == to_unit:
        return value
    return round(value * conversion_factors.get(from_unit, {}).get(to_unit, 1), 2)

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

@app.route("/convert", methods=["GET", "POST"])
def convert():
    result=None
    if request.method == "POST":
        val=float(request.form["value"])
        from_v=request.form["from_unit"]
        to_v=request.form["to_unit"]
        result=convert_units(val, from_v, to_v)
    return render_template("/convert.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)