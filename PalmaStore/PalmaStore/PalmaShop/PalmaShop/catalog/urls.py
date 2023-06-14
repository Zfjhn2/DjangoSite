from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^products/$', views.ProductListView.as_view(), name='product'),
    re_path(r'^product/(?P<product_id>\d+)$', views.product_detail, name='product-detail'),
    re_path(r'^manufacturers/$', views.ManufacturerListView.as_view(), name='manufacturer'),
    re_path(r'^manufacturer/(?P<pk>\d+)$', views.ManufacturerDetailView.as_view(), name='manufacturer-detail'),
    path('search/', views.search, name="search"),
    path('products/filterfootwear/', views.filter_footwear, name="filter_footwear"),
    path('products/filterpants/', views.filter_pants, name="filter_pants"),
    path('products/filterouterwear/', views.filter_outerwear, name="filter_outerwear"),
    path('account/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/welcome/', views.account, name='welcome'),
    re_path(r'^product/add_to_cart/(?P<product_id>\d+)$', views.add_to_cart, name='add_to_cart'),
    path('account/buy_order/', views.buy_order, name='buy_order'),
    re_path(r'^account/(?P<product_id>\d+)$', views.remove_from_cart, name='remove_from_cart'),
    path('contacts/', views.contacts, name='contacts'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
