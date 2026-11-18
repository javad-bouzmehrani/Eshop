"""
URL configuration for online_shop_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from online_shop_back import settings
from online_shop_back.views import home_page , header , footer , login_view , log_out
from eshop_products.views import ProductlistView, product_detail, SearchProduct, ProductlistView_category
from eshop_order.views import  add_new_order, cart_detail , remove_card_item
from eshop_profile.views import profile , edit_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page , name='home'),
    path('header', header , name='header'),
    path('footer', footer , name='footer'),
    path('auth', login_view , name='login_register'),
    path('logout', log_out , name='Logout'),

    path('products',ProductlistView.as_view() , name='produts_list'),
    path('product_detail/<product_id>/<title>',product_detail , name='product_detail'),
    path('products/search', SearchProduct.as_view(), name='search'),
    path('products/<category_name>', ProductlistView_category.as_view(),name="product_by_category"),
    path('order',cart_detail , name='order_page'),
    path('add_new_order',add_new_order),
    path('remove_item/<order_id>',remove_card_item , name='remove_card_item'),
    path('profile',profile , name='profile'),
    path('edit_profile',edit_profile , name='edit_profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)