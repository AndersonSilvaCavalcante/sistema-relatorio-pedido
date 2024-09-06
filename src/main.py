
from datetime import datetime
from database.mongo import ConnectMongo
from src.utils import formatDateAndHour


def bootApplication():
    try:
        print(f"Started in {formatDateAndHour(datetime.now())}")
        mongo_conn = ConnectMongo("prodDB")

    except Exception as error:
        print(f"[main] ERROR: {error}")
    finally:
        print(f"Finished in {formatDateAndHour(datetime.now())}")


if __name__ == "__main__":
    bootApplication()
