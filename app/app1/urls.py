from django.urls import path
# from .views import UserList
from .views import UserViewSet, InputViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('input', InputViewSet, basename='input')
urlpatterns = router.urls

# urlpatterns = [
#     path('users/', UserList.as_view()),
#     path('', views.main, name='main'),
#     path('get_comp/', views.get_company, name='get_company')
#
# ]
