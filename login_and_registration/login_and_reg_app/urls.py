from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new_user', views.new_user),
    path('login', views.login),
    path('sucessful_login', views.sucessful_login),
    path('logout', views.logout),
]