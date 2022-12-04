from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect, HttpResponse
from staffsys import models
from django import forms
from django.core.paginator import Paginator, Page
from staffsys.utils.LoginVerificationCode import check_code

from staffsys.utils.encrypt import md5


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(
        attrs={"class": "form-control", "id": "floatingInput", "placeholder": "name@example.com"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True,
                                                                        attrs={"class": "form-control",
                                                                               "id": "floatingPassword",
                                                                               "placeholder": "Password"}))
    login_verification_code = forms.CharField(label="验证码", widget=forms.TextInput(
        attrs={"class": "form-control", "id": "floatingInput", "placeholder": "验证码"}))

    # 因为数据库的密码是加密了md5的，如果直接拿输入的明文密码加上数据库的暗文密码，验证肯定不行，所以这里先做一步处理。
    # 先把输入的密码进行加密
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 获取用户输入的验证码，但是这里为什么要使用pop，不使用get呢？
        """
        因为我们的cleaned_data之后要在数据库进行核对信息，但是数据库并没有验证码，会报错
        因此用pop可以把验证码排除到cleaned_data。
        """
        user_input_code = form.cleaned_data.pop('login_verification_code')
        sys_output_code = request.session.get('image_code', "")

        if sys_output_code.upper() != user_input_code.upper():
            form.add_error('login_verification_code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        veriry_login = models.AdminInfo.objects.filter(**form.cleaned_data).first()

        if not veriry_login:
            # 因为已经都通过了form，进入数据库后，报错的话，也不会显示，所以在这里要另外添加
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {"form": form})

        #     网站生成随机字符串；写到用户浏览器的cookies中，也写入session中
        request.session["info"] = {'id': veriry_login.id, 'name': veriry_login.username}
        request.session.set_expiry(60*60*24*5) #登陆成功的话，让session可以5天免登录
        return redirect("/admin/")

    return render(request, 'login.html', {"form": form})


from io import BytesIO


def LoginVerificationCode(request):
    # 调用含有pillow的图片
    img, code_string = check_code()
    print(code_string)

    # 将验证码编号写入session中，以便于后去获取验证码校验
    request.session['image_code'] = code_string
    # 设置一个60秒的有效时间。
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()
    return redirect("/login/")
