"""Challenge Model
"""
import time
from pymongo import MongoClient


class Challenge:
    """Challenge Model"""
    def __init__(self, mongo_conf: dict):
        client = MongoClient(
            host=mongo_conf['DB_HOST'],
            port=mongo_conf['DB_PORT'])
        self.challengesDB = client[mongo_conf['DB_NAME']]['challenges']

    def create(self, name: str):
        """Create"""
        exist = self.challengesDB.find_one({'name': name})
        if exist:
            return None

        data = {
            'name': name,
            'start_time': time.time()
        }
        return self.challengesDB.insert_one(data)

    def get_challenge(self, name: str):
        """Get Challenge By Name"""
        return self.challengesDB.find_one({'name': name})

    def get_challenges(self):
        """Get Challenges"""
        return self.challengesDB.find()
