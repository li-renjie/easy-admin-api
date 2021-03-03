from rest_framework import serializers
from user.models import User, Role, Permission
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all()
    )

    def validate_password(self, value):
        """Get encrypted password"""
        password = make_password(value)
        return password

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'mobile', 'is_active', 'roles',
            'create_time', 'update_time'
        ]
        read_only_fields = ['create_time', 'update_time']


class UserInfoSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'mobile', 'is_active',
            'roles', 'permissions'
        ]

    def get_permissions(self, user):
        perms = []
        roles = user.roles.all()
        for role in roles:
            for perm in role.permissions.all():
                if perm.id not in [item['id'] for item in perms]:
                    perms.append({
                        'id': perm.id,
                        'name': perm.name,
                        'action': perm.action,
                        'description': perm.description,
                    })
        return perms


class SimpleRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id', 'name', 'description'
        ]
        read_only_fields = ['name', 'description']


class UserRoleSerializer(serializers.ModelSerializer):
    roles = SimpleRoleSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'roles']
        read_only_fields = ['username']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id', 'name', 'description', 'create_time', 'update_time'
        ]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_active'
        ]


class RoleUserSerializer(serializers.ModelSerializer):
    users = SimpleUserSerializer(many=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'users']


class SimplePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id', 'name', 'action', 'description'
        ]


class RolePermissionSerializer(serializers.ModelSerializer):
    permissions = SimplePermissionSerializer(many=True)

    class Meta:
        model = Role
        fields = ['name', 'permissions']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id', 'name', 'action', 'description',
            'create_time', 'update_time'
        ]
        read_only_fields = ['create_time', 'update_time']

