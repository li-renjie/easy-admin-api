from django.urls import path
from user import views


urlpatterns = [
    path('', views.UserList.as_view()),
    path('/<int:id>', views.UserDetail.as_view()),
    path('/<int:id>/roles', views.UserRoleView.as_view()),
    path('/<int:user_id>/roles/<int:role_id>', views.DeleteUserRoleView.as_view()),
    path('/<int:id>/password', views.UpdatePasswordView.as_view()),
]
