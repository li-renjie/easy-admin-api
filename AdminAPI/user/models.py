from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self.create_user(username, password, **kwargs)


class User(AbstractBaseUser):

    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=255, unique=True, verbose_name='姓名')
    # password = models.CharField(max_length=255, verbose_name='密码')
    email = models.CharField(max_length=255, verbose_name='邮箱')
    mobile = models.CharField(max_length=15, null=True, verbose_name='手机')
    status = models.SmallIntegerField(default=0, verbose_name='状态，0:正常，1:冻结')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    is_active = models.BooleanField(default=True, verbose_name="激活状态")
    is_staff = models.BooleanField(default=True, verbose_name="是否是员工")
    is_superuser = models.BooleanField(default=False, verbose_name="是否超级用户")
    roles = models.ManyToManyField(to='Role', blank=True, related_name='users')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Role(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='角色名')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='角色描述')
    permissions = models.ManyToManyField(to='Permission')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class Permission(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='权限名')
    action = models.CharField(max_length=255, verbose_name='动作')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='权限描述')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '%s:%s' % (self.name, self.action)

    class Meta:
        db_table = 'permission'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
