# -*- coding: utf-8 -*-
# @Time    : 7/28/2020 2:03 PM
# @Author  : YenYoong
# @File    : urls.py

from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path("", views.BookingView.as_view(), name='booking_home'),
    path("admin/", views.BookingAdmin.as_view(), name='booking_admin'),
    path("new/", views.BookingNewView.as_view(), name='booking_new'),
    path("manage/", views.BookingManage.as_view(), name='booking_manage'),
    path("manage/cancel/", views.BookingManage.action_cancel, name='booking_manage_cancel'),
    path("manage/edit/", views.BookingEdit.as_view(), name='booking_manage_edit'),
    path("spaces_add/", views.SpacesAddView.as_view(), name='spaces_add'),
    path("spaces_manage/", views.SpacesManage.as_view(), name='spaces_manage'),
    path("spaces_manage/activate/", views.SpacesManage.action_activate, name='spaces_activate'),
    path("spaces_manage/close/", views.SpacesManage.action_close, name='spaces_close'),
    path("spaces_manage/del/", views.SpacesManage.delete_spaces, name='spaces_delete'),
    path("admin/del/", views.BookingAdmin.delete_booking, name='admin_delete_booking'),
    path("admin/success/", views.BookingAdmin.action_success, name='admin_success_booking'),
    path("admin/cancel/", views.BookingAdmin.action_cancel, name='admin_cancel_booking'),
    path("activity/", views.ActivityManage.as_view(), name='activity_manage'),
    path("activity/new/", views.ActivityNewView.as_view(), name='activity_new'),
    path("activity/see/", views.ActivityManage.action_see, name='activity_see'),
    path("activity/no_see/", views.ActivityManage.action_no_see, name='activity_no_see'),
    path("activity/del/", views.ActivityManage.action_delete, name='activity_delete'),
    path("activity/edit/", views.ActivityEdit.as_view(), name='activity_edit'),
    # path("admin/search/", views.BookingAdmin.search, name='admin_booking_search'),
]