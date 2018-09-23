import django
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    """用户管理"""

    def create_user(self, email, ip, password=None):
        if not email:
            raise ValueError('用户必须拥有邮箱地址')

        user = self.model(
            email=self.normalize_email(email),
            ip=ip
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser):
    """用户信息"""
    id = models.BigAutoField(unique=True, primary_key=True, db_index=True)
    username = models.CharField(max_length=150, unique=True, null=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True, blank=True, max_length=254, null=True,
                              validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])
    first_name = models.CharField(blank=True, max_length=30)
    last_name = models.CharField(blank=True, max_length=150)
    last_login = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    avatar = models.URLField(max_length=500)
    bg_urls = models.TextField()
    birthday = models.DateField(null=True)
    phone = models.CharField(unique=True, null=True, max_length=20, db_index=True)
    introduce = models.TextField(max_length=1000)
    address = models.CharField(max_length=200)
    ip = models.GenericIPAddressField(protocol='both')
    is_enable = models.BooleanField(default=True)
    authorized = models.BooleanField(default=False)
    create_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=True)
    groups = models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.Group')
    user_permissions = models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user',
                                              to='auth.Permission')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()


def __str__(self):
    return self.email
