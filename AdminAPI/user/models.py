from django.db import models


class User(models.Model):

    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=255, unique=True, verbose_name='姓名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.CharField(max_length=255, verbose_name='邮箱')
    mobile = models.CharField(max_length=15, null=True, verbose_name='手机')
    status = models.SmallIntegerField(default=0, verbose_name='状态，0:正常，1:冻结')
    role = models.ManyToManyField()

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class Role(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    role_name = models.CharField(max_length=255, unique=True, verbose_name='角色名')
    description = models.CharField(max_length=255, verbose_name='角色名')

    class Meta:
        db_table = 'role'
        verbose_name = '角色表'
        verbose_name_plural = verbose_name


class Permission(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')

    class Meta:
        db_table = 'permission'
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
