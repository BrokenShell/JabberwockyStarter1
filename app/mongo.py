import os
from typing import Dict, List, Iterable, Optional

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
        self.collection().insert_one(dict(data))

    def create_many(self, iterable_data: Iterable[Dict]):
        self.collection().insert_many(map(dict, iterable_data))

    def read(self, query: Optional[Dict] = None) -> List[Dict]:
        return list(self.collection().find(query, {"_id": False}))

    def delete(self, query: Dict):
        self.collection().delete_many(query)

    def count(self, query: Optional[Dict] = None) -> int:
        return self.collection().count_documents(query or {})

    def seed(self, count: int) -> List[Dict]:
        monsters = [vars(Monster()) for _ in range(count)]
        self.create_many(monsters)
        return monsters
