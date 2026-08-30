from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Enum, TIMESTAMP, func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    balance = Column(DECIMAL(10,2), default=0)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    razorpay_order_id = Column(String(100))
    razorpay_payment_id = Column(String(100))
    amount = Column(DECIMAL(10,2))
    status = Column(Enum("pending","success","failed"), default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())