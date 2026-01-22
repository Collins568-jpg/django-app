# Django Jumia Clone - E-Commerce Platform

A comprehensive step-by-step guide to building a Jumia-inspired e-commerce platform using Django. This project is designed for students to learn Django while building a real-world application.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Step-by-Step Implementation](#step-by-step-implementation)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Project Overview

This Django Jumia Clone is a full-featured e-commerce platform that includes:
- User authentication and authorization
- Product catalog with categories
- Shopping cart functionality
- Order management system
- Payment integration
- Admin dashboard
- Search and filtering
- Reviews and ratings

**Learning Objectives:**
- Master Django MVT architecture
- Implement user authentication
- Work with Django ORM and database relationships
- Handle file uploads (product images)
- Implement REST APIs
- Learn payment gateway integration
- Deploy Django applications

## Features

### Phase 1: Core Features
- ✅ User registration and login
- ✅ Product listing and detail pages
- ✅ Category management
- ✅ Shopping cart
- ✅ Wishlist functionality

### Phase 2: Advanced Features
- ✅ Order processing
- ✅ Payment integration (Paystack/Flutterwave)
- ✅ Product reviews and ratings
- ✅ Search and filters
- ✅ Email notifications

### Phase 3: Premium Features
- ✅ Vendor dashboard
- ✅ Advanced analytics
- ✅ Discount coupons
- ✅ Real-time notifications

## Prerequisites

Before starting, ensure you have:
- Python 3.8+ installed
- pip (Python package manager)
- Virtual environment knowledge
- Basic understanding of HTML/CSS
- Git installed
- Code editor (VS Code recommended)

**Recommended Knowledge:**
- Python basics
- Django fundamentals
- SQL basics
- REST API concepts

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Dalyop/DJA_Project_1.git
cd DJA_Project_1
```

### 2. Create and Activate a Virtual Environment

Use a dedicated virtual environment to keep project dependencies isolated. The examples below use `.venv` as the environment folder (recommended), but you may name it `venv` if you prefer.

Windows (cmd.exe):
```cmd
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux (bash/zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

If you prefer not to activate the environment interactively, you can invoke the environment's Python directly: `.venv\Scripts\python` (Windows) or `.venv/bin/python` (macOS/Linux).

### 3. Install Dependencies

Install the pinned project dependencies from `requirements.txt`:

After activating the environment (or using the venv python directly):
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Note: The `requirements.txt` in this repository lists the main runtime libraries (Django, DRF, DB adapters, image handling, etc.). Adjust versions and add any extra packages you use for development or deployment.

### 4. Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=jumia_clone
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_PORT=3306

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Gateway
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
PAYSTACK_SECRET_KEY=your-paystack-secret-key
```

### 5. Database Setup
```bash
# Create MySQL database
mysql -u root -p #only when you have installed the terminal version of mysql
CREATE DATABASE jumia_clone;
exit;

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Load Sample Data (Optional)
```bash
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/products.json
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see your application!

## Project Structure

```
django-jumia-clone/
│
├── jumia_clone/              # Main project directory
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── accounts/                 # User authentication app
│   ├── models.py             # User models
│   ├── views.py              # Authentication views
│   ├── forms.py              # User forms
│   └── urls.py               # Account URLs
│
├── products/                 # Products app
│   ├── models.py             # Product, Category models
│   ├── views.py              # Product views
│   ├── admin.py              # Admin configuration
│   └── urls.py               # Product URLs
│
├── cart/                     # Shopping cart app
│   ├── models.py             # Cart models
│   ├── views.py              # Cart views
│   └── context_processors.py # Cart context
│
├── orders/                   # Order management app
│   ├── models.py             # Order models
│   ├── views.py              # Order views
│   └── tasks.py              # Background tasks
│
├── payments/                 # Payment integration app
│   ├── views.py              # Payment views
│   └── utils.py              # Payment helpers
│
├── static/                   # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                    # User uploaded files
│   └── products/
│
├── templates/                # HTML templates
│   ├── base.html
│   ├── home.html
│   └── products/
│
├── requirements.txt          # Project dependencies
├── manage.py                 # Django management script
└── README.md                 # This file
```

## Step-by-Step Implementation

### PHASE 1: PROJECT SETUP & USER AUTHENTICATION

#### Step 1: Install Django and Create Project
```bash
pip install django
django-admin startproject jumia_clone
cd jumia_clone
python manage.py startapp accounts
```

#### Step 2: Configure Settings (settings.py)
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
]

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Database configuration (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jumia_clone',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### Step 3: Create Custom User Model (accounts/models.py)
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return self.email
```

Update settings.py:
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

#### Step 4: Create Registration Form (accounts/forms.py)
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
```

#### Step 5: Create Authentication Views (accounts/views.py)
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
```

#### Step 6: Configure URLs (accounts/urls.py)
```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
```

### PHASE 2: PRODUCTS & CATEGORIES

#### Step 7: Create Products App
```bash
python manage.py startapp products
```

Add to INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    # ... other apps
    'products',
]
```

#### Step 8: Create Product Models (products/models.py)
```python
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    @property
    def final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - Image"
```

#### Step 9: Create Product Views (products/views.py)
```python
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

def home(request):
    featured_products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)
```

#### Step 10: Configure Product URLs (products/urls.py)
```python
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
```

### PHASE 3: SHOPPING CART

#### Step 11: Create Cart App
```bash
python manage.py startapp cart
```

Add to INSTALLED_APPS and create models (cart/models.py):
```python
from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):x
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id}"
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        return self.product.final_price * self.quantity
```

#### Step 12: Create Cart Views (cart/views.py)
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_detail(request):
    cart = get_or_create_cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart_detail.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:cart_detail')

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart:cart_detail')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('cart:cart_detail')
```

### PHASE 4: ORDERS & CHECKOUT

#### Step 13: Create Orders App
```bash
python manage.py startapp orders
```

Create models (orders/models.py):
```python
from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Shipping details
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        return self.price * self.quantity
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Products
- `GET /api/products/` - List all products
- `GET /api/products/<id>/` - Product detail
- `GET /api/categories/` - List categories

### Cart
- `GET /api/cart/` - View cart
- `POST /api/cart/add/` - Add to cart
- `PUT /api/cart/update/<id>/` - Update cart item
- `DELETE /api/cart/remove/<id>/` - Remove from cart

### Orders
- `POST /api/orders/create/` - Create order
- `GET /api/orders/` - List user orders
- `GET /api/orders/<id>/` - Order detail

## Testing

### Run Tests
```bash
python manage.py test
```

### Create Test Cases (products/tests.py)
```python
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
```

## Deployment

### Heroku Deployment
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Configure environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### AWS/DigitalOcean Deployment
1. Set up server with Ubuntu
2. Install Python, pip, nginx
3. Configure gunicorn
4. Set up SSL with Let's Encrypt
5. Configure static files serving

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [MySQL with Django](https://docs.djangoproject.com/en/stable/ref/databases/#mysql-notes)

## Support

For questions or issues:
- Create an issue on GitHub
- Email: devdalyop@gmail.com
## License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Happy Coding! 🚀**