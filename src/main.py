
from datetime import datetime
from database.mongo import ConnectMongo

def bootApplication():
    try:
        print(f"Started in {datetime.now()}")
        mongo_conn = ConnectMongo("prodDB")

    except Exception as error:
        print(f"[main] ERROR: {error}")
    finally:
        print(f"Finished in {datetime.now()}")


if __name__ == "__main__":
    bootApplication()
