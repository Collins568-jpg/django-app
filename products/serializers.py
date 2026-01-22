from rest_framework import serializers
from .models import Product, Category, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'product_count', 'created_at']
    
    def get_product_count(self, obj):
        return obj.products.count()

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_at']

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'discount_price', 
                  'final_price', 'category_name', 'image', 'stock', 'available']

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 
                  'discount_price', 'final_price', 'category', 'image', 
                  'images', 'stock', 'available', 'created_at', 'updated_at']