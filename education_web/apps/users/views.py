from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination  import PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from apps.users.forms import Loginform, RegisterGetForm, UpLoadImageForm, \
    UserInfoForm, ChangePwdForm
from apps.operations.models import UserCourse, UserFavorite, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course
from django.contrib.auth.backends import ModelBackend
from apps.users.models import UserProfile
class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def message_nums(request):
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}

class MyMessageView(LoginRequiredMixin, View):

    login_url = "/login/"
    def get(self, request, *args, **kwargs):
        current_page = 'message'

        messages_all = UserMessage.objects.filter(user=request.user)
        for message in messages_all:
            message.has_read = True
            message.save()
        # 对信息数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages_all, 5, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html',{
            'messages':messages,
            'current_page':current_page
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = 'myfavorg'
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'current_page': current_page
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = 'myfav_course'
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course = Course.objects.get(id=fav_course.fav_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
            'current_page': current_page
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = 'myfav_teacher'
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'current_page': current_page
        })


class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = 'mycourse'
        my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            'my_courses': my_courses,
            'current_page': current_page,
        })


class ChangePwdView(View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            # pwd2 = request.POST.get('password2', '')
            # if pwd1 != pwd2:
            #     return JsonResponse({
            #         'static':'fail',
            #         'msg':'密码不一致'
            #     })

            user = request.user
            user.set_password(pwd1)
            user.save()

            return JsonResponse({
                'static': 'success'

            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        image_form = UpLoadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse({
                'static': 'fail'
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = 'info'
        return render(request, 'usercenter-info.html', {'current_page': current_page

                                                        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                'static': 'success'
            })
        else:
            return JsonResponse(user_info_form.errors)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": register_get_form,

        })

    def post(self, request, *args, **kwargs):
        return render(request, "register.html")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        banners = Banner.objects.all()[:3]
        next = request.GET.get('next', '')
        return render(request, 'login.html', {
            'next': next,
            "banners": banners
        })

    def post(self, request, *args, **kwargs):
        # user_name = request.POST.get('username', '')
        # password = request.POST.get('password', '')
        login_form = Loginform(request.POST)
        banners = Banner.objects.all()[:3]
        if login_form.is_valid():

            user_name = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=user_name, password=password)

            if user is not None:
                login(request, user)

                next = request.GET.get('next', '')
                if next:
                    return HttpResponseRedirect(next)

                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form, "banners": banners})
        else:
            return render(request, 'login.html', {'login_form': login_form, "banners": banners})
