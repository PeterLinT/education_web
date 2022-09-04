# -*- coding:utf-8 -*-
from django import forms
from captcha.fields import CaptchaField
from apps.users.models import UserProfile
class Loginform(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)

class RegisterGetForm(forms.Form):
    captcha = CaptchaField()

class UpLoadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address']

class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

    def clean(self):
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]

        if pwd1 != pwd2:
            raise forms.ValidationError("密码不一致")
        else:
            return self.cleaned_data