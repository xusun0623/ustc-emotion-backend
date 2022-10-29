from django.db import models

# Create your models here.
class CommentModel(models.Model):
    user_id = models.IntegerField(verbose_name="用户ID")
    user_type = models.CharField(max_length=50, verbose_name="用户类型")
    nick_name = models.CharField(max_length=50, verbose_name="用户名", null=True)
    user_avatar = models.CharField(max_length=100, verbose_name="用户头像", null=True)
    cont = models.CharField(max_length=1000, verbose_name="评论内容")
    comment_type = models.CharField(max_length=50, verbose_name="评论类型", null=True)
    time = models.CharField(max_length=50, verbose_name="评论时间", null=True)
    toxic_type = models.IntegerField(verbose_name="评论类型", null=True)
    is_delete = models.IntegerField(verbose_name="是否删除", null=True)
