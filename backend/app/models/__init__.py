from sqlalchemy import Column, String, Numeric, DateTime, Integer, Text, ForeignKey
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    customer_city = Column(String)
    customer_state = Column(String)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    product_category = Column(String)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    order_status = Column(String)
    order_purchase_timestamp = Column(DateTime)
    order_delivered_timestamp = Column(DateTime)


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(String, ForeignKey("orders.order_id"), primary_key=True)
    product_id = Column(String, ForeignKey("products.product_id"), primary_key=True)
    price = Column(Numeric(10, 2))
    freight_value = Column(Numeric(10, 2))


class Payment(Base):
    __tablename__ = "payments"

    order_id = Column(String, ForeignKey("orders.order_id"), primary_key=True)
    payment_type = Column(String, primary_key=True)
    payment_value = Column(Numeric(10, 2), primary_key=True)


class AnomalyLog(Base):
    __tablename__ = "anomalies_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    detected_at = Column(DateTime)
    metric = Column(String)
    deviation_pct = Column(Numeric(5, 2))
    message = Column(Text)
