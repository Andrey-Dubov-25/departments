from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet

app_name = 'api'


router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='departments')

urlpatterns = [
    path('', include(router.urls))
]
