from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from django.shortcuts import render, redirect, HttpResponse
from app_web import models
from utils.encrypt import md5


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'form_field_captcha.html'


class CaptchaTestForm(forms.Form):
    template_name = "form_snippet.html"
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "输入用户名"})
    )
    password = forms.CharField(
        label="密码",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "输入密码"})
    )
    captcha = CaptchaField(
        label="验证码",
        widget=CustomCaptchaTextInput(attrs={"class": "form-control", "placeholder": "输入密码"}),
    )

def login(request):
    if request.method == "GET":
        form = CaptchaTestForm()
        return render(request, 'login.html', {'form': form})

    form = CaptchaTestForm(request.POST)
    # 验证数据是否符合格式 以及 验证码是否输入正确
    if not form.is_valid():
        form.add_error("captcha", "验证码输入错误")
        return render(request, 'login.html', {'form': form})

    # 在数据库校验用户名和密码
    input_name = form.cleaned_data["username"]
    input_pwd = form.cleaned_data["password"]
    encrypt_pwd = md5(input_pwd)
    print(input_name, encrypt_pwd)
    admin_object = models.Admin.objects.filter(username=input_name,password=encrypt_pwd).first()
    if not admin_object:
        form.add_error("username", "用户名或密码输入错误！")
        return render(request, 'login.html', {'form': form})

    request.session["info"] = {"id": admin_object.id, "name":admin_object.username}
    request.session.set_expiry(60 * 60 * 24 * 7)

    return HttpResponse("验证成功")




