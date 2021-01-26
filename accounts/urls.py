from django.urls import path, reverse_lazy

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('register/', views.register_user, name='register_user'),
    path('userdetails/', views.add_user_details,
         {'next': None}, name='add_user_details'),
    path('shippingdetails/', views.add_user_details,
         {'next': 'checkout:check_out'}, name='shipping_details'),
    path('profile/', views.user_profile, name='user_profile'),
    path('order/<order_number>', views.view_order, name='view_order'),
    path('userupdate/', views.update_user, name='update_user'),
]
