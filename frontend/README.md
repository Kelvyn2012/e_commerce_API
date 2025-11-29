# ShopHub Frontend

A modern, responsive e-commerce frontend built with vanilla JavaScript, HTML, and CSS.

## Features

- **Product Browsing**: View all products with beautiful card layouts
- **Advanced Filtering**: Search by name, filter by category, price range, and sort options
- **User Authentication**: Register and login functionality
- **Shopping Cart**: Add products to cart, manage quantities, and checkout
- **Product Management**: Authenticated users can create, edit, and delete their own products
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Real-time Updates**: Instant feedback and smooth animations

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid, Flexbox, and animations
- **Vanilla JavaScript**: No frameworks - pure JavaScript for maximum performance
- **REST API Integration**: Communicates with Django backend

## Getting Started

### Prerequisites

1. Make sure your Django backend is running on `http://localhost:8000`
2. Python 3.x installed

### Running the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the development server:
   ```bash
   python server.py
   ```

3. Open your browser and go to:
   ```
   http://localhost:8080
   ```

## Usage Guide

### As a Guest User
- Browse all products
- Search and filter products
- View product details
- Add items to cart (login required for checkout)

### As a Registered User
1. Click "Register" and create an account
2. Login with your credentials
3. Browse and purchase products
4. Click the "+" floating button to add your own products
5. Click "My Products" to view and manage your listings
6. Edit or delete your own products

## Project Structure

```
frontend/
├── index.html          # Main HTML file
├── css/
│   └── styles.css      # All styling
├── js/
│   ├── api.js          # API client and endpoints
│   ├── auth.js         # Authentication logic
│   ├── products.js     # Product management
│   ├── cart.js         # Shopping cart functionality
│   └── app.js          # Main app initialization
├── server.py           # Development server
└── README.md           # This file
```

## API Endpoints Used

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/products/` - List all products (with filters)
- `GET /api/products/:id/` - Get product details
- `POST /api/products/` - Create new product (auth required)
- `PUT /api/products/:id/` - Update product (auth required)
- `DELETE /api/products/:id/` - Delete product (auth required)
- `GET /api/categories/` - List all categories

## Keyboard Shortcuts

- `Cmd/Ctrl + K` - Focus search input
- `ESC` - Close any open modal

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Features Highlights

### Modern UI/UX
- Clean, intuitive interface
- Smooth animations and transitions
- Loading states and empty states
- Error handling with user-friendly messages

### Responsive Design
- Mobile-first approach
- Adapts to all screen sizes
- Touch-friendly interactions

### Performance
- Debounced search for better performance
- Lazy loading of images
- Minimal dependencies (vanilla JS)
- Optimized CSS

## Customization

You can easily customize the look and feel by modifying the CSS variables in `css/styles.css`:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --danger-color: #ef4444;
    /* ... more variables */
}
```

## Future Enhancements

- [ ] Order history for users
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced product image gallery
- [ ] Payment integration
- [ ] Progressive Web App (PWA) support
- [ ] Dark mode toggle

## License

MIT License
