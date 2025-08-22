
from django.urls import path,include
from.import views
from django.conf import settings
from django.conf.urls.static import static
from .views import login

urlpatterns = [
    path('', views.flowerinfo, name='flower'),
    path('flower/<int:id>/', views.flower_detail, name='flower_detail'),
    path('buy/<int:id>/', views.buy_flower, name='buy_flower'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.orders_list, name='orders_list'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contactus/', views.contactus, name='contact'),
    path('supportus/', views.supportus, name='support'),
    path("login/", views.login, name="login"),
]










