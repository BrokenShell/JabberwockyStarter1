import os
from typing import Dict, List, Iterable

from pymongo import MongoClient
from dotenv import load_dotenv

from app.monsters import Monster


class MongoDB:
    load_dotenv()

    def database(self):
        return MongoClient(os.getenv("MONGO_URL"))["Jabberwocky"]

    def collection(self):
        return self.database()["Monsters"]

    def create(self, data: Dict):
        self.collection().insert_one(data)

    def create_many(self, iterable_data: Iterable[Dict]):
        self.collection().insert_many(iterable_data)

    def read(self, query: Dict) -> List[Dict]:
        return list(self.collection().find(query, {"_id": False}))

    def delete(self, query: Dict):
        self.collection().delete_many(query)

    def count(self, query: Dict) -> int:
        return self.collection().count_documents(query)

    def seed(self, count: int):
        self.create_many(vars(Monster()) for _ in range(count))


if __name__ == '__main__':
    db = MongoDB()
    print(db.count({}))
    print(db.count({"name": "Goblin"}))
