from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('endpoint/', views.classify, name='endpoint'),
    path('method/<int:pk>/', views.method, name='view_method'),
    path('', views.api_method_list, name='api_list'),
]
