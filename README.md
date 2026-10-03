💳 Payben — Digital Wallet & Recharge System

🔗 github.com/Plaksha24/payben

About

A full-stack digital wallet app where users register, log in, recharge their wallet through a real payment gateway (Razorpay), and track transaction history — built to demonstrate secure, end-to-end transactional system design.

Features
Secure signup/login — hashed passwords (bcrypt) + JWT sessions
Live wallet balance, backed by MySQL
Real payment gateway integration (Razorpay) with server-side signature verification — payments can't be faked from the frontend
Transaction history log
Tech Stack

Frontend: HTML, CSS, Bootstrap 5, JavaScript Backend: Python (FastAPI) Database: MySQL (SQLAlchemy ORM) Auth: JWT + bcrypt Payments: Razorpay API

How It Works
User registers → account + wallet (₹0 balance) created in MySQL
User logs in → receives a signed JWT token
Dashboard fetches live wallet balance from the backend
User initiates a recharge → backend creates a Razorpay order
Razorpay checkout opens → user completes payment
Backend independently verifies the payment signature (server-side, never trusts the client)
On success, wallet balance updates and the transaction is logged
Screenshots
Login	Dashboard & Transactions	Razorpay Checkout
Show Image	Show Image	Show Image
Setup
bash
git clone https://github.com/Plaksha24/payben.git
cd payben
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pymysql python-jose bcrypt razorpay python-multipart python-dotenv
# add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET to a .env file
uvicorn main:app --reload

Open index.html with Live Server. Backend runs at localhost:8000, docs at localhost:8000/docs.

Future Improvements
Atomic balance updates to prevent race conditions on concurrent recharges
Email verification on signup
Live deployment (Render/Vercel)

Built for academic/portfolio purposes. Uses Razorpay's test mode — no real payments processed.