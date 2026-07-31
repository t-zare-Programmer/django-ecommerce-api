# 🛒 Shop Center

![CI](https://github.com/t-zare-Programmer/django-ecommerce-api/actions/workflows/django.yml/badge.svg)

![Codecov](https://codecov.io/gh/t-zare-Programmer/django-ecommerce-api/branch/main/graph/badge.svg)

![Python](https://img.shields.io/badge/Python-3.12-blue)

![Django](https://img.shields.io/badge/Django-5.x-success)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)

![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)

> Production-ready Django REST Framework backend for scalable e-commerce applications.

A modular e-commerce backend built with Django and Django REST Framework (DRF), following a clean architecture and service layer pattern for scalability, maintainability, and production-ready API development.

---------------------------------------------------------------------------------------

## 🚀 Overview

Shop Center is a scalable e-commerce backend built with Django and Django REST Framework (DRF).

The project follows a modular and service-oriented architecture to support clean business logic separation, API scalability, and maintainability.

It includes JWT authentication, product management APIs, warehouse management, discount systems, and API documentation using Swagger/OpenAPI.

---------------------------------------------------------------------------------------

## ✨ Highlights

- 🔐 JWT Authentication (SimpleJWT)
- 🛒 RESTful Product Management API
- 🧩 Service Layer Architecture
- 🔎 Filtering, Searching & Ordering
- 📄 OpenAPI 3 Documentation (Swagger & ReDoc)
- 🧪 Pytest Test Suite
- ⚡ Redis Cache Integration
- 📨 Celery Background Tasks
- 🐳 Docker Support
- 🚀 GitHub Actions CI Pipeline

---------------------------------------------------------------------------------------

## ⚙️ Key Features

### Authentication
- Custom User Model
- JWT Authentication using SimpleJWT
- Secure Token-based API Access

### Product Management
- Full CRUD REST API
- Nested Serializers
- Product Gallery
- Brand Management
- Service Layer Pattern

### API Features
- Pagination
- Filtering
- Searching
- Ordering
- Standardized API Responses

### Performance
- Redis Caching
- Celery Background Tasks

### Testing
- Pytest
- Factory Boy
- API Testing
- Service Layer Testing

### Documentation
- Swagger UI
- ReDoc
- OpenAPI 3 Schema

### Infrastructure
- Docker
- Docker Compose
- GitHub Actions CI

### Business Modules
- Orders
- Payments
- Warehouses
- Discounts
- Reviews, Ratings & Favorites

---------------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------------

## 🏛️ Architecture

The project follows a layered architecture to keep responsibilities separated and the codebase maintainable.

```text
                Client
                   │
                   ▼
          Django REST API Views
                   │
                   ▼
             Serializers (Validation)
                   │
                   ▼
          Service Layer (Business Logic)
                   │
                   ▼
         Django ORM / Models
                   │
                   ▼
              PostgreSQL
```

### Design Principles

- Separation of Concerns
- Service Layer Pattern
- Thin Views
- Reusable Business Logic
- Scalable REST API Design

---------------------------------------------------------------------------------------

## 🔗 Example API Endpoints

- GET /api/products/
- POST /api/products/create/
- GET /api/products/{slug}/
- PUT /api/products/{slug}/update/
- DELETE /api/products/{slug}/delete/

---------------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------------

## 🚧 Future Improvements

- Docker support
- CI/CD pipeline
- Redis caching
- Celery background tasks
- React frontend integration
- Kubernetes deployment
- AWS cloud deployment

---------------------------------------------------------------------------------------

## 📂 Project Structure

```text
shop_center/
│
├── apps/
│   ├── accounts/                  # Authentication & User Management
│   ├── products/                  # Product Domain
│   │   ├── api/
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   └── pagination.py
│   │   │
│   │   ├── services/
│   │   │   └── product_service.py
│   │   │
│   │   ├── tests/
│   │   │   ├── conftest.py
│   │   │   ├── test_api_products.py
│   │   │   └── test_services.py
│   │   │
│   │   ├── factories.py
│   │   ├── tasks.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   └── views.py
│   │
│   ├── orders/                    # Order Processing
│   ├── payments/                  # Payment Management
│   ├── discounts/                 # Discount Engine
│   ├── warehouses/                # Inventory Management
│   ├── comment_scoring_favorites/ # Reviews, Ratings & Favorites
│   ├── main/                      # Website Entry Points
│   └── core/                      # Shared Utilities & Common Components
│
├── shop_center/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

---------------------------------------------------------------------------------------

## 🗄️ Database

- PostgreSQL used as primary database
- Configured for scalable production-ready environment

---------------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------------

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=shop_center
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

The project uses **python-decouple** to securely load environment variables.

---------------------------------------------------------------------------------------

## 🐳 Running with Docker

Build and start all services:

```bash
docker compose up --build
```

Run database migrations:

```bash
docker compose exec web python manage.py migrate
```

Create a superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

Run the test suite:

```bash
docker compose exec web pytest
```

Stop all services:

```bash
docker compose down
```

---------------------------------------------------------------------------------------

## 🧪 Running Tests

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=apps/products --cov-report=term-missing
```

Current coverage:

- ✅ Product API Tests
- ✅ Service Layer Tests
- ✅ Factory-based Test Data
- ✅ GitHub Actions Continuous Integration

---------------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------------

## ⚙️ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---------------------------------------------------------------------------------------

## 👤 Create Superuser

```bash
python manage.py createsuperuser
```

---------------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------------

## 🚀 Run Development Server

```bash
python manage.py runserver
```

Server will be available at:

```text
http://127.0.0.1:8000/
```

---------------------------------------------------------------------------------------

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
