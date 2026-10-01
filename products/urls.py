from django.urls import path
from .views import (products, cart, add_to_cart, remove_from_cart, increase_quantity, decrease_quantity,
                    checkout, order_success, my_orders, order_detail, admin_dashboard, update_order_status,
                    admin_order_detail)
urlpatterns = [
    path('products/',products,name='products'),
    path('cart/',cart,name='cart'),
    path('add_to_cart/<int:id>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:id>',remove_from_cart,name='remove_from_cart'),
    path('increase_quantity/<int:id>/',increase_quantity,name='increase_quantity'),
    path('decrease_quantity/<int:id>/',decrease_quantity,name='decrease_quantity'),
    path('checkout/',checkout,name='checkout'),
    path('order_success/<int:id>',order_success,name='order_success'),
    path('my_orders/',my_orders,name='my_orders'),
    path('order_detail/<int:id>',order_detail,name='order_detail'),
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('admin-dashboard/update-order/<int:order_id>/',update_order_status,name='update_order_status'),
    path('admin-dashboard/order/<int:order_id>/',admin_order_detail,name='admin_order_detail'
),
]