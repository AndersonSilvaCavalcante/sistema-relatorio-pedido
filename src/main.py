from datetime import datetime
from database.mongo import ConnectMongo
from database.mysql import ConnectMySQL
from model.order_report import Base
from src.utils import formatDateAndHour


def bootApplication():
    try:
        print(f"Started in {formatDateAndHour(datetime.now())}")
        mongo_conn = ConnectMongo("prodDB")

        mysql_conn = ConnectMySQL(
            user='root', password='admin321', host='localhost', dbname='order_analysis')

        # Creating order report table
        Base.metadata.create_all(mysql_conn._engine)

    except Exception as error:
        print(f"[main] ERROR: {error}")
    finally:
        print(f"Finished in {formatDateAndHour(datetime.now())}")


if __name__ == "__main__":
    bootApplication()
