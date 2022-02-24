from random import randint

from flask import Flask, render_template, request
from pandas import DataFrame

from app.graphs import visualizer
from app.model import ModelRFC
from app.mongo import MongoDB


APP = Flask(__name__)
APP.db = MongoDB()
APP.model = ModelRFC()


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
            monsters = APP.db.seed(count)
        return render_template(
            "create.html",
            count=count,
            monsters=monsters,
        )
    else:
        return render_template("create.html")


@APP.route("/data")
def data():
    df = DataFrame(APP.db.read({}))
    df.columns = map(lambda s: s.title(), df.columns)
    table = df.to_html()
    count = df.shape[0]
    return render_template(
        "data.html",
        table=table,
        count=count,
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    df = DataFrame(APP.db.read())
    default_filter = "All Monsters"
    name = request.values.get("name", default_filter)
    count = df.shape[0]
    if count > 0:
        filters_options = sorted(df["name"].unique())
        filters_options.insert(0, default_filter)
        graph = visualizer(df, name)
        return render_template(
            "view.html",
            name=name,
            count=count,
            name_filters=filters_options,
            graph=graph,
        )
    else:
        return render_template(
            "view.html",
            name=name,
            count=count,
        )


@APP.route("/train")
def train():
    name = APP.model.name
    time_stamp = APP.model.time_stamp
    score = APP.model.score()
    total = APP.model.total_rows
    count = APP.db.count()
    available = count - total
    return render_template(
        "train.html",
        name=name,
        time_stamp=time_stamp,
        score=score,
        total=total,
        available=available,
        count=count,
    )


@APP.route("/retrain", methods=["GET", "POST"])
def retrain():
    APP.model = ModelRFC()
    return train()


@APP.route("/predict", methods=["GET", "POST"])
def predict():
    count = APP.db.count()
    basis = {
        "level": int(request.values.get("level", randint(1, 100))),
        "health": int(request.values.get("health", randint(1, 100))),
        "offence": int(request.values.get("offence", randint(1, 100))),
        "defense": int(request.values.get("defense", randint(1, 100))),
        "balance": int(request.values.get("balance", randint(1, 100))),
    }
    if count > 32:
        prediction, confidence = APP.model(DataFrame([basis]))
        confidence = f"{100 * confidence:.0f}%"
    else:
        prediction, confidence = "", ""
    return render_template(
        "predict.html",
        count=count,
        level=basis["level"],
        health=basis["health"],
        offence=basis["offence"],
        defense=basis["defense"],
        balance=basis["balance"],
        prediction=prediction,
        confidence=confidence,
    )


if __name__ == '__main__':
    APP.run(debug=True)
