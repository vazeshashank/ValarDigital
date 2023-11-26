from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cusDash',views.home,name='home'),
    path('login',views.loginPage,name='login'),
    path('register',views.registerPage,name='register'),
    path('custReg',views.custReg,name='custReg'),
    path('custLog',views.custLog,name='custLog'),
    path('vendReg',views.vendReg,name='vendReg'),
    path('vendLog',views.vendLog,name='vendLog'),
    path('logout',views.logoutPage,name='logout'),
    path('venDash',views.vendor_dashboard,name='venDash'),
    path('',views.customer_dashboard,name='cusDash'),
    path('myProds',views.myProds,name='myProds'),
    path('test',views.test,name='test'),
    path('addProd',views.add_product,name='addProd'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart', views.view_cart, name='view_cart'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]




