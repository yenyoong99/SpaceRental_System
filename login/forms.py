# -*- coding: utf-8 -*-
# @Time    : 7/28/2020 12:13 AM
# @Author  : YenYoong
# @File    : forms.py

from django import forms
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, error_messages={"min_length": "请输入正确格式的用户名", "max_length": "请输入正确格式的用户名", "required": "用户名必填"})
    password = forms.CharField(max_length=20, min_length=8, error_messages={"min_length": "请输入正确格式的密码", "max_length": "请输入正确格式的密码", "required": "密码必填"})

    # def LoginCheck(self):
    #     username = User.objects.filter(username=username)
    #     password = User.objects.filter(password=password)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, error_messages={"min_length": "请输入5-20个字符的用户名", "max_length": "请输入5-20个字符的用户名", "required": "用户名必填"})
    password = forms.CharField(max_length=20, min_length=8, error_messages={"min_length": "请输入8-20位长度的密码", "max_length": "请输入8-20位长度的密码", "required": "密码必填"})
    password2 = forms.CharField(max_length=20, min_length=8, error_messages={"min_length": "", "max_length": "", "required": ""})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise forms.ValidationError('用户名已经存在')

        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('密码输入不一致')
        return cleaned_data


class UserForm(forms.Form):
    password = forms.CharField(required=False, max_length=20, min_length=8, error_messages={"min_length": "密码至少包含8个字符！", "max_length": "密码太长！不超过20个字符！"})
    ic = forms.CharField(max_length=12, min_length=12, error_messages={"min_length": "请输入正确格式的身份证", "max_length": "请输入正确格式的身份证", "required": "身份证必填"})
    email = forms.EmailField(error_messages={"required": "电子邮件必填", "invalid": "请输入正确的电子邮件"})
    tel = forms.CharField(error_messages={"required": "手机号必填"})
    bank_acc = forms.IntegerField(error_messages={"required": "银行户口必填", "invalid": "请输入正确的银行户口号码"})


class UserAdd(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, error_messages={"min_length": "请输入5-20个字符的用户名", "max_length": "请输入5-20个字符的用户名", "required": "用户名必填"})
    password = forms.CharField(max_length=20, min_length=8, error_messages={"min_length": "请输入8-20位长度的密码", "max_length": "请输入8-20位长度的密码", "required": "密码必填"})
    ic = forms.CharField(max_length=12, min_length=12, error_messages={"min_length": "请输入正确格式的身份证", "max_length": "请输入正确格式的身份证", "required": "身份证必填"})
    email = forms.EmailField(error_messages={"required": "电子邮件必填", "invalid": "请输入正确的电子邮件"})
    tel = forms.CharField(error_messages={"required": "手机号必填"})
    bank_acc = forms.IntegerField(error_messages={"required": "银行户口必填", "invalid": "请输入正确的银行户口号码"})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise forms.ValidationError('用户名已经存在！')

        return username


class ChangePwdForm(forms.Form):
    old_password = forms.CharField(max_length=20, min_length=8, error_messages={"min_length": "请输入8-20位长度的密码", "max_length": "请输入8-20位长度的密码", "required": "旧密码不能为空！"})
    password = forms.CharField(max_length=20, min_length=8, error_messages={"min_length": "请输入8-20位长度的密码", "max_length": "请输入8-20位长度的密码", "required": "新密码必填！"})
    password2 = forms.CharField(max_length=20, min_length=8, error_messages={"min_length": "请输入8-20位长度的密码", "max_length": "请输入8-20位长度的密码", "required": "新密码确认必填！"})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('密码输入不一致')
        return cleaned_data