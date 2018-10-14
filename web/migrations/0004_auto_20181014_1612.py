# Generated by Django 2.1 on 2018-10-14 16:12

from django.conf import settings
from django.db import migrations, models
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20181014_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(web.models.UserManager.get_deleted_user_id), related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='update_user',
            field=models.ForeignKey(null=True, on_delete=models.SET(web.models.UserManager.get_deleted_user_id), related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(web.models.UserManager.get_deleted_user_id), related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='update_user',
            field=models.ForeignKey(null=True, on_delete=models.SET(web.models.UserManager.get_deleted_user_id), related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tag',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(web.models.UserManager.get_deleted_user_id), related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tag',
            name='update_user',
            field=models.ForeignKey(null=True, on_delete=models.SET(web.models.UserManager.get_deleted_user_id), related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='create_user',
            field=models.ForeignKey(on_delete=models.SET(web.models.UserManager.get_deleted_user_id), related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='update_user',
            field=models.ForeignKey(null=True, on_delete=models.SET(web.models.UserManager.get_deleted_user_id), related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='uploadfile',
            table='blog_uploadfile',
        ),
    ]
