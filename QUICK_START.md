# Quick Start Guide

Get ShopHub up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages (if not already done)
pip install -r requirements.txt
```

## Step 2: Set Up Database

```bash
# Make sure your .env file has DATABASE_URL configured

# Run migrations
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser
```

## Step 3: Create Sample Categories

```bash
python manage.py shell
```

Then in the shell:
```python
from catalog.models import Category
Category.objects.create(name="Electronics")
Category.objects.create(name="Clothing")
Category.objects.create(name="Books")
Category.objects.create(name="Home & Garden")
exit()
```

## Step 4: Start the Application

### Easy Method (Recommended)
```bash
./run_app.sh
```

### Manual Method
**Terminal 1:**
```bash
python manage.py runserver
```

**Terminal 2:**
```bash
cd frontend
python server.py
```

## Step 5: Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:8080
- **Admin Panel**: http://localhost:8000/admin (if you created a superuser)

## What You Can Do

### As a Guest
1. Browse products (if any exist)
2. Search and filter
3. View product details
4. Add to cart

### As a Registered User
1. Click **"Register"** button
2. Fill in your details:
   - Username
   - Email
   - Password
3. Click Register (you'll be auto-logged in)
4. Now you can:
   - Click the **"+"** button (bottom right) to add products
   - View your products by clicking **"My Products"**
   - Edit or delete your own products
   - Complete checkout

## Creating Your First Product

1. **Login/Register** if not already
2. Click the **floating "+"** button (bottom right)
3. Fill in the form:
   - **Name**: "Awesome Laptop"
   - **Description**: "High-performance laptop for work and gaming"
   - **Price**: 999.99
   - **Category**: Electronics
   - **Stock**: 10
   - **Image URL**: (optional) Any image URL
4. Click **"Save Product"**
5. Your product will appear on the homepage!

## Testing the Full Flow

1. **Register** as User 1
2. **Add a product** (e.g., Laptop - $999)
3. **Logout**
4. **Register** as User 2
5. **Browse products** - you'll see User 1's laptop
6. **Add to cart**
7. **View cart** - check quantity, total
8. **Checkout** - complete the purchase

## Common Tasks

### Filter Products by Category
1. Click on the **category dropdown**
2. Select a category
3. Products will filter automatically

### Search for Products
1. Type in the **search box** at the top
2. Results update as you type (debounced)

### Sort Products
1. Use the **"Sort by"** dropdown
2. Options: Newest, Price (Low-High), Price (High-Low), Name (A-Z)

### Manage Your Products
1. Click **"My Products"** button
2. View all products you've created
3. Click any product to see details
4. Use **Edit** or **Delete** buttons

## Tips & Tricks

- **Keyboard Shortcut**: Press `Cmd/Ctrl + K` to focus the search bar
- **ESC Key**: Closes any open modal
- **Cart Badge**: Shows number of items in your cart
- **Stock Indicators**: Green = In Stock, Red = Out of Stock
- **Real-time Validation**: Forms validate as you type

## Troubleshooting

### "CORS error" in browser console
- Make sure django-cors-headers is installed
- Check settings.py has proper CORS configuration
- Restart Django server

### "Cannot connect to database"
- Check your .env file has DATABASE_URL
- Make sure PostgreSQL is running
- Verify database credentials

### "Port already in use"
```bash
# Kill the process using the port
lsof -ti:8000 | xargs kill -9  # For backend
lsof -ti:8080 | xargs kill -9  # For frontend
```

### Products not showing up
- Make sure you've created categories first
- Products need a valid category to be created
- Check the browser console for errors

## Next Steps

1. **Customize the design** - Edit `frontend/css/styles.css`
2. **Add more features** - Shopping wishlist, reviews, ratings
3. **Deploy** - Use Render, Heroku for backend; Netlify, Vercel for frontend
4. **Add images** - Implement image upload instead of URLs
5. **Add payments** - Integrate Stripe or PayPal

## Need Help?

- Check the full [PROJECT_README.md](PROJECT_README.md)
- Review the [frontend/README.md](frontend/README.md)
- Check Django logs in terminal
- Check browser console for frontend errors

---

**Happy coding! Enjoy building your e-commerce empire!**
