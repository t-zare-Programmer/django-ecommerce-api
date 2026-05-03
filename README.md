# 🛒 Shop Center - Django E-commerce Backend

A modular e-commerce backend system built with Django and Django REST Framework, designed for product management, user authentication, and scalable business logic.

---

## 🚀 Overview

Shop Center is a backend system for an e-commerce platform.  
It includes product management APIs, user authentication with JWT, and structured modules for orders, payments, discounts, and warehouse management.

The project is built with a modular architecture to support scalability and separation of concerns.

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

---

## ⚙️ Key Features

### 🔐 Authentication
- JWT-based authentication using `djangorestframework-simplejwt`
- Custom user model (`accounts.CustomUser`)
- Token-based secure API access

---

### 📦 Product Management
- Product API with CRUD operations
- Filtering by category and brand
- Search and ordering support
- Active/inactive product handling
- Nested relationships (Brand, Category, Gallery)

---

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

- apps/
  - accounts
  - products
  - orders
  - payments
  - discounts
  - warehouses
  - main

---

## 🗄️ Database

- PostgreSQL used as primary database
- Configured for scalable production-ready environment

---

## ⚙️ Installation

```bash
git clone https://github.com/t-zare-Programmer/shop_center.git
cd shop_center

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
