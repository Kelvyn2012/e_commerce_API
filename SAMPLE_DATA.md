# Sample Data Reference

## Demo User Account

For testing purposes, a demo user has been created:

**Username:** `shopkeeper`
**Password:** `demo123`
**Email:** `shopkeeper@shophub.com`

All 20 sample products are owned by this user.

## Products by Category

### 🔌 Electronics (4 products)

| Product | Price | Stock | Image |
|---------|-------|-------|-------|
| Wireless Bluetooth Headphones | $149.99 | 45 | ✅ |
| Smart Watch Pro | $299.99 | 30 | ✅ |
| Laptop Computer 15.6 inch | $899.99 | 15 | ✅ |
| Wireless Charging Pad | $29.99 | 100 | ❌ |

**Features:**
- Premium noise-cancelling headphones
- Fitness tracking smartwatch
- Powerful laptop for work and gaming
- Fast wireless charging technology

---

### 👕 Clothing (4 products)

| Product | Price | Stock | Image |
|---------|-------|-------|-------|
| Classic Denim Jacket | $79.99 | 60 | ✅ |
| Cotton T-Shirt Pack (3) | $34.99 | 120 | ✅ |
| Running Sneakers | $89.99 | 75 | ✅ |
| Leather Belt | $39.99 | 0 | ❌ |

**Features:**
- Timeless denim fashion
- 3-pack premium cotton tees
- Athletic shoes with superior cushioning
- **OUT OF STOCK** - Genuine leather belt

---

### 📚 Books (4 products)

| Product | Price | Stock | Image |
|---------|-------|-------|-------|
| The Art of Programming | $49.99 | 35 | ✅ |
| Mindful Living | $24.99 | 50 | ✅ |
| Cooking Made Easy | $29.99 | 40 | ❌ |
| Science Fiction Trilogy Box Set | $59.99 | 25 | ✅ |

**Features:**
- Software development guide
- Meditation and mindfulness
- 200+ delicious recipes
- Epic space adventure trilogy

---

### 🏡 Home & Garden (4 products)

| Product | Price | Stock | Image |
|---------|-------|-------|-------|
| Indoor Plant Collection (5 plants) | $44.99 | 55 | ✅ |
| Aromatherapy Diffuser | $34.99 | 80 | ✅ |
| Kitchen Knife Set (8 pieces) | $99.99 | 42 | ❌ |
| Throw Pillow Set (4) | $39.99 | 95 | ✅ |

**Features:**
- Low-maintenance indoor plants
- Ultrasonic essential oil diffuser
- Professional-grade knife set
- Modern geometric cushion covers

---

### ⚽ Sports (4 products)

| Product | Price | Stock | Image |
|---------|-------|-------|-------|
| Yoga Mat Premium | $34.99 | 70 | ✅ |
| Adjustable Dumbbells Set | $249.99 | 20 | ✅ |
| Basketball Official Size | $29.99 | 65 | ✅ |
| Water Bottle 32oz | $24.99 | 150 | ❌ |

**Features:**
- Extra thick non-slip yoga mat
- 5-50 lbs adjustable dumbbells
- Regulation size basketball
- Insulated stainless steel bottle

---

## Product Statistics

- **Total Products:** 20
- **Total Value:** $1,679.79
- **Average Price:** $83.99
- **In Stock Items:** 19
- **Out of Stock Items:** 1 (Leather Belt)
- **Total Stock Units:** 1,362

## Price Range by Category

| Category | Lowest | Highest | Average |
|----------|--------|---------|---------|
| Electronics | $29.99 | $899.99 | $344.99 |
| Clothing | $34.99 | $89.99 | $61.24 |
| Books | $24.99 | $59.99 | $41.24 |
| Home & Garden | $34.99 | $99.99 | $54.74 |
| Sports | $24.99 | $249.99 | $84.99 |

## Testing Scenarios

### Scenario 1: Browse and Filter
1. Open http://localhost:8080
2. Select "Electronics" from category filter
3. See 4 electronics products
4. Change to "Sports" - see 4 sports products

### Scenario 2: Search
1. Type "book" in search box
2. See basketball and books
3. Type "bluetooth" - see headphones
4. Clear search to see all products

### Scenario 3: Price Filtering
1. Set Min Price: 30, Max Price: 50
2. See 8 products in that range
3. Sort by "Price: Low to High"
4. Verify order is correct

### Scenario 4: Shopping Cart
1. Click on "Wireless Bluetooth Headphones"
2. Click "Add to Cart"
3. Click Cart button (shows badge "1")
4. Adjust quantity to 2
5. Total should be $299.98

### Scenario 5: Out of Stock
1. Filter by "Clothing"
2. Find "Leather Belt"
3. Click to view details
4. Notice "Out of Stock" badge
5. "Add to Cart" button should be disabled

### Scenario 6: Product Management (as shopkeeper)
1. Login with shopkeeper/demo123
2. Click any product
3. See "Edit" and "Delete" buttons
4. Try editing a product
5. Try creating a new product

### Scenario 7: New User Experience
1. Click "Register"
2. Create account: username=`testuser`, email=`test@test.com`, password=`test123`
3. Auto-logged in after registration
4. Click "+" to add a product
5. Your product appears in the list
6. Click "My Products" to see only yours

## API Endpoints with Sample Data

### Get All Products
```bash
curl http://localhost:8000/api/products/
```

### Get Single Product
```bash
curl http://localhost:8000/api/products/1/
```

### Filter by Category
```bash
curl http://localhost:8000/api/products/?category=electronics
```

### Price Range Filter
```bash
curl http://localhost:8000/api/products/?price_min=20&price_max=50
```

### Search
```bash
curl http://localhost:8000/api/products/?search=headphones
```

### Sort by Price
```bash
curl http://localhost:8000/api/products/?ordering=price
```

## Image URLs

Products with images use Unsplash URLs:
- High-quality, free stock photos
- Automatically optimized for web
- Some products intentionally have no images (shows emoji placeholders)

## Notes

- Product images are hosted on Unsplash (external URLs)
- Some products intentionally have no image to show the placeholder UI
- The "Leather Belt" is out of stock to demonstrate that functionality
- All products have realistic descriptions and pricing
- Stock quantities vary to show different inventory levels

## Resetting Sample Data

To recreate all sample products:

```bash
python manage.py shell
```

```python
from catalog.models import Product
Product.objects.all().delete()
# Then run the product creation script again
```

Or to delete just demo user's products:

```python
from users.models import User
shopkeeper = User.objects.get(username='shopkeeper')
Product.objects.filter(owner=shopkeeper).delete()
```

---

**Your application is fully populated and ready to demonstrate!**
