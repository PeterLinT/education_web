"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
import xadmin
from django.views.static import serve
from config.settings import MEDIA_ROOT

xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
from django.views.generic import TemplateView
from apps.users.views import LoginView, LogoutView, RegisterView
from apps.operations.views import IndexView

xversion.register_models()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    # 机构相关页面
    url(r'^org/', include(('apps.organizations.urls', "organizations"), namespace="org")),
    url(r'^op/', include(('apps.operations.urls', "operations"), namespace="op")),
    url(r'^course/', include(('apps.courses.urls', "courses"), namespace="course")),
    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),
]
