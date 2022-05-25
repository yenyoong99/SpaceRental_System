from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import BookingForm, SpacesAddForm, ActivityForm, BookingEditForm
from .models import BookingNew, SpacesAdd, ActivityNew
from login.models import User
from datetime import datetime


class BookingView(View):
    def get(self, request):
        if request.user.is_authenticated:
            bookings = BookingNew.objects.filter()
            all_activity = ActivityNew.objects.filter()
            return render(request, 'booking/booking_home.html', {'bookings': bookings, 'all_activity': all_activity})
        return redirect(reverse('login:login'))

    def post(self, request):
        pass


class BookingNewView(View):
    def get(self, request):
        if request.user.is_authenticated:
            spaces = SpacesAdd.objects.filter()
            return render(request, 'booking/booking_new.html', {'spaces': spaces})
        return redirect(reverse('login:login'))

    def post(self, request):
        spaces = SpacesAdd.objects.filter()
        form = BookingForm(request.POST)

        if form.is_valid():
            try:
                user_name = request.user.username
                spaces_id = form.cleaned_data.get('spaces_id')
                spaces = SpacesAdd.objects.filter(id=spaces_id)  # 筛选Space数据
                spaces_name = spaces[0].spaces_name
                fee = spaces[0].fee
                status = spaces[0].status

                # 若表单判断无误，则获取表单验证后的资料
                start_datetime_form = form.cleaned_data.get('datetime_set')[0:19]
                end_datetime_form = form.cleaned_data.get('datetime_set')[23:41]

                # 转为时间格式
                start_datetime_dt = datetime.strptime(start_datetime_form, "%m/%d/%Y %I:%M %p")
                end_datetime_dt = datetime.strptime(end_datetime_form, "%m/%d/%Y %I:%M %p")
                order = User.objects.get(pk=request.user.pk)  # 外键查询预定用的ID
                booking_obj = BookingNew(useradd=user_name, spaces_name=spaces_name, start_datetime=start_datetime_dt, end_datetime=end_datetime_dt, fee=fee, username=order)
                if status != 0:
                    booking_obj.save()
                else:
                    return render(request, 'booking/booking_new.html', {'booking_error_message': '预定失败，空间预定状态关闭！', 'spaces': spaces})
            except:
                return render(request, 'booking/booking_new.html', {'booking_error_message': '预定失败！请联系管理员！'})
        else:
            context = {
                'forms_errors': form.errors,
                'spaces': spaces
            }
            return render(request, 'booking/booking_new.html', context=context)

        return redirect(reverse('booking:booking_manage'))


class BookingManage(View):
    def get(self, request):
        if request.user.is_authenticated:
            bookings = BookingNew.objects.filter(useradd=request.user.username).order_by("-start_datetime")
            return render(request, 'booking/booking_manage.html', {'bookings': bookings})
        return redirect(reverse('login:login'))

    def action_cancel(request):
        if request.user.is_authenticated:
            try:
                action_id = request.GET.get('id', None)
                booking = BookingNew.objects.get(pk=action_id)
                if action_id and booking.useradd == request.user.username and booking.status == 0:
                    booking.status = 2
                    booking.save()
                else:
                    return redirect(reverse('booking:booking_manage'))
            except:
                return redirect(reverse('booking:booking_manage'))

            return redirect(reverse('booking:booking_manage'))
        return redirect(reverse('login:login'))


class BookingEdit(View):
    def get(self, request):
        q = request.GET.get('id', None)
        bookings = BookingNew.objects.get(pk=q)
        if request.user.is_authenticated and request.user.username == bookings.useradd:
            try:
                return render(request, 'booking/booking_edit.html', {'bookings': bookings})
            except:
                return redirect(reverse('booking:booking_manage'))
        return redirect(reverse('login:login'))

    def post(self, request):
        bookings = BookingNew.objects.filter()
        form = BookingEditForm(request.POST)
        q = request.GET.get('id', None)
        booking = BookingNew.objects.get(pk=q)
        if form.is_valid():
            try:
                # 若表单判断无误，则获取表单验证后的资料
                start_datetime_form = form.cleaned_data.get('datetime_set')[0:19]
                end_datetime_form = form.cleaned_data.get('datetime_set')[23:41]

                # 转为时间格式
                booking.start_datetime = datetime.strptime(start_datetime_form, "%m/%d/%Y %I:%M %p")
                booking.end_datetime = datetime.strptime(end_datetime_form, "%m/%d/%Y %I:%M %p")
                booking.save()
            except:
                return render(request, 'booking/booking_manage.html', {'error_message': '活动修改失败！请联系管理员！'})
        else:
            context = {
                'forms_errors': form.errors,
                'bookings': bookings
            }
            return render(request, 'booking/booking_manage.html', context=context)

        return render(request, 'booking/booking_manage.html', {'success_msg': '您预定的：'+booking.spaces_name+'，修改成功！', 'bookings': bookings})


class BookingAdmin(View):

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser == 1:
            booking = BookingNew.objects.filter().order_by("-start_datetime")
            return render(request, 'booking/booking_admin.html', {'booking': booking})
        return redirect(reverse('login:login'))

    def post(self, request):
        pass

    # def search(request):
    #     q = request.GET.get('q')
    #     error_msg = ''
    #
    #     if not q:
    #         error_msg = '请输入要搜索的用户'
    #         return render(request, 'booking/booking_admin.html', {'error_msg': error_msg})
    #
    #     booking = BookingNew.objects.filter(username__icontains=q)
    #     return render(request, 'booking/booking_admin.html', {'error_msg': error_msg, 'booking': booking})

    def action_cancel(request):
        try:
            action_id = request.GET.get('id', None)
            booking = BookingNew.objects.get(pk=action_id)
        except:
            return redirect(reverse('booking:booking_admin'))

        if request.user.is_authenticated and request.user.is_superuser == 1 and booking.status == 0:
            if action_id:
                booking.status = 2
                booking.save()
            else:
                return redirect(reverse('booking:booking_admin'))

            return redirect(reverse('booking:booking_admin'))
        return redirect(reverse('login:login'))

    def action_success(request):
        try:
            action_id = request.GET.get('id', None)
            booking = BookingNew.objects.get(pk=action_id)
        except:
            redirect(reverse('booking:booking_admin'))

        if request.user.is_authenticated and request.user.is_superuser == 1 and booking.status == 0:
            if action_id:
                booking.status = 1
                booking.save()
            else:
                return redirect(reverse('booking:booking_admin'))

            return redirect(reverse('booking:booking_admin'))
        return redirect(reverse('login:login'))

    def delete_booking(request):
        try:
            del_id = request.GET.get('id', None)
        except:
            return redirect(reverse('booking:booking_admin'))

        if request.user.is_authenticated and request.user.is_superuser == 1:
            if del_id:
                booking = BookingNew.objects.filter(pk=del_id)
                booking.delete()
            else:
                return redirect(reverse('booking:booking_admin'))

            return redirect(reverse('booking:booking_admin'))
        return redirect(reverse('login:login'))


class SpacesAddView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser == 1:
            return render(request, 'booking/spaces_add.html')
        return redirect(reverse('login:login'))

    def post(self, request):
        form = SpacesAddForm(request.POST)
        # booking = BookingNew.objects.all()
        if form.is_valid():
            spaces_name = form.cleaned_data.get('spaces_name')
            fee = float(form.cleaned_data.get('fee'))

            spaces_obj = SpacesAdd(spaces_name=spaces_name, fee=fee)
            try:
                spaces_obj.save()
            except:
                return render(request, 'booking/apsces_add.html', {'booking_error_message': '增加失败！'})
        else:
            context = {
                'forms_errors': form.errors
            }
            return render(request, 'booking/spaces_add.html', context=context)
        return redirect(reverse('booking:spaces_manage'))


class SpacesManage(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser == 1:
            booking = SpacesAdd.objects.filter()
            return render(request, 'booking/spaces_manage.html', {'booking': booking})
        return redirect(reverse('login:login'))

    def post(self, request):
        pass

    def action_activate(request):
        try:
            action_id = request.GET.get('id', None)
            spaces = SpacesAdd.objects.get(pk=action_id)
        except:
            return redirect(reverse('booking:spaces_manage'))

        if request.user.is_authenticated and request.user.is_superuser == 1 and spaces.status == 0:
            if action_id:
                spaces.status = 1
                spaces.save()
            else:
                return redirect(reverse('booking:spaces_manage'))

            return redirect(reverse('booking:spaces_manage'))
        return redirect(reverse('login:login'))

    def action_close(request):
        try:
            action_id = request.GET.get('id', None)
            spaces = SpacesAdd.objects.get(pk=action_id)
        except:
            return redirect(reverse('booking:spaces_manage'))

        if request.user.is_authenticated and request.user.is_superuser == 1 and spaces.status == 1:
            if action_id:
                spaces.status = 0
                spaces.save()
            else:
                return redirect(reverse('booking:spaces_manage'))

            return redirect(reverse('booking:spaces_manage'))
        return redirect(reverse('login:login'))

    def delete_spaces(request):
        try:
            del_id = request.GET.get('id', None)
        except:
            return redirect(reverse('booking:spaces_manage'))

        if request.user.is_authenticated and request.user.is_superuser == 1:
            if del_id:
                spaces = SpacesAdd.objects.filter(pk=del_id)
                spaces.delete()
            else:
                return redirect(reverse('booking:spaces_manage'))

            return redirect(reverse('booking:spaces_manage'))
        return redirect(reverse('login:login'))


class ActivityManage(View):
    def get(self, request):
        if request.user.is_authenticated:
            all_activity = ActivityNew.objects.filter(useradd=request.user.username).order_by("-start_datetime")
            return render(request, 'booking/activity_manage.html', {'all_activity': all_activity})
        return redirect(reverse('login:login'))

    def action_see(request):
        if request.user.is_authenticated:
            try:
                action_id = request.GET.get('id', None)
                activity = ActivityNew.objects.get(pk=action_id)
                if action_id and activity.useradd == request.user.username and activity.status == 0:
                    activity.status = 1
                    activity.save()
                else:
                    return redirect(reverse('booking:activity_manage'))
            except:
                return redirect(reverse('booking:activity_manage'))

            return redirect(reverse('booking:activity_manage'))
        return redirect(reverse('login:login'))

    def action_no_see(request):
        if request.user.is_authenticated:
            try:
                action_id = request.GET.get('id', None)
                activity = ActivityNew.objects.get(pk=action_id)
                if action_id and activity.useradd == request.user.username and activity.status == 1:
                    activity.status = 0
                    activity.save()
                else:
                    return redirect(reverse('booking:activity_manage'))
            except:
                return redirect(reverse('booking:activity_manage'))

            return redirect(reverse('booking:activity_manage'))
        return redirect(reverse('login:login'))

    def action_delete(request):
        try:
            del_id = request.GET.get('id', None)
        except:
            return redirect(reverse('booking:activity_manage'))

        if request.user.is_authenticated and request.user.is_superuser == 1:
            if del_id:
                activity = ActivityNew.objects.filter(pk=del_id)
                activity.delete()
            else:
                return redirect(reverse('booking:activity_manage'))

            return redirect(reverse('booking:activity_manage'))
        return redirect(reverse('login:login'))


class ActivityNewView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'booking/activity_new.html')
        return redirect(reverse('login:login'))

    def post(self, request):
        activity = ActivityNew.objects.filter()
        form = ActivityForm(request.POST)

        if form.is_valid():
            try:
                user_name = request.user.username
                activity_name = request.POST.get('activity_name')
                # 若表单判断无误，则获取表单验证后的资料
                start_datetime_form = form.cleaned_data.get('datetime_set')[0:19]
                end_datetime_form = form.cleaned_data.get('datetime_set')[23:41]

                # 转为时间格式
                start_datetime_dt = datetime.strptime(start_datetime_form, "%m/%d/%Y %I:%M %p")
                end_datetime_dt = datetime.strptime(end_datetime_form, "%m/%d/%Y %I:%M %p")
                color = request.POST.get('color')
                all_day = form.cleaned_data.get('all_day')
                order = User.objects.get(pk=request.user.pk)  # 外键查询预定用的ID
                activity_obj = ActivityNew(useradd=user_name, activity_name=activity_name, start_datetime=start_datetime_dt, end_datetime=end_datetime_dt, username=order, color=color, all_day=all_day)
                activity_obj.save()
            except:
                return render(request, 'booking/activity_new.html', {'booking_error_message': '活动新增失败！请联系管理员！'})
        else:
            context = {
                'forms_errors': form.errors,
                'activity': activity
            }
            return render(request, 'booking/activity_new.html', context=context)

        return redirect(reverse('booking:activity_manage'))


class ActivityEdit(View):
    def get(self, request):
        q = request.GET.get('id', None)
        if request.user.is_authenticated and request.user.is_superuser == 1:
            try:
                activity = ActivityNew.objects.get(pk=q)
                return render(request, 'booking/activity_edit.html', {'activity': activity})
            except:
                return redirect(reverse('booking:activity_manage'))
        return redirect(reverse('login:login'))

    def post(self, request):
        all_activity = ActivityNew.objects.filter()
        form = ActivityForm(request.POST)
        q = request.GET.get('id', None)
        activity_id = ActivityNew.objects.get(pk=q)
        if form.is_valid():
            try:
                activity_id.activity_name = request.POST.get('activity_name')
                # 若表单判断无误，则获取表单验证后的资料
                start_datetime_form = form.cleaned_data.get('datetime_set')[0:19]
                end_datetime_form = form.cleaned_data.get('datetime_set')[23:41]

                # 转为时间格式
                activity_id.start_datetime = datetime.strptime(start_datetime_form, "%m/%d/%Y %I:%M %p")
                activity_id.end_datetime = datetime.strptime(end_datetime_form, "%m/%d/%Y %I:%M %p")
                activity_id.color = request.POST.get('color')
                activity_id.all_day = form.cleaned_data.get('all_day')
                activity_id.save()
            except:
                return render(request, 'booking/activity_manage.html', {'error_message': '活动修改失败！请联系管理员！'})
        else:
            context = {
                'forms_errors': form.errors,
                'all_activity': all_activity
            }
            return render(request, 'booking/activity_manage.html', context=context)

        return redirect(reverse('booking:activity_manage'))