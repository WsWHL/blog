from django.db import models


class UserInfo(models.Model):
    """用户信息"""
    Id = models.BigAutoField(primary_key=True, db_index=True)
    CheckKey = models.CharField(max_length=8)
    Password = models.CharField(max_length=256)
    UserName = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=50)
    Avatar = models.URLField(max_length=500)
    BgUrls = models.TextField()
    Birthday = models.DateField(null=True)
    Email = models.EmailField(unique=True, null=True, db_index=True)
    Phone = models.CharField(unique=True, null=True, max_length=20, db_index=True)
    Introduce = models.TextField(max_length=1000)
    Address = models.CharField(max_length=200)
    IP = models.GenericIPAddressField(protocol='both')
    IsEnable = models.BooleanField(default=True)
    Authorized = models.BooleanField(default=False)
    CreateTime = models.DateTimeField(null=False, auto_now_add=True)
    UpdateTime = models.DateTimeField(null=True)

    def __str__(self):
        return self.Email
