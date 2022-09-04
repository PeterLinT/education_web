from django.conf.urls import url

from apps.users.views import UserInfoView, UploadImageView, \
    ChangePwdView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = (
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    url(r'^image/$', UploadImageView.as_view(), name="image"),
    url(r'^update/pwd/$', ChangePwdView.as_view(), name="update_pwd"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    url(r'^myfavorg/$', MyFavOrgView.as_view(), name="myfavorg"),
    url(r'^myfav_teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    url(r'^myfav_course/$', MyFavCourseView.as_view(), name="myfav_course"),
    url(r'^messages/$', MyMessageView.as_view(), name="messages"),
)
# -*- coding:utf-8 -*-
