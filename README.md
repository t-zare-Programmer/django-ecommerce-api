# 🛒 Shop Center – Scalable Django E-commerce Backend

A modular e-commerce backend system built with Django and Django REST Framework, designed for product management, user authentication, and scalable business logic.

---

## 🚀 Overview

Shop Center is a scalable e-commerce backend built with Django and Django REST Framework (DRF).

The project follows a modular and service-oriented architecture to support clean business logic separation, API scalability, and maintainability.

It includes JWT authentication, product management APIs, warehouse management, discount systems, and API documentation using Swagger/OpenAPI.

---

## 🧰 Tech Stack

- Python
- Django
- Django REST Framework (DRF)
- PostgreSQL
- SimpleJWT (Authentication)
- Django Filters
- CKEditor (Rich Text Editor)
- drf-spectacular (API documentation)
- Swagger / OpenAPI
- Service Layer Pattern
- Git & GitHub Workflow

---

## 🏗️ Architecture

The project follows a modular architecture with separation of concerns:

- Views handle HTTP requests and responses
- Serializers handle validation and transformation
- Services contain business logic
- Models manage database structure

This structure improves:
- scalability
- maintainability
- testability
- clean code organization

## ⚙️ Key Features

### 🔐 Authentication
- JWT-based authentication using `djangorestframework-simplejwt`
- Custom user model (`accounts.CustomUser`)
- Token-based secure API access

---

### 📦 Product Management API

- CRUD operations for products
- Nested serializers for brand, category, and gallery
- JWT-protected admin endpoints
- Service Layer implementation for business logic
- Swagger/OpenAPI documentation
- Search, filtering, and ordering support (in progress)

---

## 🔗 Example API Endpoints

- GET /api/products/
- POST /api/products/create/
- GET /api/products/{slug}/
- PUT /api/products/{slug}/update/
- DELETE /api/products/{slug}/delete/

## 🌱 Seed Data

The project includes a custom seed script for generating test data:

- Products
- Brands
- Categories
- Orders
- Warehouses
- Discounts
- Users

This helps simulate realistic e-commerce scenarios during development.

## 🔀 Git Workflow

Development follows a feature-branch workflow:

- main → stable production-ready code
- feature/* → isolated feature development

Example:
`feature/product-service-layer`

## 🚧 Future Improvements

- Docker support
- CI/CD pipeline
- Redis caching
- Celery background tasks
- React frontend integration
- Kubernetes deployment
- AWS cloud deployment

### 🛒 Order & Cart System (In Development)
- Orders module structure implemented
- Payment module structure prepared
- Business logic under development

---

### 🏷️ Discounts System
- Discount app structure available for promotions

---

### 🏬 Warehouse Management
- Inventory and stock management module

---

### 📝 Content Management
- CKEditor integration for rich text editing
- Image upload support for products and content

---

### 📊 Admin Panel
- Fully customized Django admin
- Advanced filtering and search in admin interface
- Optimized model display for management

---

## 📂 Project Structure

```text
apps/
├── accounts/
├── products/
├── orders/
├── payments/
├── discounts/
├── warehouses/
└── main/
```

---

## 🗄️ Database

- PostgreSQL used as primary database
- Configured for scalable production-ready environment

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/t-zare-Programmer/shop_center.git
cd shop_center
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

Create a PostgreSQL database and configure database settings inside:

```python
shop_center/settings.py
```

Example configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop_center',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## ⚙️ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 👤 Create Superuser

```bash
python manage.py createsuperuser
```

---

## 🌱 Seed Test Data

The project includes a custom seed script for generating sample data.

Run:

```bash
python seed_data_precise.py
```

This script generates:

- Products
- Brands
- Categories
- Users
- Orders
- Discounts
- Warehouses

---

## 🚀 Run Development Server

```bash
python manage.py runserver
```

Server will be available at:

```text
http://127.0.0.1:8000/
```

---

## 📘 API Documentation

Available API documentation endpoints:

### Swagger UI
```text
http://127.0.0.1:8000/api/docs/
```

### ReDoc
```text
http://127.0.0.1:8000/api/redoc/
```

### OpenAPI Schema
```text
http://127.0.0.1:8000/api/schema/
```
