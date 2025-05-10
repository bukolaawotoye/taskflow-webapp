from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout_user', views.logout_user, name='logout_user'),
]