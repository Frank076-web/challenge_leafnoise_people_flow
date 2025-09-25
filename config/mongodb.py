from mongoengine import connect

from constants.environment_variables import MONGO_DB, MONGO_HOST


def init_db():
    connect(db=MONGO_DB, host=MONGO_HOST)
