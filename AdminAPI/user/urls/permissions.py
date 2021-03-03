from django.urls import path

from user import views

urlpatterns = [
    path('', views.PermissionList.as_view()),
    path('/<int:id>', views.PermissionDetail.as_view()),
]
