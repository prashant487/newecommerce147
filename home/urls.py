from django.contrib import admin
from django.urls import path
from .views import *
app_name = 'home'
urlpatterns = [
    path('', HomeVIew.as_view(), name='home'),
    path('product/<slug>', ProductDetailView.as_view(), name='product'),
    path('search', SearchView.as_view(), name='search'),
    path('category/<slug>', CategoryView.as_view(), name='category'),
    path('signup', register, name='signup'),
    path('signin', signin, name='signin'),
    path('mycart',ViewCart.as_view(),name = 'mycart'),
    path('add-to-cart/<slug>',cart,name = 'add-to-cart'),
    path('delete-cart/<slug>',deletecart,name = 'delete-cart'),
    path('minus-cart/<slug>', minusitem, name='minus-cart'),
    path('grand-total/<slug>', grand_total, name='grand-total'),
    path('brand/<name>', BrandView.as_view(), name='brand'),
    path('contact', contact, name='contact'),
    ]
































































