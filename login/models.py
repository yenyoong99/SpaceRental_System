from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    tel = models.CharField(null=True, blank=True, max_length=11, verbose_name="手机号码")
    company = models.CharField(max_length=30, null=True, verbose_name="公司名")
    bank_name = models.CharField(max_length=20, null=False, verbose_name="银行名称")
    bank_acc = models.CharField(max_length=25, null=False, verbose_name="户口号码")
    ic = models.CharField(max_length=12, null=False, verbose_name="身份证号码")

    class Meta:
        db_table = 'auth_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


def __str__(self):
    return "User(username:%s, date_joined:%s, is_active:%s， personal_code:%s)" % (self.username, self.date_joined, self.is_active, self.personal_code)