# 🛍️ E-commerce Product API (Django + DRF)

A **RESTful API** for managing users, categories, and products in an e-commerce platform.  
Built with **Django + Django REST Framework** and connected to **PostgreSQL**.

---

## 🚀 Features

### 🔐 User Management
- Register with **username, email, and password**  
- Login to obtain an **authentication token**  
- Authenticated users can **create, update, delete products**  
- Admins can manage **all users and categories**  

### 📦 Product Management
- Fields: `name`, `description`, `price`, `category`, `stock`, `image_url`, `created_at`  
- Validations:  
  - `price > 0`  
  - `stock ≥ 0`  
  - `name` required  
- Products are linked to **categories** and **owners (users)**  

### 🏷️ Category Management
- Create, update, delete categories (**admin only**)  
- Products can be assigned to categories  

### 🔍 Search & Filtering
- Search by **product name** or **category**  
- Filters:  
  - `category`  
  - `price_min`, `price_max`  
  - `in_stock=true/false`  
- Ordering: by **price**, **date**, or **name**  

### 📄 Pagination
- Page-based pagination (`?page=2`)  
- Configurable in settings  

### 🔑 Authentication
- **Token-based authentication**  
- Add token in request headers:
  ```http
  Authorization: Token your_token_here
