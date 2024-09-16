import pandas as pd
from services.utils import getOrderDates, getOrderPaymentDetailsAndOrderFee, getRelevantAddress


class OrderService:
    def __init__(self, conn):
        self.ordersCollection = conn.useCollection("orders")

    def fetchOrders(self, query):
        return self.ordersCollection.find(query).sort({"createdAt": 1})

    def processOrders(self, orders):
        processedOrders = []
        for order in orders:
            temp_order = {
                "order_id": str(order['_id']),
                "created_at": order['createdAt'],
                "status": order['status'],
                "number": order['number'],
                "type": order['orderType'],
                "detail": order['detail']
            }
            temp_order.update(getOrderDates(order))
            temp_order.update(getOrderPaymentDetailsAndOrderFee(order))
            temp_order.update(getRelevantAddress(order['address']))
            processedOrders.append(temp_order)
   
        df_orders = pd.DataFrame(processedOrders)

        return df_orders
