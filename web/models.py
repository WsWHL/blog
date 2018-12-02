import django
from django.utils import timezone
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

    def get_deleted_user_id(self):
        user = self.model().objects.get(username='delete')
        if user:
            return user.id
        return -1


class BaseManager(models.Manager):
    """自定义模型管理器"""

    def first(self, *args, **kwargs):
        """获取一条数据"""

        clone = self.filter(*args, **kwargs)
        clone = clone.order_by()
        if len(clone) >= 1:
            return clone._result_cache[0]
        return None

    def save_new(self, model, user):
        """保存或更新数据"""

        if model.id and model.id > 0:
            origin = self.first(id=model.id)
            if origin:
                model.create_user = origin.create_user
                model.create_time = origin.create_time
                model.update_user = user
                model.update_time = timezone.now()
        else:
            model.create_user = user
            model.create_time = timezone.now()
        model.save()


class UserInfo(AbstractBaseUser):
    """用户信息"""

    class Meta:
        db_table = 'user_info'

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


class BaseModel(models.Model):
    """模型抽象类"""

    class Meta:
        abstract = True

    id = models.AutoField(unique=True, primary_key=True, db_index=True)
    create_user = models.ForeignKey(UserInfo, on_delete=models.SET(UserInfo.objects.get_deleted_user_id),
                                    related_name='+')
    create_time = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(UserInfo, on_delete=models.SET(UserInfo.objects.get_deleted_user_id), null=True,
                                    related_name='+')
    update_time = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    objects = BaseManager()


class Category(BaseModel):
    """分类"""

    class Meta:
        db_table = 'category'

    name = models.CharField(max_length=50)
    spell = models.CharField(max_length=200, unique=True, db_index=True)
    level = models.SmallIntegerField()
    parent_id = models.IntegerField()
    sort = models.IntegerField()


class Tag(BaseModel):
    """标签"""

    class Meta:
        db_table = 'tag'

    name = models.CharField(max_length=50)
    spell = models.CharField(max_length=200, unique=True, db_index=True)
    sort = models.IntegerField()


class Article(BaseModel):
    """文章"""

    class Meta:
        db_table = 'article'

    title = models.CharField(max_length=100, db_index=True)
    subject = models.CharField(max_length=500, null=True)
    content = models.TextField()
    cover = models.URLField(max_length=1000, null=True)
    images = models.TextField(null=True)
    category_ids = models.CharField(max_length=200, null=True)
    tag_ids = models.CharField(max_length=200, null=True)
    hits = models.IntegerField()
    score = models.DecimalField(max_digits=3, decimal_places=1)


class UploadFile(BaseModel):
    """上传文件"""

    class Meta:
        db_table = 'upload_file'

    name = models.CharField(max_length=1000)
    type = models.CharField(max_length=20, db_index=True)
    size = models.IntegerField()
    file = models.FileField(upload_to='%Y/%m/%d')
