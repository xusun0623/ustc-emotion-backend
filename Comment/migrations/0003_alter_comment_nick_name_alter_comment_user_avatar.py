# Generated by Django 4.1 on 2022-10-05 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comment', '0002_rename_user_name_comment_nick_name_comment_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='nick_name',
            field=models.CharField(max_length=50, null=True, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_avatar',
            field=models.CharField(max_length=100, null=True, verbose_name='用户头像'),
        ),
    ]