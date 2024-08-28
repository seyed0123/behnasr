from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('product/<int:pk>/', views.view_product, name='view_product')
]
