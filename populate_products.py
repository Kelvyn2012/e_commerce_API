"""
Django script to populate Product and Category models with sample data.

Usage:
    python manage.py shell < populate_products.py

    Or place in a Django management command:
    python manage.py populate_products
"""

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
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        },
        {
            "name": "Cotton T-Shirt",
            "description": "Comfortable 100% cotton t-shirt available in multiple colors",
            "price": Decimal("19.99"),
            "category": categories["Clothing"],
            "stock_quantity": 200,
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
        },
        {
            "name": "Python Programming Guide",
            "description": "Comprehensive guide to Python programming for beginners",
            "price": Decimal("34.99"),
            "category": categories["Books"],
            "stock_quantity": 75,
            "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
        },
        {
            "name": "Indoor Plant Pot Set",
            "description": "Set of 3 ceramic plant pots with drainage holes",
            "price": Decimal("24.99"),
            "category": categories["Home & Garden"],
            "stock_quantity": 40,
            "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400",
        },
        {
            "name": "Yoga Mat",
            "description": "Non-slip yoga mat with carrying strap",
            "price": Decimal("29.99"),
            "category": categories["Sports & Outdoors"],
            "stock_quantity": 100,
            "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400",
        },
        {
            "name": "Building Blocks Set",
            "description": "Educational building blocks for children ages 3+",
            "price": Decimal("39.99"),
            "category": categories["Toys & Games"],
            "stock_quantity": 60,
            "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400",
        },
        {
            "name": "Organic Coffee Beans",
            "description": "Premium organic coffee beans, medium roast",
            "price": Decimal("14.99"),
            "category": categories["Food & Beverages"],
            "stock_quantity": 150,
            "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400",
        },
        {
            "name": "Natural Face Moisturizer",
            "description": "Hydrating face moisturizer with natural ingredients",
            "price": Decimal("26.99"),
            "category": categories["Beauty & Personal Care"],
            "stock_quantity": 80,
            "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400",
        },
        {
            "name": "Laptop Stand",
            "description": "Adjustable aluminum laptop stand for ergonomic viewing",
            "price": Decimal("44.99"),
            "category": categories["Electronics"],
            "stock_quantity": 35,
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",
        },
        {
            "name": "Running Shoes",
            "description": "Lightweight running shoes with cushioned sole",
            "price": Decimal("89.99"),
            "category": categories["Sports & Outdoors"],
            "stock_quantity": 45,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
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
