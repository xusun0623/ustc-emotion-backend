# Generated by Django 4.1 on 2022-10-04 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='学生姓名')),
                ('number', models.CharField(max_length=50, verbose_name='学号')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('gender', models.BinaryField(verbose_name='性别')),
                ('school_class', models.CharField(max_length=50, verbose_name='年级')),
                ('major', models.CharField(max_length=50, verbose_name='专业')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号码')),
                ('wx_openid', models.CharField(max_length=50, verbose_name='微信开放ID')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='学生姓名')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('gender', models.BinaryField(verbose_name='性别')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号码')),
                ('wx_openid', models.CharField(max_length=50, verbose_name='微信开放ID')),
            ],
        ),
    ]