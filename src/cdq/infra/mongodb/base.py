from pymongo import MongoClient

from cdq.configuration import MongoUrl


class MongoSettings:
    url = MongoUrl()


def mongoclient():
    return MongoClient(MongoSettings.url)
