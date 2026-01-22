from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet, basename='product')
router.register(r'categories', api_views.CategoryViewSet, basename='category')

app_name = 'products_api'

urlpatterns = [
    path('', include(router.urls)),
]