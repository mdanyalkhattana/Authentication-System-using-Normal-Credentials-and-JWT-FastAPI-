 # 🔐 Authentication System using Normal Credentials and JWT (FastAPI)

## 📘 Overview

The **Authentication System using Normal Credentials and JWT (FastAPI)** is a secure and modular backend designed for modern applications requiring user authentication and authorization.

This system allows users to **sign up**, **verify their email**, **log in**, **reset passwords**, **logout**, and **manage sessions** securely using **JWT (JSON Web Tokens)** and **Argon2 password hashing**.

It can serve as a backend for:

* Web applications (React, Angular, Vue)
* Mobile apps (Flutter, Android, iOS)
* Enterprise systems needing secure user management

This project follows a **clean architecture**, ensuring that the system is **scalable, testable, maintainable, and secure**.

---

## 🧱 Key Objectives

* Secure user registration and login system using email and password
* Email verification through unique tokens
* JWT authentication for session management
* Forgot and reset password workflows
* Prevention of multiple active sessions per user
* Modular structure for future scalability and integration

---

## 🏗️ Project Structure

```
AuthenticationSystem/
│
├── main.py                           # Application entry point (creates FastAPI instance)
├── database.py                       # SQLAlchemy setup (engine, Base, SessionLocal)
│
├── config/
│   └── config.py                     # Configuration and environment settings
│
├── models/                           # SQLAlchemy ORM Models
│   ├── user_model.py                 # User model (email, password, verification)
│   ├── session_model.py              # Active session model
│   ├── email_verification_model.py   # Email verification tokens
│   ├── password_reset_model.py       # Password reset tokens
│   └── audit_log_model.py            # Optional: Logs user actions (login/logout)
│
├── schemas/                          # Pydantic Schemas (Validation Models)
│   ├── user_schema.py                # User create & response models
│   ├── auth_schema.py                # Login & JWT token schemas
│   ├── verify_schema.py              # Email verification schema
│   ├── password_schema.py            # Forgot/reset password schema
│   └── token_schema.py               # JWT structure schema
│
├── routes/                           # API Endpoints
│   ├── auth_routes.py                # Signup, login, logout
│   ├── verify_routes.py              # Email verification
│   ├── password_routes.py            # Forgot/reset password
│   └── session_routes.py             # Session check
│
├── utils/                            # Utility modules
│   ├── hashing.py                    # Argon2 password hashing and verification
│   ├── jwt_utils.py                  # Create and verify JWT tokens
│   ├── email_utils.py                # Send verification & reset emails
│   ├── session_utils.py              # Manage session state
│   └── security_utils.py             # Optional password strength validator
│
├── tests/
│   └── test_auth.py                  # Unit and integration tests
│
├── .env                              # Environment variables
├── requirements.txt                  # Dependencies
└── README.md                         # Documentation
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

## 🧩 Database Entities and Relationships

| Entity                | Description                               | Primary Key | Foreign Key      | Relationship                             |
| --------------------- | ----------------------------------------- | ----------- | ---------------- | ---------------------------------------- |
| **User**              | Stores registered user data               | `id`        | —                | 1:N with Sessions, Verifications, Resets |
| **Session**           | Tracks active user sessions               | `id`        | `user_id` → User | Belongs to User                          |
| **EmailVerification** | Stores verification tokens                | `id`        | `user_id` → User | Belongs to User                          |
| **PasswordReset**     | Manages password reset tokens             | `id`        | `user_id` → User | Belongs to User                          |
| **AuditLog**          | Optional tracking of login/logout actions | `id`        | `user_id` → User | Belongs to User                          |

---

## 🔁 Flow of the System

### 1️⃣ **Signup**

* User registers using username, email, and password.
* The password is hashed using **Argon2**.
* A **verification email** is sent to confirm ownership.

### 2️⃣ **Email Verification**

* User receives an email with a **tokenized link**.
* Clicking it activates the account (`is_verified=True`).

### 3️⃣ **Login**

* User provides credentials.
* The password is verified, and a **JWT access token** is generated.
* Session is created and stored in DB.

### 4️⃣ **Session Management**

* Each user can have only **one active session** at a time.
* Attempts to log in again prompt a warning: *"Session already active"*.

### 5️⃣ **Forgot Password**

* User requests a reset link.
* Email is sent with a secure token for password reset.

### 6️⃣ **Reset Password**

* User sets a new password using the received token.
* Old tokens and sessions are invalidated.

### 7️⃣ **Logout**

* User logs out manually.
* Session is marked as inactive.

---

## 🧠 Techniques Used

| Technique                | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| **FastAPI**              | Framework for high-performance async APIs              |
| **SQLAlchemy ORM**       | Object Relational Mapper for database tables           |
| **Argon2 / Bcrypt**      | Advanced password hashing algorithms                   |
| **JWT (JSON Web Token)** | Secure token-based authentication                      |
| **SMTP**                 | Used to send email verification & password reset links |
| **Pydantic**             | Data validation and serialization                      |
| **Dependency Injection** | Efficient DB and token handling                        |
| **.env Configuration**   | Secure environment variable management                 |

---

## 🏗️ Architecture

```
               ┌────────────────────────────┐
               │        FRONTEND APP        │
               │ (React / Angular / Flutter)│
               └──────────────┬─────────────┘
                              │
                              ▼
                  ┌────────────────────┐
                  │   FASTAPI ROUTES   │
                  │ (auth, verify etc) │
                  └────────┬───────────┘
                           │
                           ▼
                   ┌─────────────────┐
                   │     SCHEMAS     │
                   │  (Data models)  │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │     UTILS       │
                   │(JWT, Hash, Mail)│
                   └────────┬────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │     MODELS       │
                   │ (SQLAlchemy ORM) │
                   └────────┬─────────┘
                            │
                            ▼
                     🗄️ MySQL DATABASE
```

This **layered architecture** ensures:

* Clean separation of business logic
* Scalability for future modules
* Easier maintenance and testing

---

## 🌟 Project Features

✅ Secure password hashing using Argon2
✅ JWT-based authentication and session control
✅ Email verification via SMTP
✅ Forgot/reset password workflow
✅ Single active session management
✅ Validation of user input
✅ Error handling and structured JSON responses
✅ Swagger UI for API testing
✅ Modular and maintainable codebase

---

## 🔗 API Endpoints

| Method   | Endpoint           | Description                   |
| -------- | ------------------ | ----------------------------- |
| **POST** | `/auth/signup`     | Register a new user           |
| **POST** | `/verify/send`     | Send email verification token |
| **POST** | `/verify/confirm`  | Verify email token            |
| **POST** | `/auth/login`      | Login and generate JWT        |
| **POST** | `/auth/logout`     | Logout and deactivate session |
| **POST** | `/password/forgot` | Request password reset link   |
| **POST** | `/password/reset`  | Reset password using token    |
| **GET**  | `/session/active`  | Check active session          |
| **GET**  | `/`                | API status check              |

---

## 🧰 Setup & Usage

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/Authentication-System-Using-Normal-Credentials-and-JWT.git
cd Authentication-System-Using-Normal-Credentials-and-JWT
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate    # Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure `.env`

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

### 6️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

You can now test all endpoints from your browser!

---

## 🧱 Example API Usage

### **Signup**

**POST** `/auth/signup`

```json
{
  "username": "danyal",
  "email": "danyal@example.com",
  "password": "SecurePass123"
}
```

**Response**

```json
{
  "status": 201,
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "danyal",
    "email": "danyal@example.com",
    "is_verified": false
  }
}
```

---

### **Login**

**POST** `/auth/login`

```json
{
  "email": "danyal@example.com",
  "password": "SecurePass123"
}
```

**Response**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer"
}
```

Use this token in headers:

```
Authorization: Bearer <your_token_here>
```

---

## 🚀 Future Enhancements

* 🔒 Two-Factor Authentication (2FA)
* 🌍 Social login (Google, GitHub OAuth2)
* 🧩 Role-based Access Control (RBAC)
* 💾 Redis session caching
* 🧠 Add test automation and CI/CD
* 📱 Integration with a frontend dashboard

---

## 👨‍💻 Author

**Muhammad Danyal**
💼 Project Manager | Ali Sher Sie | AI & Backend Expert
🌐 [GitHub Profile](https://github.com/yourusername)

---
 
