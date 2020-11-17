from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('', views.index, name='index'),
# ]

urlpatterns = []

router = DefaultRouter()
router.register('students', views.StudentViewSet)

urlpatterns += router.urls
