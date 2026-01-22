from django.urls import path
from . import api_views

app_name = 'accounts_api'

urlpatterns = [
    path('register/', api_views.register_user, name='register'),
    path('login/', api_views.login_user, name='login'),
    path('logout/', api_views.logout_user, name='logout'),
    path('profile/', api_views.user_profile, name='profile'),
]