from django.db import models


class User(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=255, unique=True, verbose_name='姓名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.CharField(max_length=255, verbose_name='邮箱')
    mobile = models.CharField(max_length=15, null=True, verbose_name='手机')
    status = models.SmallIntegerField(default=0, verbose_name='状态，0:正常，1:冻结')
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    role = models.ManyToManyField(to='Role')

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class Role(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    role_name = models.CharField(max_length=255, unique=True, verbose_name='角色名')
    description = models.CharField(max_length=255, verbose_name='角色名')
    permission = models.ManyToManyField(to='Permission')
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'role'
        verbose_name = '角色表'
        verbose_name_plural = verbose_name


class Permission(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=255, unique=True, verbose_name='权限名')
    action = models.CharField(max_length=255, verbose_name='动作')
    description = models.CharField(max_length=255, null=True, verbose_name='权限描述')
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'permission'
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
