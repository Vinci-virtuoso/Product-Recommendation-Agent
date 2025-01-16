import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    ProductId = Column(Integer, primary_key=True, index=True)
    Gender = Column(String, index=True)
    Category = Column(String, index=True)
    SubCategory = Column(String, index=True)
    ProductType = Column(String, index=True)
    Colour = Column(String, index=True)
    Usage = Column(String, index=True)
    ProductTitle = Column(String, index=True)
    Image = Column(String)
    ImageURL = Column(String)
    price = Column(Float)
    orders = relationship("OrderItem", back_populates="product")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.ProductId"))
    quantity = Column(Integer, default=1)
    price = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="orders")

DATABASE_URL = "sqlite:///example.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

def init_db():
    global db
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    users = [
        User(name="Vinci", age=25, email="alice@example.com"),
        User(name="Kuba", age=25, email="bob@example.com"),
        User(name="Wale", age=25, email="charlie@example.com"),
    ]
    session.add_all(users)
    session.commit()

    # Read products from CSV file
    products_df = pd.read_csv(r'C:\Users\username\file-directory-for-products.csv')
    products = [
        Product(
            ProductId=row['ProductId'],
            Gender=row['Gender'],
            Category=row['Category'],
            SubCategory=row['SubCategory'],
            ProductType=row['ProductType'],
            Colour=row['Colour'],
            Usage=row['Usage'],
            ProductTitle=row['ProductTitle'],
            Image=row['Image'],
            ImageURL=row['ImageURL'],
            price=row['price']
        )
        for index, row in products_df.iterrows()
    ]
    session.add_all(products)
    session.commit()
    session.close()
    print("The database has been successfully expanded and filled with sample data.")

if __name__ == "__main__":
    if not os.path.exists("example.db"):
        init_db()
    else:
        print("The database already exists.")
