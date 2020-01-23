from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('detail/<slug>', views.ItemDetailView.as_view(), name='detail'),
    path('<int:pk>', views.category_view, name='category'),
    path('cart/', views.CartView.as_view(), name='cart'),  
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('cash-checkout/', views.CashCheckoutView.as_view(), name='cash-checkout'),
    path('option/', views.OptionView.as_view(), name='option'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
    path('accounts/', include('django.contrib.auth.urls')),   
    path('signup/', views.signup, name='signup'),
]
