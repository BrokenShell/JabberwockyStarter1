from flask import Flask, render_template, request
from pandas import DataFrame

from app.mongo import MongoDB
from app.monsters import Monster

APP = Flask(__name__)
APP.db = MongoDB()


@APP.route("/")
def home():
    return render_template("index.html")


@APP.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        raw_count = request.values.get("count") or "1"
        if raw_count == "0":
            APP.db.delete({})
            count = 0
            monsters = []
        else:
            min_int = min(int(raw_count), 1024)
            max_int = max(1, min_int)
            count = max_int
            monsters = [vars(Monster()) for _ in range(count)]
            APP.db.create_many(monsters)
        return render_template(
            "create.html",
            count=count,
            monsters=monsters,
        )
    return render_template("create.html")


@APP.route("/data")
def data():
    df = DataFrame(APP.db.read({}))
    table = df.to_html()
    count = df.shape[0]
    return render_template(
        "data.html",
        table=table,
        count=count,
    )


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
