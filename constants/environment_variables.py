import os


MONGO_DB = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_HOST")

assert MONGO_DB is not None, "Variable de entorno MONGO_DB no está definida"
assert MONGO_HOST is not None, "Variable de entorno MONGO_HOST no está definida"
