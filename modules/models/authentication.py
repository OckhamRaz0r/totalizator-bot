"""Authentication Model
"""
from pymongo import MongoClient


class Authentication:
    """Authentication Model"""

    def __init__(self, mongo_conf):
        client = MongoClient(
            host=mongo_conf['DB_HOST'],
            port=mongo_conf['DB_PORT'])
        self.authDB = client[mongo_conf['DB_NAME']]['users']

    def check(self, user_id: int):
        """Check Registration"""
        return self.authDB.find_one({'chat_id': user_id})
