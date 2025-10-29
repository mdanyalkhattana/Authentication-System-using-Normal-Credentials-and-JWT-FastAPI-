 # 🔐 Authentication System using Normal Credentials and JWT (FastAPI)

## 📘 Overview

The **Authentication System using Normal Credentials and JWT** is a secure and modular backend built with **FastAPI**.
It enables users to **sign up, verify their email, log in, log out, and reset their password** — all using **normal credentials (email & password)** with **JWT-based authentication** for secure session handling.

This project follows modern backend development standards and can easily be integrated into any **frontend application** (React, Angular, Vue, etc.) or **mobile app**.

---

## 🏗️ Project Structure

```
AuthenticationSystem/
│
├── main.py                           # Application entry point
├── database.py                       # SQLAlchemy setup (engine, Base, SessionLocal)
│
├── config/
│   └── config.py                     # Environment & app configuration (Pydantic)
│
├── models/                           # SQLAlchemy ORM models
│   ├── user_model.py                 # User table
│   ├── session_model.py              # Session table
│   ├── email_verification_model.py   # Email verification table
│   ├── password_reset_model.py       # Password reset table
│   └── audit_log_model.py            # Optional: Logs user activity
│
├── schemas/                          # Pydantic data validation schemas
│   ├── user_schema.py                # User creation & response schemas
│   ├── auth_schema.py                # Login & token schemas
│   ├── verify_schema.py              # Email verification schema
│   ├── password_schema.py            # Forgot/reset password schema
│   └── token_schema.py               # JWT schema
│
├── routes/                           # FastAPI route files
│   ├── auth_routes.py                # Signup, login, logout routes
│   ├── verify_routes.py              # Email verification routes
│   ├── password_routes.py            # Forgot/reset password routes
│   └── session_routes.py             # Manage active sessions
│
├── utils/                            # Utility/helper modules
│   ├── hashing.py                    # Password hashing (Argon2 / bcrypt)
│   ├── jwt_utils.py                  # Create and verify JWT tokens
│   ├── email_utils.py                # Send emails via SMTP
│   ├── session_utils.py              # Session management
│   └── security_utils.py             # (Optional) Password strength validation
│
├── tests/
│   └── test_auth.py                  # Unit tests
│
├── .env                              # Environment variables
├── requirements.txt                  # Dependencies
└── README.md                         # Project documentation
```

---

## ⚙️ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

### **requirements.txt**

```text
fastapi
uvicorn
sqlalchemy
pydantic
pydantic-settings
python-jose[cryptography]
python-multipart
email-validator
mysql-connector-python
argon2-cffi
passlib[bcrypt]
```

---

## 🧩 Entities and Relationships

| Entity                | Description                  | Primary Key | Foreign Key      | Relationship                          |
| --------------------- | ---------------------------- | ----------- | ---------------- | ------------------------------------- |
| **User**              | Stores user information      | `id`        | —                | 1:N with Session, Verification, Reset |
| **Session**           | Tracks user sessions         | `id`        | `user_id` → User | Belongs to User                       |
| **EmailVerification** | Stores verification tokens   | `id`        | `user_id` → User | Belongs to User                       |
| **PasswordReset**     | Stores password reset tokens | `id`        | `user_id` → User | Belongs to User                       |

---

## 🔁 Flow of the Project

### 🧱 1. **Signup**

* User registers using username, email, and password.
* Password is hashed using Argon2.
* Verification email is sent with a unique token.

### ✉️ 2. **Email Verification**

* User clicks the link or enters a code.
* Account becomes verified (`is_verified = True`).

### 🔑 3. **Login**

* User logs in using email & password.
* JWT token is generated for authentication.
* Session is created in the database.

### 🚪 4. **Logout**

* User logs out.
* Session is deactivated.

### 🔁 5. **Forgot / Reset Password**

* User requests password reset link via email.
* Token is sent and used to update password securely.

### 🧩 6. **Session Check**

* Prevents multiple logins on the same account.

---

## 🧠 Techniques Used

| Technique                        | Purpose                               |
| -------------------------------- | ------------------------------------- |
| **FastAPI**                      | High-performance API framework        |
| **SQLAlchemy ORM**               | Database mapping and management       |
| **Argon2 / Bcrypt**              | Secure password hashing               |
| **JWT (JSON Web Token)**         | Stateless authentication              |
| **SMTP**                         | Email verification and reset password |
| **Pydantic Models**              | Data validation and serialization     |
| **Dependency Injection**         | Database session handling             |
| **Environment Variables (.env)** | Secure configuration                  |

---

## 🏗️ Architecture

```
[ Client / Frontend ]
        ↓
[ FastAPI Routes / Controllers ]
        ↓
[ Business Logic (Utils) ]
        ↓
[ Data Layer (SQLAlchemy ORM) ]
        ↓
[ MySQL Database ]
```

This modular structure ensures:

* 🔄 Reusability
* 🧩 Scalability
* 🔐 Security
* 🧱 Maintainability

---

## 🌟 Features

✅ Email-based registration
✅ Email verification system
✅ JWT authentication & token expiry
✅ Forgot and reset password feature
✅ Session tracking (prevent multiple logins)
✅ Secure password hashing
✅ Easy MySQL integration
✅ Fully tested endpoints via Swagger UI
✅ Modular project structure

---

## 🔗 API Endpoints

| Method   | Endpoint           | Description                     |
| -------- | ------------------ | ------------------------------- |
| **POST** | `/auth/signup`     | Register new user               |
| **POST** | `/verify/send`     | Send verification email         |
| **POST** | `/verify/confirm`  | Verify user email               |
| **POST** | `/auth/login`      | User login & JWT generation     |
| **POST** | `/auth/logout`     | Logout and deactivate session   |
| **POST** | `/password/forgot` | Send reset link to user         |
| **POST** | `/password/reset`  | Reset password                  |
| **GET**  | `/session/active`  | Check if user session is active |
| **GET**  | `/`                | API health/status check         |

---

## 🧰 How to Run This Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Authentication-System-Using-Normal-Credentials-and-JWT.git
cd Authentication-System-Using-Normal-Credentials-and-JWT
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # For Windows
# or
source venv/bin/activate   # For Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create `.env` file:

```env
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DB_NAME=auth_system

SECRET_KEY=mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

SMTP_EMAIL=youremail@gmail.com
SMTP_PASSWORD=yourpassword
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 5️⃣ Run the Application

```bash
uvicorn main:app --reload
```

### 6️⃣ Access Swagger UI

```
http://127.0.0.1:8000/docs
```

You can now test all APIs directly through your browser.

---

## 🧱 Example JWT Login Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Use the token in your request headers:

```
Authorization: Bearer <your_token_here>
```

---

## 🚀 Future Enhancements

* 🔒 Two-Factor Authentication (2FA)
* 🌍 Google / GitHub OAuth Login
* 🧩 Role-Based Access Control (RBAC)
* 💾 Redis-based session management
* 🧠 Unit and integration testing
* 📱 Integration with a React or Flutter frontend

---

## 👨‍💻 Author

**Muhammad Danyal**
💼 Project Manager | Developer | AI & Research Expert
📧 [your-email@example.com](mailto:your-email@example.com)
🌐 [GitHub Profile](https://github.com/yourusername)

 

Would you like me to generate this as a **ready-to-download `README.md` file** (with Markdown formatting, emojis, and proper spacing) so you can just drop it into your project folder and upload to GitHub?
