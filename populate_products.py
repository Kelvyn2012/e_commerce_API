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
        # Additional Electronics
        {
            "name": "Smartphone Case",
            "description": "Protective silicone case for smartphones",
            "price": Decimal("15.99"),
            "category": categories["Electronics"],
            "stock_quantity": 120,
            "image_url": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400",
        },
        {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with USB receiver",
            "price": Decimal("24.99"),
            "category": categories["Electronics"],
            "stock_quantity": 85,
            "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400",
        },
        {
            "name": "USB-C Cable",
            "description": "Fast charging USB-C cable, 6 feet long",
            "price": Decimal("12.99"),
            "category": categories["Electronics"],
            "stock_quantity": 200,
            "image_url": "https://images.unsplash.com/photo-1591290619762-f1daa1dbdbb5?w=400",
        },
        {
            "name": "Portable Power Bank",
            "description": "10000mAh portable charger for phones and tablets",
            "price": Decimal("32.99"),
            "category": categories["Electronics"],
            "stock_quantity": 65,
            "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400",
        },
        # Additional Clothing
        {
            "name": "Denim Jeans",
            "description": "Classic fit denim jeans, multiple sizes available",
            "price": Decimal("49.99"),
            "category": categories["Clothing"],
            "stock_quantity": 90,
            "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
        },
        {
            "name": "Winter Jacket",
            "description": "Warm insulated winter jacket with hood",
            "price": Decimal("89.99"),
            "category": categories["Clothing"],
            "stock_quantity": 45,
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        },
        {
            "name": "Running Socks Pack",
            "description": "Pack of 5 breathable athletic socks",
            "price": Decimal("16.99"),
            "category": categories["Clothing"],
            "stock_quantity": 150,
            "image_url": "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=400",
        },
        {
            "name": "Baseball Cap",
            "description": "Adjustable baseball cap with embroidered logo",
            "price": Decimal("22.99"),
            "category": categories["Clothing"],
            "stock_quantity": 110,
            "image_url": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400",
        },
        # Additional Books
        {
            "name": "Web Development Handbook",
            "description": "Complete guide to modern web development",
            "price": Decimal("42.99"),
            "category": categories["Books"],
            "stock_quantity": 55,
            "image_url": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400",
        },
        {
            "name": "Mystery Novel Collection",
            "description": "Bestselling mystery novels box set",
            "price": Decimal("29.99"),
            "category": categories["Books"],
            "stock_quantity": 40,
            "image_url": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400",
        },
        {
            "name": "Cookbook - Healthy Meals",
            "description": "150 healthy and delicious recipes",
            "price": Decimal("24.99"),
            "category": categories["Books"],
            "stock_quantity": 70,
            "image_url": "https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=400",
        },
        # Additional Home & Garden
        {
            "name": "Desk Lamp",
            "description": "LED desk lamp with adjustable brightness",
            "price": Decimal("34.99"),
            "category": categories["Home & Garden"],
            "stock_quantity": 60,
            "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400",
        },
        {
            "name": "Throw Pillow Set",
            "description": "Set of 2 decorative throw pillows",
            "price": Decimal("27.99"),
            "category": categories["Home & Garden"],
            "stock_quantity": 75,
            "image_url": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400",
        },
        {
            "name": "Wall Clock",
            "description": "Modern minimalist wall clock, 12 inch",
            "price": Decimal("19.99"),
            "category": categories["Home & Garden"],
            "stock_quantity": 50,
            "image_url": "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400",
        },
        {
            "name": "Garden Tool Set",
            "description": "5-piece gardening tool set with carrying bag",
            "price": Decimal("38.99"),
            "category": categories["Home & Garden"],
            "stock_quantity": 35,
            "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400",
        },
        # Additional Sports & Outdoors
        {
            "name": "Water Bottle",
            "description": "Stainless steel insulated water bottle, 32oz",
            "price": Decimal("21.99"),
            "category": categories["Sports & Outdoors"],
            "stock_quantity": 130,
            "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400",
        },
        {
            "name": "Resistance Bands Set",
            "description": "Set of 5 resistance bands for home workout",
            "price": Decimal("18.99"),
            "category": categories["Sports & Outdoors"],
            "stock_quantity": 95,
            "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400",
        },
        {
            "name": "Camping Tent",
            "description": "4-person waterproof camping tent",
            "price": Decimal("129.99"),
            "category": categories["Sports & Outdoors"],
            "stock_quantity": 20,
            "image_url": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400",
        },
        {
            "name": "Bicycle Helmet",
            "description": "Adjustable safety helmet for cycling",
            "price": Decimal("35.99"),
            "category": categories["Sports & Outdoors"],
            "stock_quantity": 55,
            "image_url": "https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=400",
        },
        # Additional Toys & Games
        {
            "name": "Board Game - Strategy",
            "description": "Family-friendly strategy board game for ages 8+",
            "price": Decimal("29.99"),
            "category": categories["Toys & Games"],
            "stock_quantity": 65,
            "image_url": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400",
        },
        {
            "name": "Puzzle 1000 Pieces",
            "description": "Challenging jigsaw puzzle with beautiful artwork",
            "price": Decimal("17.99"),
            "category": categories["Toys & Games"],
            "stock_quantity": 80,
            "image_url": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400",
        },
        {
            "name": "Art Supplies Kit",
            "description": "Complete art set with paints, brushes, and canvas",
            "price": Decimal("44.99"),
            "category": categories["Toys & Games"],
            "stock_quantity": 40,
            "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400",
        },
        # Additional Food & Beverages
        {
            "name": "Green Tea Bags",
            "description": "Organic green tea, box of 100 bags",
            "price": Decimal("11.99"),
            "category": categories["Food & Beverages"],
            "stock_quantity": 120,
            "image_url": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400",
        },
        {
            "name": "Dark Chocolate Bar",
            "description": "Premium 70% dark chocolate, 3.5oz",
            "price": Decimal("4.99"),
            "category": categories["Food & Beverages"],
            "stock_quantity": 200,
            "image_url": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=400",
        },
        {
            "name": "Protein Powder",
            "description": "Whey protein powder, vanilla flavor, 2lbs",
            "price": Decimal("34.99"),
            "category": categories["Food & Beverages"],
            "stock_quantity": 70,
            "image_url": "https://images.unsplash.com/photo-1579722821273-0f6c7d44362f?w=400",
        },
        {
            "name": "Honey Jar",
            "description": "Pure organic honey, 16oz glass jar",
            "price": Decimal("12.99"),
            "category": categories["Food & Beverages"],
            "stock_quantity": 90,
            "image_url": "https://images.unsplash.com/photo-1587049352846-4a222e784f4c?w=400",
        },
        # Additional Beauty & Personal Care
        {
            "name": "Shampoo & Conditioner Set",
            "description": "Sulfate-free shampoo and conditioner duo",
            "price": Decimal("23.99"),
            "category": categories["Beauty & Personal Care"],
            "stock_quantity": 100,
            "image_url": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400",
        },
        {
            "name": "Face Serum",
            "description": "Anti-aging vitamin C serum",
            "price": Decimal("31.99"),
            "category": categories["Beauty & Personal Care"],
            "stock_quantity": 60,
            "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400",
        },
        {
            "name": "Lip Balm Set",
            "description": "Pack of 3 moisturizing lip balms",
            "price": Decimal("9.99"),
            "category": categories["Beauty & Personal Care"],
            "stock_quantity": 150,
            "image_url": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=400",
        },
        {
            "name": "Bath Bombs Set",
            "description": "Luxurious bath bombs, set of 6",
            "price": Decimal("19.99"),
            "category": categories["Beauty & Personal Care"],
            "stock_quantity": 85,
            "image_url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400",
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
