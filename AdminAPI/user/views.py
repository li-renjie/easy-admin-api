from django.views.generic.base import View
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from user.models import User, Role, Permission
from user.serializers import (
    UserSerializer, UserRoleSerializer, UserInfoSerializer,
    RoleSerializer, RoleUserSerializer, RolePermissionSerializer,
    PermissionSerializer
)


class CreateListMixin:
    """
    允许批量创建资源
    """
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)


class UserInfoView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserInfoSerializer(request.user)
            return JsonResponse(data=serializer.data)
        else:
            return JsonResponse(
                status=401,
                data={'detail': 'You are not logged in.'}
            )


class UpdatePasswordView(APIView):
    """用户本人有调用权限"""
    # permission_classes = [IsUser]

    def put(self, request, id):
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        user = User.objects.get(id=id)

        if not user:
            return JsonResponse(
                status=400,
                data={'detail': 'User not found.'}
            )

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return HttpResponse(status=201)
        else:
            return JsonResponse(
                status=400,
                data={'detail': 'Incorrect old password.'}
            )


class UserList(generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email']

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True    # support partial update on post
        return super().get_serializer(*args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     if 'password' not in request.data:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     super().create(request, *args, **kwargs)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRoleView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer

    def post(self, request, id):
        """Update user roles"""
        # user = User.objects.get(id=id)
        user = get_object_or_404(User, pk=id)
        role_ids = request.data['roles']    # { "roles": [2, 4, 6] }
        user.roles.set(role_ids)
        return Response(request.data, status=status.HTTP_201_CREATED)


class DeleteUserRoleView(APIView):

    def delete(self, request, user_id, role_id):
        user = get_object_or_404(User, pk=user_id)
        role = get_object_or_404(Role, pk=role_id)

        if role not in user.roles.all():
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        user.roles.remove(role)
        return Response(None, status=status.HTTP_200_OK)


class RoleList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleUserView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Role.objects.all()
    serializer_class = RoleUserSerializer

    def post(self, request, id):
        role = get_object_or_404(Role, pk=id)
        user_ids = request.data['users']    # { "users": [2, 4, 6] }
        role.users.set(user_ids)
        return Response(request.data, status=status.HTTP_201_CREATED)


class DeleteRoleUserView(APIView):

    def delete(self, request, role_id, user_id):
        role = get_object_or_404(Role, pk=role_id)
        user = get_object_or_404(User, pk=user_id)

        if user not in role.users.all():
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        role.users.remove(user)
        return Response(None, status=status.HTTP_200_OK)


class RolePermissionView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Role.objects.all()
    serializer_class = RolePermissionSerializer

    def post(self, request, id):
        role = get_object_or_404(Role, pk=id)
        permission_ids = request.data['permissions']
        role.permissions.set(permission_ids)
        return Response(request.data, status=status.HTTP_201_CREATED)


class DeleteRolePermissionView(APIView):

    def delete(self, request, role_id, permission_id):
        role = get_object_or_404(Role, pk=role_id)
        permission = get_object_or_404(Permission, pk=permission_id)

        if permission not in role.permissions.all():
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        role.permissions.remove(permission)
        return Response(None, status=status.HTTP_200_OK)


class PermissionList(CreateListMixin, generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
