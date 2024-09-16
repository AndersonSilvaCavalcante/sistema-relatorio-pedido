from datetime import datetime, time

from bson import ObjectId
from sqlalchemy import desc
from database.mongo import ConnectMongo
from database.mysql import ConnectMySQL
from model.order_report import ModelBase, OrderReport
from services.order_service import OrderService
from utils import formatDateAndHour
from dotenv import load_dotenv
import os


def bootApplication():
    load_dotenv()

    try:
        print(f"Started in {formatDateAndHour(datetime.now())}")
        mongo_conn = ConnectMongo(
            os.getenv('URI_MONGO'), os.getenv('MONGO_DB_NAME'))
        orderService = OrderService(mongo_conn)

        mysql_conn = ConnectMySQL(
            user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'), host=os.getenv('MYSQL_HOST'), dbname=os.getenv('MYSQL_DATABASE'))

        # Creating order report table
        ModelBase.metadata.create_all(mysql_conn._engine)

        # Mongo query
        query = {}

        # Retrieving the date of the last order registered in mysql
        last_register = mysql_conn._session.query(OrderReport).order_by(
            desc(OrderReport.created_at)).first()

        if (last_register):
            if (last_register.created_at):
                query = {"createdAt": {
                    "$gte": datetime.combine(last_register.created_at.date(), time.min)}}

        # Retrieving registered order ids
        order_ids = mysql_conn._session.query(OrderReport.order_id).all()

        query["_id"] = {"$nin":  [ObjectId(id_str[0]) for id_str in order_ids]}

        # Fetching order in Mongo DB By Query
        print("Fetching orders...")
        fetchedOrdersByQuery = orderService.fetchOrders(query)

        # Creating order report dataframe
        print("Creating DataFrame and Inserting...")
        df_orders = orderService.processOrders(fetchedOrdersByQuery)
        df_orders.to_sql(OrderReport.__tablename__, con=mysql_conn._engine,
                         if_exists='append', index=False, method='multi')

    except Exception as error:
        print(f"[main] ERROR: {error}")
    finally:
        mongo_conn.closeConnection()
        print(f"Finished in {formatDateAndHour(datetime.now())}")


if __name__ == "__main__":
    bootApplication()
