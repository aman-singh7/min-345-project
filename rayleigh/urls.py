from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='r_home'),
    path('result/<str:pk>', views.solve, name='r_solver')
]