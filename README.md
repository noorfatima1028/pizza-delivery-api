# 🍕 Pizza Delivery API

A RESTful Pizza Delivery API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT Authentication**.

---

##  About the Project

This project is a backend REST API for a pizza delivery system developed using FastAPI. It allows users to securely register, authenticate using JWT tokens, and perform CRUD operations on pizza orders. The project was built to strengthen my backend development skills and gain hands-on experience with REST API development, authentication, database integration, and version control using Git and GitHub.

---

##  Features

- 👤 User Registration
- 🔐 User Login with JWT Authentication
- ♻️ Refresh JWT Tokens
- 🍕 Place a New Pizza Order
- 📋 View All Orders
- 🔍 View a Single Order
- 👤 View Logged-in User's Orders
- ✏️ Update an Order
- 🚚 Update Order Status
- ❌ Delete an Order
- 🔒 Password Hashing
- 📄 Interactive API Documentation with Swagger UI

---

##  Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Uvicorn
- Git
- GitHub

---

##  Project Structure

```text
pizza-delivery-api/
│
├── auth_routes.py
├── database.py
├── init_db.py
├── main.py
├── models.py
├── order_routes.py
├── schema.py
├── README.md
└── requirements.txt
```

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/noorfatima1028/pizza-delivery-api.git
```

### 2. Navigate to the Project Directory

```bash
cd pizza-delivery-api
```

### 3. Create a Virtual Environment

```bash
python -m venv env
```

### 4. Activate the Virtual Environment

#### Linux/macOS

```bash
source env/bin/activate
```

#### Windows

```bash
env\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
uvicorn main:app --reload
```

The API will start at:

```text
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation.

After running the project, visit:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## 📌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| POST | `/auth/refresh` | Refresh access token |

### Orders

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/orders/order` | Place a new order |
| GET | `/orders/orders` | Retrieve all orders |
| GET | `/orders/order/{id}` | Retrieve a single order |
| GET | `/orders/user/orders` | Retrieve current user's orders |
| PUT | `/orders/order/update/{id}` | Update an existing order |
| PATCH | `/orders/order/status/{id}` | Update order status |
| DELETE | `/orders/order/delete/{id}` | Delete an order |

---

##  Future Improvements

- 🐳 Docker support
- 🧪 Unit and integration testing
- 🔄 CI/CD pipeline
- 👥 Role-based authorization
- 💳 Payment gateway integration
- 📧 Email notifications
- 📦 Order tracking

---

## 👩 Author

**Noor Fatima**

- GitHub: https://github.com/noorfatima1028
- LinkedIn: www.linkedin.com/in/noor-fatima-6767613ab

---

