from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'), 
    path('get_comp/', views.get_company, name='get_company')

]
