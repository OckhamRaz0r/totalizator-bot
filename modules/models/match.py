"""Match Model
"""
import time
from pymongo import MongoClient


class Match:
    """Match Model"""
    def __init__(self, mongo_conf: dict):
        client = MongoClient(
            host=mongo_conf['DB_HOST'],
            port=mongo_conf['DB_PORT'])
        self.matchesDB = client[mongo_conf['DB_NAME']]['matches']

    def create(self, challenge: str, match: str):
        """Create"""
        exist = self.matchesDB.find_one(
            {'challenge': challenge, 'match': match})
        if exist:
            return None

        data = {
            'challenge': challenge,
            'match': match,
            'start_time': time.time()
        }
        return self.matchesDB.insert_one(data)

    def get_match(self, challenge: str, match: str):
        """Get Match By Name"""
        return self.matchesDB.find_one(
            {'challenge': challenge, 'match': match})

    def get_matches(self, challenge: str):
        """Get Matches"""
        return self.matchesDB.find_one({'challenge': challenge})
