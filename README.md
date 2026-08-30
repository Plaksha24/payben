💳 Payben — Digital Wallet & Recharge System

A full-stack digital wallet application that lets users register, authenticate, top up their wallet through a real payment gateway (Razorpay), and track transaction history — built to demonstrate secure, end-to-end transactional system design.

🎯 Problem Statement

Prepaid recharge and wallet top-up flows in consumer apps (Paytm, PhonePe, etc.) are closed-source, monolithic systems. Payben implements a scaled-down but functionally complete version of the same core mechanism: secure user authentication + wallet balance management + real payment gateway integration with server-side verification.

✨ Features
🔐 User registration & login with hashed passwords (bcrypt)
🪪 JWT-based session authentication
💰 Digital wallet with live balance tracking
💳 Real payment gateway integration (Razorpay, test mode)
✅ Server-side payment signature verification (prevents fake/spoofed payments)
📜 Transaction history log
🎨 Responsive Bootstrap frontend
🛠️ Tech Stack
Layer	Technology
Frontend	HTML, CSS, Bootstrap 5, Vanilla JS
Backend	Python, FastAPI
Database	MySQL (via SQLAlchemy ORM)
Auth	JWT (python-jose), bcrypt
Payments	Razorpay API (test mode)
Server	Uvicorn
🏗️ Architecture
Frontend (HTML/JS/Bootstrap)
        │
        ▼  fetch() calls
FastAPI Backend (main.py)
        │
        ├── auth.py       → password hashing (bcrypt) + JWT tokens
        ├── models.py      → SQLAlchemy ORM models
        ├── database.py    → MySQL connection/session
        └── Razorpay SDK   → order creation + payment verification
        │
        ▼
MySQL Database (users, wallets, transactions)
📂 Database Schema
users — id, name, email, password_hash, created_at
wallets — id, user_id (FK), balance
transactions — id, user_id (FK), razorpay_order_id, razorpay_payment_id, amount, status, created_at
🔒 Security Highlights
Passwords are never stored in plain text — hashed using bcrypt.
Payment confirmation is never trusted from the client. After Razorpay redirects with a payment response, the backend independently recomputes the HMAC-SHA256 signature using the secret key (server-side only) and compares it — only then is the wallet balance updated.
JWTs are used for session auth instead of resending credentials on every request.
🚀 How It Works
User registers → account + wallet (₹0 balance) created in MySQL
User logs in → receives a signed JWT token
Dashboard fetches live wallet balance from the backend
User initiates a recharge → backend creates a Razorpay order
Razorpay checkout opens → user completes test payment
Backend verifies the payment signature server-side
On success, wallet balance is updated and a transaction record is logged
Transaction history is displayed on the dashboard
⚙️ Setup & Installation
Prerequisites
Python 3.12+
MySQL (via XAMPP or standalone)
Razorpay test account (free)
Backend Setup
bash
# Clone the repo
git clone <your-repo-url>
cd payben-backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install fastapi uvicorn sqlalchemy pymysql python-jose "passlib[bcrypt]" bcrypt razorpay python-multipart

# Set up the database
# Run the SQL schema (see /schema.sql) in phpMyAdmin or MySQL CLI

# Add your Razorpay test keys in main.py
# RAZORPAY_KEY_ID = "your_key_id"
# RAZORPAY_KEY_SECRET = "your_key_secret"

# Run the server
uvicorn main:app --reload

Backend runs at http://localhost:8000 — API docs available at http://localhost:8000/docs.

Frontend Setup

Open index.html with VS Code Live Server (or any static file server). Update the Razorpay key in dashboard.html with your Key ID.

📸 Screenshots

Add screenshots of the login page, dashboard, Razorpay checkout, and transaction history here.

🔮 Future Improvements
Row-level locking / atomic balance updates to prevent race conditions on concurrent recharges
Refresh token support
Email verification on signup
Deploy backend (Render/Railway) + frontend (Vercel/Netlify) for a live demo link
Mobile app (Flutter) consuming the same REST API
📄 License

This project was built for academic/portfolio purposes.

Note: This project uses Razorpay's test mode — no real payments are processed.