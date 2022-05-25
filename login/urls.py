# -*- coding: utf-8 -*-
# @Time    : 7/27/2020 8:27 PM
# @Author  : YenYoong
# @File    : urls.py

from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path("", views.LoginView.as_view(), name='login'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("users/", views.UsersManage.as_view(), name='manage'),
    path("users/view/", views.UsersManage.user_view, name='user_view'),
    path("users/del/", views.UsersManage.delete_user, name='delete_user'),
    path("users/edit/", views.UsersEdit.as_view(), name='user_edit'),
    path("users/add/", views.UsersAdd.as_view(), name='user_add'),
    path("user/profile/", views.UsersProfile.as_view(), name='user_profile'),
    path("user/change_pwd/", views.ChangePwd.as_view(), name='change_pwd'),
    path("logout/", views.Logout.as_view()),
]