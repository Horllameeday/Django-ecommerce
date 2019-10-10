from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('cart/', views.CartView.as_view(), name='cart'),  
    path('add-to-cart/<int:pk>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<int:pk>', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('cash-checkout/', views.CashCheckoutView.as_view(), name='cash-checkout'),
    path('option/', views.OptionView.as_view(), name='option'),
    path('accounts/', include('django.contrib.auth.urls')),   
    path('signup/', views.signup, name='signup'),
]
