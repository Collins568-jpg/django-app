from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from cart.models import Cart
import uuid

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """Create order from cart"""
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                cart = Cart.objects.get(user=request.user)
                if not cart.items.exists():
                    return Response({
                        'error': 'Cart is empty'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                with transaction.atomic():
                    # Create order
                    order = Order.objects.create(
                        user=request.user,
                        order_number=f'ORD-{uuid.uuid4().hex[:8].upper()}',
                        total_amount=cart.total_price,
                        shipping_address=serializer.validated_data['shipping_address'],
                        shipping_city=serializer.validated_data['shipping_city'],
                        shipping_state=serializer.validated_data['shipping_state'],
                        phone_number=serializer.validated_data['phone_number'],
                    )
                    
                    # Create order items
                    for cart_item in cart.items.all():
                        # Check stock
                        if cart_item.product.stock < cart_item.quantity:
                            raise Exception(f'{cart_item.product.name} is out of stock')
                        
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.final_price
                        )
                        
                        # Update product stock
                        cart_item.product.stock -= cart_item.quantity
                        cart_item.product.save()
                    
                    # Clear cart
                    cart.items.all().delete()
                    
                    return Response({
                        'message': 'Order created successfully',
                        'order': OrderSerializer(order).data
                    }, status=status.HTTP_201_CREATED)
            
            except Cart.DoesNotExist:
                return Response({
                    'error': 'Cart not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)