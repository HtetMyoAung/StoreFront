# 🛒 StoreFront - Secured E-Commerce REST API

A robust, production-grade E-Commerce REST API built with Django and Django REST Framework (DRF). This project implements an advanced API security architecture, industry-standard authentication protocols, dynamic role-based access control (RBAC), and specialized user profile mappings.

---

## 🔐 Security Architecture

This API is hardened using a multi-layered backend security strategy, balancing tight data-access restrictions with an optimal client user experience.

### 1. Token Rotation Architecture (JWT)
Instead of relying on long-lived API tokens that pose a severe security risk if intercepted, this system separates capabilities using **JSON Web Tokens (JWT)** via `djangorestframework-simplejwt`:
* **Access Token:** Short-lived token expiring in **5 minutes** used for authorizing everyday data operations against API endpoints.
* **Refresh Token:** Long-lived token expiring in **14 days** stored safely by the client, utilized behind the scenes to request fresh access tokens via `/auth/jwt/refresh/` without interrupting the user experience or forcing re-authentication.

### 2. User & Dynamic Profile Mapping
Built on top of **Djoser**, the user management ecosystem features a unified data stream:
* **`/auth/users/me/` Overriding:** Extended Djoser's core user endpoints with a custom nested serializer (`CurrentUserSerializer`) to automatically bridge Core Auth data (`id`, `username`, `email`) with application-specific e-commerce profiles.
* **`/api/customers/me/` Special Action:** Implemented a non-id-dependent custom `@action(detail=False)` route inside `CustomerViewSet` allowing front-end clients to query and update (`GET`/`PUT`) their personalized shopping profiles instantly using only their active bearer token.

### 3. Granular Access Control & Permissions
Endpoints are locked down utilizing a blend of Django's native permissions and customized policy classes:
* **Method-Based Permission Overriding:** Applied context-driven rules via `get_permissions()`. Public visitors enjoy read-only access (`GET`), while destructive or data-altering mutations (`POST`, `PUT`, `DELETE`) are restricted exclusively to authenticated store staff.
* **Database-Driven Model Permissions:** Integrated a customized version of DRF's `DjangoModelPermissions` (named `FullDjangoModelPermissions`) which explicitly maps incoming REST HTTP methods (including `GET` requests) directly to database-level user group assignments dynamically configured inside the Django Admin panel.

---

## 🚀 API Endpoints Map

### Authentication & User Management (Djoser/JWT)
| HTTP Method | Endpoint | Description | Access Level |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/users/` | Register a brand new user account | Public |
| `POST` | `/auth/jwt/create/` | Log in and receive JWT Access & Refresh token pairs | Public |
| `POST` | `/auth/jwt/refresh/` | Exchange an active Refresh token for a new Access token | Public |
| `GET` | `/auth/users/me/` | Retrieve core account details alongside profile IDs | Authenticated |

### Store & E-Commerce Profiles
| HTTP Method | Endpoint | Description | Access Level |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/products/` | Browse the store's catalogue listings | Public |
| `POST` / `DELETE` | `/api/products/` | Create or remove structural product listings | Admin / Staff Only |
| `GET` | `/api/customers/` | View global customer tracking sheets | Admin / Staff Only |
| `GET` / `PUT` | `/api/customers/me/` | Read or update the current user's e-commerce profile | Authenticated Owner |

---

## 🛠️ Technology Stack & Packages

* **Backend Framework:** Django 5.x Ecosystem
* **API Toolkit:** Django REST Framework (DRF)
* **Authentication Provider:** `djangorestframework-simplejwt`
* **User Management System:** `djoser`

---

## 💻 Local Installation & Setup

Follow these procedural instructions to launch and explore the secured backend ecosystem locally.

1. **Clone the repository and jump into the directory:**
   ```bash
   git clone [https://github.com/HtetMyoAung/StoreFront.git](https://github.com/HtetMyoAung/StoreFront.git)
   cd StoreFront
