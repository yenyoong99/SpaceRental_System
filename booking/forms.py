# -*- coding: utf-8 -*-
# @Time    : 7/31/2020 8:04 PM
# @Author  : YenYoong
# @File    : forms.py
from django import forms
from .models import BookingNew, SpacesAdd
from datetime import datetime
import time


class BookingForm(forms.Form):
    # spaces = BookingNew.objects.filter(BookingNew.status == '1')
    # username = forms.CharField(max_length=20, null=False)
    spaces_id = forms.CharField(max_length=20, error_messages={"required": "暂时没有可预定的空间"})
    datetime_set = forms.CharField(max_length=201, min_length=16, error_messages={"required": "租用日期必填！"})

    def clean(self):
        cleaned_data = super().clean()
        datetime_set = cleaned_data.get('datetime_set')
        start_datetime_form = datetime_set[0:19]
        end_datetime_form = datetime_set[22:41]

        # 将字符串转为时间戳
        start_datetime_dt = int(time.mktime(time.strptime(start_datetime_form, "%m/%d/%Y %I:%M %p")))
        end_datetime_dt = int(time.mktime(time.strptime(end_datetime_form, "%m/%d/%Y %I:%M %p")))
        format_time = time.localtime(start_datetime_dt)
        start_datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", format_time)


        # 获取当前时间，转为时间戳进行比较
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        datetime_now = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        # print(datetime_now)  # 2020-08-11 14:40:33

        if start_datetime_form and end_datetime_form:
            if start_datetime_dt < time_now or end_datetime_dt <= time_now:
                raise forms.ValidationError('不能预定过去的时间！')

            return cleaned_data

'''
旧概念
'''
# for booking_date in booking_dates_str:
#     # booking_start_datetime = datetime.strftime(booking_date.start_datetime, "%m/%d/%Y %H:%M")
#     # booking_end_datetime = datetime.strftime(booking_date.end_datetime, "%m/%d/%Y %H:%M")
#     if booking_start_datetime < start_datetime_str < booking_end_datetime:
#         raise forms.ValidationError('该时间已被其它用户预定！')

class BookingEditForm(forms.Form):
    datetime_set = forms.CharField(max_length=201, min_length=16, error_messages={"required": "租用日期必填！"})

    def clean(self):
        cleaned_data = super().clean()
        datetime_set = cleaned_data.get('datetime_set')
        start_datetime_form = datetime_set[0:19]
        end_datetime_form = datetime_set[22:41]

        # 将字符串转为时间戳
        start_datetime_dt = int(time.mktime(time.strptime(start_datetime_form, "%m/%d/%Y %I:%M %p")))
        end_datetime_dt = int(time.mktime(time.strptime(end_datetime_form, "%m/%d/%Y %I:%M %p")))
        format_time = time.localtime(start_datetime_dt)


        # 获取当前时间，转为时间戳进行比较
        time_now = int(time.time())

        if start_datetime_form and end_datetime_form:
            if start_datetime_dt < time_now or end_datetime_dt <= time_now:
                raise forms.ValidationError('不能预定过去的时间！')

            return cleaned_data

class SpacesAddForm(forms.Form):
    spaces_name = forms.CharField(max_length=20, error_messages={"required": "空间名称必填！"})
    fee = forms.FloatField(error_messages={"invalid": "请输入正确格式的费用（数字）！", "required": "租用费用必填！"})

    def clean_spaces_name(self):
        spaces_name = self.cleaned_data.get('spaces_name')
        spaces_name_exists = SpacesAdd.objects.filter(spaces_name=spaces_name).exists()
        if spaces_name_exists:
            raise forms.ValidationError('空间增加失败，空间已存在！')

        return spaces_name

class ActivityForm(forms.Form):
    # spaces = BookingNew.objects.filter(BookingNew.status == '1')
    # username = forms.CharField(max_length=20, null=False)
    activity_name = forms.CharField(max_length=20, error_messages={"required": "活动名称必填！"})
    datetime_set = forms.CharField(max_length=201, min_length=16, error_messages={"required": "租用日期必填！"})
    color = forms.CharField(max_length=7, error_messages={"required": "请选择活动显示的颜色！"})
    all_day = forms.CharField(required=False, max_length=5)

    def clean_all_day(self):
        all_day = self.cleaned_data.get('all_day')
        if all_day:
            all_day = 'true'
        else:
            all_day = 'false'

            return all_day

        return all_day

    def clean(self):
        cleaned_data = super().clean()
        datetime_set = cleaned_data.get('datetime_set')
        start_datetime_form = datetime_set[0:19]
        end_datetime_form = datetime_set[22:41]

        # 将字符串转为时间戳
        start_datetime_dt = int(time.mktime(time.strptime(start_datetime_form, "%m/%d/%Y %I:%M %p")))
        end_datetime_dt = int(time.mktime(time.strptime(end_datetime_form, "%m/%d/%Y %I:%M %p")))
        format_time = time.localtime(start_datetime_dt)
        start_datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", format_time)


        # 获取当前时间，转为时间戳进行比较
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        datetime_now = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        # print(datetime_now)  # 2020-08-11 14:40:33

        if start_datetime_form and end_datetime_form:
            if start_datetime_dt < time_now or end_datetime_dt <= time_now:
                raise forms.ValidationError('活动不能设置过去的时间！')

            return cleaned_data