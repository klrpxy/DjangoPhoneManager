from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from django.shortcuts import render, redirect, HttpResponse




class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'form_field_captcha.html'


class CaptchaTestForm(forms.Form):
    template_name = "form_snippet.html"
    user_name = forms.CharField(
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

    return HttpResponse("验证成功")




