from datetime import datetime
from database.mongo import ConnectMongo
from database.mysql import ConnectMySQL
from model.order_report import Base
from utils import formatDateAndHour
from dotenv import load_dotenv
import os


def bootApplication():
    load_dotenv()

    try:
        print(f"Started in {formatDateAndHour(datetime.now())}")
        mongo_conn = ConnectMongo(os.getenv('URI_MONGO'), os.getenv('MONGO_DB_NAME'))

        mysql_conn = ConnectMySQL(
            user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASS'), host=os.getenv('MYSQL_HOST'), dbname=os.getenv('MYSQL_DB'))

        # Creating order report table
        Base.metadata.create_all(mysql_conn._engine)

    except Exception as error:
        print(f"[main] ERROR: {error}")
    finally:
        mongo_conn.closeConnection()
        print(f"Finished in {formatDateAndHour(datetime.now())}")


if __name__ == "__main__":
    bootApplication()
