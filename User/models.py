from django.db import models

# class Teacher(models.Model):
#     username = models.CharField(max_length=50, verbose_name="用户名")
#     name = models.CharField(max_length=50, verbose_name="姓名")
#     password = models.CharField(max_length=100, verbose_name="密码")
#     age = models.IntegerField(verbose_name="年龄")
#     gender = models.BinaryField(verbose_name="性别")
#     phone = models.CharField(max_length=11, verbose_name="手机号码")
#     wx_openid = models.CharField(max_length=50, verbose_name="微信开放ID")

class Admin(models.Model):
    username = models.CharField(max_length=50, verbose_name="用户名")
    nickname = models.CharField(max_length=50, verbose_name="姓名", null=True)
    password = models.CharField(max_length=100, verbose_name="密码")
    avatar = models.CharField(max_length=100, verbose_name="头像", null=True)
    age = models.IntegerField(verbose_name="年龄", null=True)
    gender = models.IntegerField(verbose_name="性别", null=True)
    phone = models.CharField(max_length=11, verbose_name="手机号码", null=True)
    wx_openid = models.CharField(max_length=50, verbose_name="微信开放ID", null=True)

class Teacher(models.Model):
    username = models.CharField(max_length=50, verbose_name="用户名")
    nickname = models.CharField(max_length=50, verbose_name="姓名", null=True)
    password = models.CharField(max_length=100, verbose_name="密码")
    avatar = models.CharField(max_length=100, verbose_name="头像", null=True)
    age = models.IntegerField(verbose_name="年龄", null=True)
    gender = models.IntegerField(verbose_name="性别", null=True)
    phone = models.CharField(max_length=11, verbose_name="手机号码", null=True)
    wx_openid = models.CharField(max_length=50, verbose_name="微信开放ID", null=True)

class Student(models.Model):
    username = models.CharField(max_length=50, verbose_name="用户名")
    number = models.CharField(max_length=50, verbose_name="学号", null=True)
    nickname = models.CharField(max_length=50, verbose_name="姓名", null=True)
    password = models.CharField(max_length=100, verbose_name="密码")
    avatar = models.CharField(max_length=100, verbose_name="头像", null=True)
    age = models.IntegerField(verbose_name="年龄", null=True)
    gender = models.IntegerField(verbose_name="性别", null=True)
    school_class = models.CharField(max_length=50, verbose_name="年级", null=True)
    major = models.CharField(max_length=50, verbose_name="专业", null=True)
    phone = models.CharField(max_length=11, verbose_name="手机号码", null=True)
    wx_openid = models.CharField(max_length=50, verbose_name="微信开放ID", null=True)

