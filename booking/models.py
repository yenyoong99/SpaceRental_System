from django.db import models
from login.models import User


# Create your models here.
class BookingNew(models.Model):
    id = models.AutoField(primary_key=True)
    useradd = models.CharField(max_length=20, null=False)
    spaces_name = models.CharField(max_length=20, null=False)
    start_datetime = models.DateTimeField(max_length=50, null=False)
    end_datetime = models.DateTimeField(max_length=20, null=False)
    fee = models.FloatField(max_length=20, null=False)
    status = models.IntegerField(default=0)
    all_day = models.CharField(max_length=5, default='false')
    color = models.CharField(max_length=7, default='#ba6ff5')
    username = models.ForeignKey("login.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'booking_bookingnew'
        verbose_name = '租用空间'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "BookingNew(id:%s, useradd:%s, spaces_name:%s, start_datetime:%s, end_datetime:%s, fee:%s, status:%s, username:%s)" %(self.id, self.useradd, self.spaces_name, self.start_datetime, self.end_datetime, self.fee, self.status, self.username)


class SpacesAdd(models.Model):
    id = models.AutoField(primary_key=True)
    spaces_name = models.CharField(max_length=20, null=False)
    fee = models.FloatField(max_length=20, null=False)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = "booking_spacesadd"
        verbose_name = '空间增加'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "BookingNew(spaces_name:%s, fee:%s, status:%s)" %(self.spaces_name, self.fee, self.status)


class ActivityNew(models.Model):
    id = models.AutoField(primary_key=True)
    useradd = models.CharField(max_length=20, null=False)
    activity_name = models.CharField(max_length=20, null=False)
    start_datetime = models.DateTimeField(max_length=50, null=False)
    end_datetime = models.DateTimeField(max_length=20, null=False)
    status = models.IntegerField(default=1)
    all_day = models.CharField(max_length=5, default='false')
    color = models.CharField(max_length=7, default='#ba6ff5')
    username = models.ForeignKey("login.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'booking_activitynew'
        verbose_name = '活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "BookingNew(id:%s, useradd:%s, activity_name:%s, start_datetime:%s, end_datetime:%s, status:%s, username:%s)" %(self.id, self.useradd, self.activity_name, self.start_datetime, self.end_datetime, self.status, self.username)


