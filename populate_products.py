"""
Django script to populate Product and Category models with sample data.

Usage:
    python manage.py shell < populate_products.py

    Or place in a Django management command:
    python manage.py populate_products
"""

# Setup Django environment (uncomment if running as standalone script)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
# django.setup()

from django.contrib.auth import get_user_model
from decimal import Decimal

# Import your models (adjust the import path to match your app structure)
from catalog.models import Category, Product

User = get_user_model()


def create_categories():
    """Create sample categories"""
    categories_data = [
        "Electronics",
        "Clothing",
        "Books",
        "Home & Garden",
        "Sports & Outdoors",
        "Toys & Games",
        "Food & Beverages",
        "Beauty & Personal Care",
    ]

    categories = []
    for cat_name in categories_data:
        category, created = Category.objects.get_or_create(name=cat_name)
        categories.append(category)
        if created:
            print(f"Created category: {cat_name}")
        else:
            print(f"Category already exists: {cat_name}")

    return categories


def create_products(owner):
    """Create sample products"""
    categories = {cat.name: cat for cat in Category.objects.all()}

    products_data = [
        {
            "name": "Wireless Bluetooth Headphones",
            "description": "High-quality wireless headphones with noise cancellation",
            "price": Decimal("79.99"),
            "category": categories["Electronics"],
            "stock_quantity": 50,
            "image_url": "https://example.com/images/headphones.jpg",
        },
        {
            "name": "Cotton T-Shirt",
            "description": "Comfortable 100% cotton t-shirt available in multiple colors",
            "price": Decimal("19.99"),
            "category": categories["Clothing"],
            "stock_quantity": 200,
            "image_url": "https://example.com/images/tshirt.jpg",
        },
        {
            "name": "Python Programming Guide",
            "description": "Comprehensive guide to Python programming for beginners",
            "price": Decimal("34.99"),
            "category": categories["Books"],
            "stock_quantity": 75,
            "image_url": "https://example.com/images/python-book.jpg",
        },
        {
            "name": "Indoor Plant Pot Set",
            "description": "Set of 3 ceramic plant pots with drainage holes",
            "price": Decimal("24.99"),
            "category": categories["Home & Garden"],
            "stock_quantity": 40,
            "image_url": "https://example.com/images/plant-pots.jpg",
        },
        {
            "name": "Yoga Mat",
            "description": "Non-slip yoga mat with carrying strap",
            "price": Decimal("29.99"),
            "category": categories["Sports & Outdoors"],
            "stock_quantity": 100,
            "image_url": "https://example.com/images/yoga-mat.jpg",
        },
        {
            "name": "Building Blocks Set",
            "description": "Educational building blocks for children ages 3+",
            "price": Decimal("39.99"),
            "category": categories["Toys & Games"],
            "stock_quantity": 60,
            "image_url": "https://example.com/images/blocks.jpg",
        },
        {
            "name": "Organic Coffee Beans",
            "description": "Premium organic coffee beans, medium roast",
            "price": Decimal("14.99"),
            "category": categories["Food & Beverages"],
            "stock_quantity": 150,
            "image_url": "https://example.com/images/coffee.jpg",
        },
        {
            "name": "Natural Face Moisturizer",
            "description": "Hydrating face moisturizer with natural ingredients",
            "price": Decimal("26.99"),
            "category": categories["Beauty & Personal Care"],
            "stock_quantity": 80,
            "image_url": "https://example.com/images/moisturizer.jpg",
        },
        {
            "name": "Laptop Stand",
            "description": "Adjustable aluminum laptop stand for ergonomic viewing",
            "price": Decimal("44.99"),
            "category": categories["Electronics"],
            "stock_quantity": 35,
            "image_url": "https://example.com/images/laptop-stand.jpg",
        },
        {
            "name": "Running Shoes",
            "description": "Lightweight running shoes with cushioned sole",
            "price": Decimal("89.99"),
            "category": categories["Sports & Outdoors"],
            "stock_quantity": 45,
            "image_url": "https://example.com/images/running-shoes.jpg",
        },
    ]

    created_count = 0
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data["name"],
            owner=owner,
            defaults={
                "description": product_data["description"],
                "price": product_data["price"],
                "category": product_data["category"],
                "stock_quantity": product_data["stock_quantity"],
                "image_url": product_data["image_url"],
            },
        )
        if created:
            created_count += 1
            print(f"Created product: {product.name}")
        else:
            print(f"Product already exists: {product.name}")

    print(f"\nTotal products created: {created_count}")


def populate():
    """Main function to populate the database"""
    print("Starting database population...\n")

    # Get or create a default owner
    owner, created = User.objects.get_or_create(
        username="admin",
        defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True},
    )

    if created:
        owner.set_password("admin123")
        owner.save()
        print(f"Created default owner: {owner.username}")
    else:
        print(f"Using existing owner: {owner.username}")

    print("\n--- Creating Categories ---")
    create_categories()

    print("\n--- Creating Products ---")
    create_products(owner)

    print("\n✓ Database population completed!")
    print(f"Total categories: {Category.objects.count()}")
    print(f"Total products: {Product.objects.count()}")


if __name__ == "__main__":
    populate()
