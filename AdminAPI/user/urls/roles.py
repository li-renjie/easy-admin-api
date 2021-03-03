from django.urls import path

from user import views

urlpatterns = [
    path('', views.RoleList.as_view()),
    path('/<int:id>', views.RoleDetail.as_view()),
    path('/<int:id>/users', views.RoleUserView.as_view()),
    path('/<int:role_id>/users/<int:user_id>', views.DeleteRoleUserView.as_view()),
    path('/<int:id>/permissions', views.RolePermissionView.as_view()),
    path('/<int:role_id>/permissions/<int:permission_id>', views.DeleteRolePermissionView.as_view()),
]
