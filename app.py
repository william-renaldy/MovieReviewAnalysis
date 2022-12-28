from flask import Flask,render_template,redirect,request,url_for,jsonify
from predictor import Processor,Model
import getmovie


app = Flask(__name__)
processor = Processor()
model = Model()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict",methods = ["POST","GET"])
def predict():
    if request.method == "POST":

        movie = request.form["res"]

        review,movie_name,year = getmovie.GetMovie(movie)

        if isinstance(review,list):
            X = processor.pre_process(review)

            result = model.predict(X)

            result = sum(result)/len(result)



            print(result)
            if result > 0.7:
                message = f"The movie is Good"
            elif result > 0.4:
                message = f"The movie is Neutral"
            else:
                message = f"The movie is Bad" 

        else:
            message = review  


        return jsonify([message,movie_name,year])
    else:
        return redirect(url_for("home"))


@app.errorhandler(404)
def error(e):
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(port="0.0.0.0")
