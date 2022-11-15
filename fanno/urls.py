from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='f_home'),
    path('result/<str:pk>', views.solve, name='f_solver')
]