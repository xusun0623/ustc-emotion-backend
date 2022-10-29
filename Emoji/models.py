from django.db import models

class Status(models.Model):
    user_id = models.IntegerField(verbose_name="用户ID")
    status_type = models.IntegerField(verbose_name="状态类型") # 1~6 代表不同的状态类型
    start_time = models.DateTimeField(max_length=50, verbose_name="开始时间")
    end_time = models.DateTimeField(max_length=50, verbose_name="结束时间", null=True)