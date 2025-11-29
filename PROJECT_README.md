# ShopHub - Full Stack E-Commerce Application

A modern, full-stack e-commerce application with a Django REST API backend and a responsive vanilla JavaScript frontend.

## Project Overview

ShopHub is a complete e-commerce solution featuring:
- RESTful API backend built with Django
- Modern, responsive frontend with vanilla JavaScript
- User authentication and authorization
- Product management (CRUD operations)
- Shopping cart functionality
- Advanced filtering and search
- Category-based organization

## Technology Stack

### Backend
- **Django 5.2.4** - Web framework
- **Django REST Framework 3.16.0** - API development
- **PostgreSQL** - Database (via psycopg2-binary)
- **Token Authentication** - User authentication
- **django-filter** - Advanced filtering
- **django-cors-headers** - CORS support
- **Whitenoise** - Static file serving
- **Gunicorn** - WSGI HTTP server

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling (Grid, Flexbox, animations)
- **Vanilla JavaScript** - No frameworks needed
- **Fetch API** - HTTP requests

## Project Structure

```
e_commerce_API/
├── e_commerce_API/          # Django project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
├── catalog/                 # Products & Categories app
│   ├── models.py            # Product, Category models
│   ├── views.py             # API views
│   ├── serializers.py       # Data serialization
│   ├── filters.py           # Filter classes
│   └── permissions.py       # Custom permissions
├── users/                   # User management app
│   ├── models.py            # Custom User model
│   ├── views.py             # Auth views
│   └── serializers.py       # User serialization
├── frontend/                # Frontend application
│   ├── index.html           # Main page
│   ├── css/
│   │   └── styles.css       # All styles
│   ├── js/
│   │   ├── api.js           # API client
│   │   ├── auth.js          # Authentication
│   │   ├── products.js      # Product management
│   │   ├── cart.js          # Shopping cart
│   │   └── app.js           # App initialization
│   ├── server.py            # Development server
│   └── README.md            # Frontend docs
├── requirements.txt         # Python dependencies
├── manage.py                # Django management
└── run_app.sh              # Startup script
```

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL
- pip (Python package manager)

### Installation

1. **Clone the repository** (if applicable)

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_db
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Create some categories** (via Django admin or shell)
   ```bash
   python manage.py shell
   >>> from catalog.models import Category
   >>> Category.objects.create(name="Electronics")
   >>> Category.objects.create(name="Clothing")
   >>> Category.objects.create(name="Books")
   ```

### Running the Application

#### Option 1: Use the startup script (Recommended)
```bash
./run_app.sh
```

This will start both the backend and frontend servers automatically.

#### Option 2: Run servers manually

**Terminal 1 - Backend:**
```bash
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python server.py
```

### Access the Application

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/token/` - Get auth token

### Products
- `GET /api/products/` - List all products
- `GET /api/products/:id/` - Get product detail
- `POST /api/products/` - Create product (auth required)
- `PUT /api/products/:id/` - Update product (owner only)
- `DELETE /api/products/:id/` - Delete product (owner only)

**Query Parameters:**
- `search` - Search by name or category
- `category` - Filter by category slug
- `price_min` - Minimum price
- `price_max` - Maximum price
- `ordering` - Sort by field (e.g., `price`, `-created_at`)

### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/:id/` - Get category detail
- `POST /api/categories/` - Create category (auth required)

### Users
- `GET /api/users/` - List users (auth required)
- `GET /api/users/:id/` - Get user detail (auth required)

## Features

### For All Users
- Browse products with beautiful card layouts
- Search products by name
- Filter by category, price range
- Sort by price, date, name
- View detailed product information
- Add items to shopping cart
- View cart and manage quantities

### For Authenticated Users
- Register and login
- Create new products
- Edit own products
- Delete own products
- View "My Products"
- Complete checkout

## Development

### Backend Development

**Run tests:**
```bash
python manage.py test
```

**Create migrations:**
```bash
python manage.py makemigrations
```

**Django shell:**
```bash
python manage.py shell
```

### Frontend Development

The frontend uses vanilla JavaScript - no build process needed! Just edit the files and refresh your browser.

**File organization:**
- **api.js** - All API communication
- **auth.js** - Authentication logic
- **products.js** - Product CRUD operations
- **cart.js** - Shopping cart management
- **app.js** - App initialization and utilities

## Configuration

### CORS Settings
Located in [settings.py](e_commerce_API/settings.py:134-154)

By default, allows:
- http://localhost:8080
- http://localhost:3000

Add more origins as needed.

### Database Configuration
Update `DATABASE_URL` in your `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

## Deployment

### Backend Deployment (Render, Heroku, etc.)

1. Set environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `DATABASE_URL`

2. Run collectstatic:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Frontend Deployment

The frontend is static HTML/CSS/JS and can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- Any static hosting service

**Important:** Update the `API_BASE_URL` in [frontend/js/api.js](frontend/js/api.js:2) to your production API URL.

## Security Considerations

1. **Never commit `.env` file** - Contains sensitive information
2. **Use strong SECRET_KEY** in production
3. **Set DEBUG=False** in production
4. **Configure ALLOWED_HOSTS** properly
5. **Use HTTPS** in production
6. **Keep dependencies updated**

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8080
lsof -ti:8080 | xargs kill -9
```

### CORS Errors
Make sure:
1. `corsheaders` is installed
2. It's in `INSTALLED_APPS`
3. Middleware is configured correctly
4. Frontend origin is in `CORS_ALLOWED_ORIGINS`

### Database Connection Issues
1. Verify PostgreSQL is running
2. Check `DATABASE_URL` in `.env`
3. Ensure database exists
4. Check credentials

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions:
- Check the documentation
- Review error logs
- Check Django and DRF documentation

## Acknowledgments

- Django and Django REST Framework communities
- All contributors and users

---

**Built with love using Django and Vanilla JavaScript**
