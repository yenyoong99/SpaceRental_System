from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm, RegisterForm, UserForm, UserAdd, ChangePwdForm
from django.contrib.auth import authenticate, login, logout
from .models import User


class LoginView(View):
    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login/login.html', {'login_error_message': '账号或密码不正确！'})
            else:
                login(request, user)
                return redirect(reverse('booking:booking_home'))
        else:
            context = {
                'forms_errors': form.errors
            }
            return render(request, 'login/login.html', context=context)


class Logout(View):
    def get(self, request):
        logout(request)
        # Redirect to a success page.
        return redirect('login:login')


class RegisterView(View):
    def get(self, request):
        return render(request, 'login/register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
            except:
                return render(request, 'login/register.html', {'register_error_message': '注册失败'})

            # return render(request, 'login/login.html', {'login_error_message': '注册成功，请登入！'})
            return redirect(reverse('booking:booking_home'))
        else:
            context = {
                'forms_errors': form.errors
            }
            return render(request, 'login/register.html', context=context)
            # return HttpResponse('fail')


class UsersAdd(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser == 1:
            try:
                return render(request, 'login/user_add.html')
            except:
                return redirect(reverse('login:manage'))

        return redirect(reverse('login:login'))

    def post(self, request):
        form = UserAdd(request.POST)
        users = User.objects.filter()
        if request.user.is_authenticated and request.user.is_superuser == 1:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = request.POST.get('password')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                ic = request.POST.get('ic')
                company = request.POST.get('company')
                email = request.POST.get('email')
                tel = request.POST.get('tel')
                bank_name = request.POST.get('bank_name')
                bank_acc = request.POST.get('bank_acc')
                is_superuser = request.POST.get('is_superuser')
                is_active = request.POST.get('is_active')
                try:
                    User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, ic=ic, company=company, email=email, tel=tel, bank_name=bank_name, bank_acc=bank_acc, is_superuser=is_superuser, is_active=is_active)
                except:
                    return render(request, 'login/user_add.html', {'register_error_message': '用户增加失败！', 'users': users})

                return render(request, 'login/user_manage.html', {'success_msg': username+'，增加成功！', 'users': users})
            else:
                context = {
                    'forms_errors': form.errors
                }
                return render(request, 'login/user_add.html', context=context)

        return redirect(reverse('login:login'))


class UsersEdit(View):
    def get(self, request):
        q = request.GET.get('id', None)
        error_msg = ''
        if request.user.is_authenticated and request.user.is_superuser == 1:
            try:
                user_view = User.objects.get(pk=q)
                return render(request, 'login/user_edit.html', {'error_msg': error_msg, 'user_view': user_view})
            except:
                return redirect(reverse('login:manage'))
        return redirect(reverse('login:login'))

    def post(self, request):
        form = UserForm(request.POST)
        q = request.GET.get('id', None)
        usr_id = User.objects.get(pk=q)
        users = User.objects.filter()
        if request.user.is_authenticated and request.user.is_superuser == 1:
            if form.is_valid():
                if request.POST.get('password'):
                    password = form.cleaned_data.get('password')
                    usr_id.set_password(password)
                    usr_id.save()

                usr_id.first_name = request.POST.get('first_name')
                usr_id.last_name = request.POST.get('last_name')
                usr_id.ic = request.POST.get('ic')
                usr_id.company = request.POST.get('company')
                usr_id.email = request.POST.get('email')
                usr_id.tel = request.POST.get('tel')
                usr_id.bank_name = request.POST.get('bank_name')
                usr_id.bank_acc = request.POST.get('bank_acc')
                usr_id.is_superuser = request.POST.get('is_superuser')
                usr_id.save()
            else:
                context = {
                    'forms_errors': form.errors,
                    'users': users
                }
                return render(request, 'login/user_manage.html', context=context)

            return render(request, 'login/user_manage.html', {'success_msg': usr_id.username+'，资料修改成功！', 'users': users})
        return redirect(reverse('login:login'))


class UsersManage(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser == 1:
            users = User.objects.filter().order_by("-id")
            return render(request, 'login/user_manage.html', {'users': users})
        return redirect(reverse('login:login'))

    def post(self, request):
        pass

    def user_view(request):
        q = request.GET.get('id', None)
        error_msg = ''
        if request.user.is_authenticated and request.user.is_superuser == 1:
            try:
                user_view = User.objects.get(pk=q)
                return render(request, 'login/user_view.html', {'error_msg': error_msg, 'user_view': user_view})
            except:
                return redirect(reverse('login:manage'))
        return redirect(reverse('login:login'))

    def delete_user(request):
        del_id = request.GET.get('id', None)
        print(type(del_id))
        if request.user.is_authenticated and request.user.is_superuser == 1:
            if del_id and del_id != '1':
                user = User.objects.filter(pk=del_id)
                user.delete()
            else:
                return redirect(reverse('login:manage'))

            return redirect(reverse('login:manage'))
        return redirect(reverse('login:login'))


class UsersProfile(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_view = User.objects.get(username=request.user.username)
            return render(request, 'login/profile.html', {'user_view': user_view})
        return redirect(reverse('login:login'))

    def post(self, request):
        pass


class ChangePwd(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'login/password.html')
        return redirect(reverse('login:login'))

    def post(self, request):
        form = ChangePwdForm(request.POST)
        if request.user.is_authenticated and request.user.is_superuser == 1:
            if form.is_valid():
                old_password = request.POST.get('old_password')
                if request.user.check_password(old_password):
                    user = User.objects.get(username=request.user.username)
                    password = form.cleaned_data.get('password')
                    user.set_password(password)
                    user.save()
                else:
                    return render(request, 'login/password.html', {'error_message': '旧密码不正确！'})
            else:
                context = {
                    'forms_errors': form.errors,
                }
                return render(request, 'login/password.html', context=context)

            return render(request, 'login/password.html',
                          {'success_msg': user.username + '，密码修改成功！'})
        return redirect(reverse('login:login'))