from django.urls import path
from . import views


urlpatterns = [
    path('',views.store,name='store'),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name='checkout'),
    path('gotoCart/',views.gotoCart,name='gotoCart'),
    path('updatecart/',views.updatecart,name='updatecart'),
    path('gotocheckout/',views.gotocheckout,name='gotocheckout'),
    path('complete/',views.complete,name='complete'),
]
