from flask import Flask, render_template

APP = Flask(__name__)


@APP.route("/")
def home():
    return render_template("index.html")


@APP.route("/create")
def create():
    return render_template("create.html", disabled=True)


@APP.route("/data")
def data():
    return render_template("data.html", disabled=True)


@APP.route("/view")
def view():
    return render_template("view.html", disabled=True)


@APP.route("/train")
def train():
    return render_template("train.html", disabled=True)


@APP.route("/predict")
def predict():
    return render_template("predict.html", disabled=True)


if __name__ == '__main__':
    APP.run(debug=True)
