from django.urls import path
from . import views

urlpatterns = [
    path('', views.window1_view, name='window1'),
    path('window1/', views.window1_view, name='window1'),
    path('window2/', views.window2_view, name='window2'),
    path('api/users/', views.user_list, name='user-list'),
    path('api/users/<int:pk>/', views.user_detail, name='user-detail'),
]

