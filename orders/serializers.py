from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user_email', 'total_amount', 'status',
                  'shipping_address', 'shipping_city', 'shipping_state', 
                  'phone_number', 'items', 'created_at', 'updated_at']
        read_only_fields = ['order_number', 'total_amount']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['shipping_address', 'shipping_city', 'shipping_state', 'phone_number']