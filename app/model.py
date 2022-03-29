from datetime import datetime
from typing import Tuple

import pytz
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from app.mongo import MongoDB


class ModelRFC:

    def __init__(self):
        self.db = MongoDB()
        df = DataFrame(self.db.read({})).drop(columns=["name"])
        target = df["rank"]
        features = df.drop(columns=["rank"])

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            features,
            target,
            test_size=0.10,
            random_state=42,
            stratify=target,
        )

        self.total_rows = df.shape[0]
        self.total_trained = self.y_train.shape[0]
        self.total_tested = self.y_test.shape[0]

        self.name = "Random Forest Classifier"
        timezone = pytz.timezone("US/Pacific")
        self.time_stamp = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

        self.model = RandomForestClassifier(
            n_jobs=-1,
            n_estimators=33,
            random_state=42,
        )
        self.model.fit(self.X_train, self.y_train)

    def __call__(self, feature_basis: DataFrame) -> Tuple:
        pred = self.model.predict(feature_basis)[0]
        prob = self.model.predict_proba(feature_basis)[0]
        return pred, max(prob)

    def score(self):
        return f"{100 * self.model.score(self.X_test, self.y_test):.0f}%"
