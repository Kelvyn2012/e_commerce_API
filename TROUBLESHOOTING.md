# Troubleshooting Guide

## Common Issues and Solutions

### 1. Category Filtering Not Working

**Problem:** Selecting a category doesn't filter products

**Solution:** ✅ FIXED - Added `DjangoFilterBackend` to the filter backends

**Verification:**
```bash
# Test category filter
curl "http://localhost:8000/api/products/?category=electronics"

# Should return only electronics products
```

**Files Changed:**
- `catalog/views.py` - Added `DjangoFilterBackend` import and to `filter_backends` list

---

### 2. Products Not Loading / API Error

**Symptoms:**
- Frontend shows "Error loading products"
- Empty product grid
- Console errors in browser

**Solutions:**

#### Check Backend Server
```bash
# Is Django running?
curl http://localhost:8000/api/products/

# If not, start it
python manage.py runserver
```

#### Check CORS Settings
In `settings.py`, verify:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

#### Check Browser Console
1. Open Developer Tools (F12)
2. Go to Console tab
3. Look for errors like:
   - CORS errors → Check CORS settings
   - 404 errors → Backend not running
   - Network errors → Wrong API URL

---

### 3. Frontend Not Loading

**Problem:** Cannot access http://localhost:8080

**Solution:**
```bash
# Check if frontend server is running
lsof -i:8080

# If not running, start it
cd frontend
python server.py
```

---

### 4. Authentication Issues

**Problem:** Login/Register not working

**Check These:**

1. **Backend has auth endpoints**
```bash
# Test login endpoint
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

2. **rest_framework.authtoken is installed**
In `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
    ...
]
```

3. **Migrations are applied**
```bash
python manage.py migrate
```

---

### 5. No Products Showing

**Problem:** Empty product list even after creating products

**Solutions:**

1. **Check database**
```bash
python manage.py shell
```
```python
from catalog.models import Product
print(f"Total products: {Product.objects.count()}")
```

2. **Create sample products**
```bash
# Run the sample data creation script
python manage.py shell < create_products.py
```

3. **Check product serializer**
```bash
# Test API directly
curl http://localhost:8000/api/products/ | python -m json.tool
```

---

### 6. Search Not Working

**Problem:** Search returns no results or all products

**Verification:**
```bash
# Test search
curl "http://localhost:8000/api/products/?search=laptop"

# Should return only products matching "laptop"
```

**Check:**
- `search_fields` in `ProductViewSet`
- `filters.SearchFilter` in `filter_backends`

---

### 7. Price Filtering Not Working

**Problem:** Price min/max filters don't work

**Verification:**
```bash
# Test price filter
curl "http://localhost:8000/api/products/?price_min=20&price_max=50"

# Should return 12 products in that range
```

**Check:**
- `ProductFilter` class in `catalog/filters.py`
- `DjangoFilterBackend` in filter_backends
- django-filter is installed

---

### 8. Images Not Displaying

**Problem:** Product images show as broken or placeholder emoji

**This is Normal if:**
- No image URL was provided for the product
- Image URL is invalid or broken
- External image host (like Unsplash) is down

**Solution:**
- Products without images show emoji placeholders (🛍️)
- This is intentional design
- Add valid image URLs when creating products

---

### 9. Cart Not Working

**Problem:** Cart count doesn't update or items don't save

**Check:**
- Browser localStorage (F12 → Application → Local Storage)
- Look for `cart` key with product data
- Clear cache if needed

**Reset Cart:**
```javascript
// In browser console
localStorage.removeItem('cart');
location.reload();
```

---

### 10. Port Already in Use

**Problem:** "Port 8000 is already in use"

**Solution:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Then restart
python manage.py runserver
```

**For port 8080:**
```bash
lsof -ti:8080 | xargs kill -9
cd frontend && python server.py
```

---

### 11. Database Connection Issues

**Problem:** "Could not connect to database"

**Check `.env` file:**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
DEBUG=True
SECRET_KEY=your-secret-key
```

**Verify PostgreSQL is running:**
```bash
# Check if PostgreSQL is running
pg_isready

# Start PostgreSQL (macOS)
brew services start postgresql
```

**Test connection:**
```bash
python manage.py dbshell
```

---

### 12. Static Files Not Loading

**Problem:** CSS/JS not loading on frontend

**For Development:**
- Frontend uses simple HTTP server
- Files should load automatically
- Check browser console for 404 errors

**Check File Paths:**
```
frontend/
├── index.html
├── css/
│   └── styles.css
└── js/
    ├── api.js
    ├── auth.js
    ├── products.js
    ├── cart.js
    └── app.js
```

---

### 13. Sorting Not Working

**Problem:** Products don't sort by selected option

**Verification:**
```bash
# Test sorting
curl "http://localhost:8000/api/products/?ordering=price"
curl "http://localhost:8000/api/products/?ordering=-price"
```

**Check:**
- `ordering_fields` in ProductViewSet
- `filters.OrderingFilter` in filter_backends

---

### 14. Creating Products Fails

**Problem:** "Error saving product" or validation errors

**Common Causes:**

1. **Not authenticated**
   - Login first before creating products

2. **Invalid category**
   - Category must exist in database
   - Use category ID, not name

3. **Invalid price**
   - Must be positive number
   - Use decimal format (e.g., 29.99)

4. **Missing required fields**
   - Name, price, category_id, stock_quantity are required

---

### 15. Modal Won't Close

**Problem:** Modal stuck open or won't close

**Solutions:**
- Press ESC key
- Click outside the modal (on dark overlay)
- Refresh the page

**If persists:**
```javascript
// In browser console
document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
```

---

## Debug Commands

### Check All Services
```bash
# Backend status
curl -s http://localhost:8000 > /dev/null && echo "✅ Backend running" || echo "❌ Backend down"

# Frontend status
curl -s http://localhost:8080 > /dev/null && echo "✅ Frontend running" || echo "❌ Frontend down"

# API status
curl -s http://localhost:8000/api/products/ | python -c "import json,sys; d=json.load(sys.stdin); print(f'✅ API: {len(d)} products')" 2>/dev/null || echo "❌ API error"
```

### View Django Logs
```bash
# Backend logs show in terminal where you ran:
python manage.py runserver
```

### Browser Console
```javascript
// Check if API is reachable
fetch('http://localhost:8000/api/products/')
  .then(r => r.json())
  .then(d => console.log(`${d.length} products loaded`))
  .catch(e => console.error('API Error:', e));

// Check cart
console.log('Cart:', localStorage.getItem('cart'));

// Check auth
console.log('Token:', localStorage.getItem('authToken'));
console.log('User:', localStorage.getItem('username'));
```

---

## Getting Help

1. **Check the logs** - Django terminal output
2. **Check browser console** - F12 → Console tab
3. **Test API directly** - Use curl commands above
4. **Verify services running** - Both servers must be up
5. **Check documentation** - See PROJECT_README.md

---

## Quick Reset

If everything is broken and you want to start fresh:

```bash
# 1. Kill all servers
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null

# 2. Clear database (optional - will delete all data!)
python manage.py flush

# 3. Re-run migrations
python manage.py migrate

# 4. Create categories
python manage.py shell -c "
from catalog.models import Category
for name in ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']:
    Category.objects.get_or_create(name=name)
"

# 5. Restart servers
./run_app.sh
```

---

**Most issues can be solved by checking logs and verifying both servers are running!**
