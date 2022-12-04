from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from staffsys import models
from staffsys.utils.encrypt import md5


def get_page_range(num, total_page, size=7):
    """
    :param num: 当前页数
    :param total_page: 总页数
    :param size: 列表的数量，即 上一页 [1,2,3,4,5,6,7] 下一页
    :return:
    """


    min = num - int(size / 2)
    min = min if min >= 1 else 1
    max = min + size - 1
    max = max if max <= total_page else total_page
    return range(min, max + 1)


def admin_index(request):
    all_admin_data = models.AdminInfo.objects.all()

    # 获取需要显示的页数
    page = request.GET.get('page')

    # 使用django自带的分页类 Paginator，在传参中，第一项是数据库对象，二项是每页显示的条数，
    # 表示从数据库导出来的信息，以15条（第二个参数）进行显示。
    paginator = Paginator(all_admin_data, 15)

    # .get_page()是获得当前页数的数据，这个方法的好处是，如果输入大于页数的数，也只会显示最大页数。输入不是数字的，就会显示第一页。十分方便不需要做判断。
    mobile_paginator = paginator.get_page(page)

    # 分页页数
    page_range = get_page_range(mobile_paginator.number, paginator.num_pages, 7)

    # ********** 分页处理 - 结束 ********** #

    context = {
        'data': mobile_paginator,
        'page_range': page_range
    }

    return render(request, 'admin.html', context)




class AdminModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))

    # (render_value=True) 当密码不一致时,数据会保留,不会清空

    class Meta:
        model = models.AdminInfo
        fields = ["username", 'password']
        widgets = {'password': forms.PasswordInput(render_value=True)}

    # 通过钩子方法去校验密码和加密
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd:
            raise ValidationError("密码不一致，请重新确认")

        # return的字段将会保存到数据库中
        return confirm_pwd


def admin_add(request):
    title = "新建管理员"

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'add.html', {'title': title, 'form': form})

    post_data = AdminModelForm(data=request.POST)
    if post_data.is_valid():
        post_data.save()
        return redirect('/admin/')

    return render(request, 'add.html', {'title': title, 'form': post_data})


def admin_del(request, nid):
    # 拿到传入的id后，直接在数据库上删除
    models.AdminInfo.objects.filter(id=nid).delete()
    return redirect('/admin/')


class AdminResetModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = models.AdminInfo
        fields = ['password']
        widgets = {'password': forms.PasswordInput(render_value=True)}

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pws = md5(pwd)

        # 去数据库校验当前密码和新密码是否一样
        # 1、现在函数中通过instance传参拿到该id， .pk是id的意思，在与新密码进行md5加密后，和数据库的md5密码进行匹配。
        # 2、如果密码存在 .exists()
        psw_check = models.AdminInfo.objects.filter(id=self.instance.pk, password=md5_pws).exists()

        # 3、进行判断处理
        if psw_check:
            raise ValidationError('不能与以前的密码相同')

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd:
            raise ValidationError("密码不一致，请重新确认")

        # return的字段将会保存到数据库中
        return confirm_pwd


def admin_reset(request, nid):
    """密码重置"""

    reset_id = models.AdminInfo.objects.filter(id=nid).first()

    if not reset_id:
        return redirect('error.html')

    title = "{}的重置密码".format(reset_id.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'add.html', {'title': title, "form": form})

    form = AdminResetModelForm(data=request.POST, instance=reset_id)
    if form.is_valid():
        form.save()
        return redirect('/admin/')
    return render(request, 'add.html', {'title': title, "form": form})



