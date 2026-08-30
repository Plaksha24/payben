from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import razorpay
import hmac
import hashlib
import os
from dotenv import load_dotenv

from database import get_db, engine, Base
import models, auth

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("rzp_test_TSkop11OlWxj0s")
RAZORPAY_KEY_SECRET = os.getenv("FJ7V1aq1Hb7CT1sOl8Zzgveo")

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


@app.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(400, "Email already registered")
    user = models.User(name=name, email=email, password_hash=auth.hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    wallet = models.Wallet(user_id=user.id, balance=0)
    db.add(wallet)
    db.commit()
    return {"msg": "registered", "user_id": user.id}


@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "user_id": user.id}


@app.get("/wallet/balance/{user_id}")
def balance(user_id: int, db: Session = Depends(get_db)):
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()
    return {"balance": wallet.balance}


@app.post("/wallet/create-order")
def create_order(amount: float, user_id: int):
    order = razorpay_client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })
    return order


@app.post("/wallet/verify-payment")
def verify_payment(
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
    user_id: int,
    amount: float,
    db: Session = Depends(get_db)
):
    generated_signature = hmac.new(
        RAZORPAY_KEY_SECRET.encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    if generated_signature != razorpay_signature:
        raise HTTPException(400, "Payment verification failed")

    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()
    wallet.balance = float(wallet.balance) + amount

    txn = models.Transaction(
        user_id=user_id,
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        amount=amount,
        status="success"
    )
    db.add(txn)
    db.commit()

    return {"msg": "payment verified", "new_balance": wallet.balance}


@app.get("/wallet/transactions/{user_id}")
def transactions(user_id: int, db: Session = Depends(get_db)):
    txns = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.created_at.desc()).all()
    return [
        {
            "id": t.id,
            "amount": float(t.amount),
            "status": t.status,
            "date": t.created_at.strftime("%d %b %Y, %I:%M %p") if t.created_at else None
        }
        for t in txns
    ]