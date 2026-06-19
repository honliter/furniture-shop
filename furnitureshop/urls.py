from django.contrib import admin
from django.urls import path
from store import views as store_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store_views.home, name='home'),
    path('login/', store_views.login_view, name='login'),
    path('register/', store_views.register_view, name='register'),
    path('logout/', store_views.logout_view, name='logout'),
    path('add-to-cart/<int:pk>/', store_views.add_to_cart, name='add_to_cart'),
    path('cart/', store_views.cart_view, name='cart'),
    path('checkout/', store_views.checkout_view, name='checkout'),
    path('super/add-furniture/', store_views.add_furniture_view, name='add_furniture'),
]
