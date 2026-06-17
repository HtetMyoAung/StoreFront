# Storefront - E-commerce REST API

A powerful, scalable, and secure e-commerce RESTful API built using Django and Django REST Framework (DRF). This project follows clean architecture principles and enterprise-grade backend development patterns.

> 🛠️ **Project Status:** **In Progress** (Active Development)
> I am currently building this project to master advanced backend concepts, industrial best practices, and enterprise standards taught by Mosh Hamedani.

---

## 🚀 Key Features Implemented So Far

### 1. Product & Collection Management
* Full CRUD operations for Products and Categories/Collections.
* Advanced filtering (by collection), full-text search, and multi-column ordering.
* Custom pagination for performance optimization.
* Database annotations (e.g., dynamic product counts for collections).

### 2. Shopping Cart System
* Robust shopping cart logic using **UUIDs** for secure, session-independent carts.
* Dynamic cart nested items retrieval, addition, and quantity updating.
* Auto-calculation of item total prices and overall cart summaries.

### 3. Customer & Profile Architecture
* Extended Django's built-in User model using a **One-to-One relationship** to support rich Customer Profiles.
* Auto-creation of Customer profiles upon new User registration using **Django Signals**.

### 4. Advanced Django Admin Customization
* Overhauled the default Django Admin panel into a professional dashboard.
* Added inline model management (e.g., editing cart items directly inside carts).
* Implemented custom administrative actions (e.g., bulk clearing inventory).

---

## 🗺️ Future Roadmap (What I'm Building Next)
- [ ] Implement JWT Authentication (JSON Web Tokens) & User Permissions.
- [ ] Set up Automated Unit Testing with Pytest.
- [ ] Implement Caching using Redis to optimize database queries.
- [ ] Configure Background Tasks (Celery & Redis) for sending emails.
- [ ] Production deployment and server performance optimization.

---

## 🛠️ Tech Stack Used
* **Backend:** Python, Django, Django REST Framework (DRF)
* **Database:** MySQL / PostgreSQL
* **Tools:** Postman (API Testing), Git/GitHub (Version Control)

---