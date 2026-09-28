import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from products.models import FoodCategory, Product
from inventory.models import InventoryItem

user, created = User.objects.get_or_create(
    email='demo@foodguard.com',
    defaults={
        'username': 'demo@foodguard.com',
        'first_name': 'Demo',
        'last_name': 'User',
        'is_active': True,
        'is_staff': True,
        'is_superuser': True,
    }
)
user.set_password('Password1234!')
user.is_active = True
user.save()

cat_dairy, _ = FoodCategory.objects.get_or_create(name='Dairy', defaults={'slug': 'dairy', 'description': 'Milk, yogurt, cheese'})
cat_produce, _ = FoodCategory.objects.get_or_create(name='Produce', defaults={'slug': 'produce', 'description': 'Fresh fruits and vegetables'})
cat_pantry, _ = FoodCategory.objects.get_or_create(name='Pantry', defaults={'slug': 'pantry', 'description': 'Dry goods and canned food'})
cat_bakery, _ = FoodCategory.objects.get_or_create(name='Bakery', defaults={'slug': 'bakery', 'description': 'Bread and baked goods'})

p_milk, _ = Product.objects.get_or_create(name='Organic Whole Milk', defaults={'brand': 'Organic Valley', 'category': cat_dairy, 'shelf_life_days': 14, 'storage_instructions': 'Keep refrigerated'})
p_yogurt, _ = Product.objects.get_or_create(name='Greek Yogurt', defaults={'brand': 'Chobani', 'category': cat_dairy, 'shelf_life_days': 21, 'storage_instructions': 'Keep refrigerated'})
p_spinach, _ = Product.objects.get_or_create(name='Baby Spinach', defaults={'brand': 'Earthbound Farm', 'category': cat_produce, 'shelf_life_days': 10, 'storage_instructions': 'Keep in crisper drawer'})
p_sauce, _ = Product.objects.get_or_create(name='Tomato Basil Pasta Sauce', defaults={'brand': 'Rao\'s Homemade', 'category': cat_pantry, 'shelf_life_days': 180, 'storage_instructions': 'Store in cool dry place'})
p_bread, _ = Product.objects.get_or_create(name='Artisan Sourdough Bread', defaults={'brand': 'Local Bakery', 'category': cat_bakery, 'shelf_life_days': 7, 'storage_instructions': 'Store sealed at room temp'})

today = date.today()

items_data = [
    (p_milk, 1, 'bottle', today - timedelta(days=10), today + timedelta(days=3), InventoryItem.Storage.FRIDGE, InventoryItem.Status.ACTIVE),
    (p_yogurt, 2, 'cups', today - timedelta(days=15), today + timedelta(days=1), InventoryItem.Storage.FRIDGE, InventoryItem.Status.ACTIVE),
    (p_spinach, 1, 'box', today - timedelta(days=2), today + timedelta(days=7), InventoryItem.Storage.FRIDGE, InventoryItem.Status.ACTIVE),
    (p_sauce, 3, 'jars', today - timedelta(days=20), today + timedelta(days=60), InventoryItem.Storage.PANTRY, InventoryItem.Status.ACTIVE),
    (p_bread, 1, 'loaf', today - timedelta(days=8), today - timedelta(days=1), InventoryItem.Storage.PANTRY, InventoryItem.Status.ACTIVE),
]

for prod, qty, unit, purchased, expires, loc, status in items_data:
    InventoryItem.objects.get_or_create(
        user=user,
        product=prod,
        expires_on=expires,
        defaults={
            'quantity': qty,
            'unit': unit,
            'purchased_on': purchased,
            'storage_location': loc,
            'status': status,
            'notes': 'Demo stock',
        }
    )

print('SUCCESS: Demo user created with email demo@foodguard.com and password Password1234!')
print('Inventory count:', InventoryItem.objects.filter(user=user).count())
