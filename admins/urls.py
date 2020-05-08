from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('login/', views.login, name='login'),
    path('register/', views.register, name="register"),
    path('user/', views.userPage, name="user-page"),
    path('interuser/', views.interuserPage, name="inter-user-page"),
    path('admins/<int:id>/accept/', views.admin_accept, name='admin_accept'),
    path('admins/<int:id>/reject/', views.admin_reject, name='admin_reject')
]
