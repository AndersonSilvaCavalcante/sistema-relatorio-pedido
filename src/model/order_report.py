import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

ModelBase = declarative_base()

class OrderReport(ModelBase):
    __tablename__ = os.getenv('REPORT_TABLE_NAME', 'order_report')

    id = Column(Integer, primary_key=True)
    order_id = Column(String(255), unique=True, nullable=False)
    # Order Dates
    created_at = Column(DateTime())
    preparation_start_datetime = Column(DateTime())
    prepared_datetime = Column(DateTime())
    assigned_datetime = Column(DateTime())
    collected_datetime = Column(DateTime())
    datetime_finished = Column(DateTime())
    # Order Address
    street = Column(String(255))
    neighborhood = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    # Payment details and order fee
    additional_fee = Column(Float)
    deliveryman_fee = Column(Float)
    delivery_fee = Column(Float)
    payment_type = Column(String(255))
    prepaid = Column(Boolean)
    discounts = Column(Float)
    subtotal = Column(Float)
    total = Column(Float)
    # Order detail
    status = Column(String(50))
    type = Column(String(50))
    number = Column(String(50))
    detail = Column(String(5000))
