from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ocr/', views.post_ocr, name='ocr_endpoint'),
    path('classify/', views.post_classify, name='classify_endpoint'),
    path('method/<int:pk>/', views.method, name='view_method'),
    path('', views.api_method_list, name='api_list'),
    path('set-language/<str:lang>/', views.active_language, name='set_language'),
    path('demo/', views.demo_page, name='demo_page'),
    path('api_param/', views.get_api_param, name='get_api_param'),
]
