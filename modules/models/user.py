"""User Model
"""
import time
from pymongo import MongoClient


class User:
    """User Model"""

    def __init__(self, mongo_conf):
        client = MongoClient(
            host=mongo_conf['DB_HOST'],
            port=mongo_conf['DB_PORT'])
        self.usersDB = client[mongo_conf['DB_NAME']]['users']

    def create(self, name: str):
        """Create New User"""
        exist = self.usersDB.find_one({'name': name})
        if exist:
            return None

        data = {
            'name': name,
            'join_time': time.time()
        }
        return self.usersDB.insert_one(data)

    def get_user(self, user_id: int):
        """Get User ID By Name"""
        return self.usersDB.find_one({'user_id': user_id})
