from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
from products.models import Product

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    def list(self, request):
        """Get user's cart"""
        cart = self.get_cart()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add item to cart"""
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            try:
                product = Product.objects.get(id=product_id, available=True)
            except Product.DoesNotExist:
                return Response({
                    'error': 'Product not found or unavailable'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check stock
            if product.stock < quantity:
                return Response({
                    'error': f'Only {product.stock} items available'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            cart = self.get_cart()
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock:
                    return Response({
                        'error': f'Only {product.stock} items available'
                    }, status=status.HTTP_400_BAD_REQUEST)
                cart_item.save()
            
            return Response({
                'message': 'Item added to cart',
                'cart': CartSerializer(cart).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'], url_path='update/(?P<item_id>[^/.]+)')
    def update_item(self, request, item_id=None):
        """Update cart item quantity"""
        try:
            cart = self.get_cart()
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            
            quantity = request.data.get('quantity', 1)
            quantity = int(quantity)
            
            if quantity < 1:
                return Response({
                    'error': 'Quantity must be at least 1'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if quantity > cart_item.product.stock:
                return Response({
                    'error': f'Only {cart_item.product.stock} items available'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return Response({
                'message': 'Cart updated',
                'cart': CartSerializer(cart).data
            })
        
        except CartItem.DoesNotExist:
            return Response({
                'error': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['delete'], url_path='remove/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """Remove item from cart"""
        try:
            cart = self.get_cart()
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            
            return Response({
                'message': 'Item removed from cart',
                'cart': CartSerializer(cart).data
            })
        
        except CartItem.DoesNotExist:
            return Response({
                'error': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear entire cart"""
        cart = self.get_cart()
        cart.items.all().delete()
        return Response({
            'message': 'Cart cleared'
        })