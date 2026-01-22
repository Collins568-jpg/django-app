from django.test import TestCase
from .models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            price=1000.00,
            stock=10
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Laptop')
        self.assertEqual(self.product.price, 1000.00)