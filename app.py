from flask import Flask,render_template,redirect,request,url_for,jsonify
from predictor import Processor,Model


app = Flask(__name__)
processor = Processor()
model = Model()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict",methods = ["POST","GET"])
def predict():
    if request.method == "POST":

        review = request.form["res"]

        X = processor.pre_process([review])

        result = model.predict(X)

        if result[0] == 1:
            message = "Heyy!! It's a Positive Review"
        else:
            message = "Aww! It's a negative Review"


        return jsonify(message)
    else:
        return redirect(url_for("home"))


@app.errorhandler(404)
def error(e):
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)