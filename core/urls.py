from django.urls import path
from django.contrib import admin
from .views import  (
CheckoutView,
ItemDetailView,
#HomeView,
add_to_cart,
OrderSummaryView,
remove_from_cart,
remove_single_item_from_cart,
home
)




app_name = 'core'

urlpatterns = [
    #path('', HomeView.as_view(), name='home'),
    path('', home, name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
]
