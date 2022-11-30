from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from staffsys import models
from django import forms
from django.core.paginator import Paginator, Page


# Create your views here.

# 页码分类



def index(request):
    if request.method == 'GET':
        dep_data = models.staff_department.objects.all()
        return render(request, 'index.html', {"dep_data": dep_data})


def add_depart(request):
    if request.method == "GET":
        return render(request, "add_depart.html")

    new_depart = request.POST.get('new_depart')
    models.staff_department.objects.create(title=new_depart)
    return redirect("/depart/")


def delete_depart(request):
    del_id = request.GET.get("nid")
    models.staff_department.objects.filter(id=del_id).delete()
    return redirect("/depart/")
    # return HttpResponse('删除成功')


def edit_depart(request, nid):
    if request.method == 'GET':
        edit_obj = models.staff_department.objects.filter(id=nid).first()
        print(edit_obj.title)
        return render(request, "edit_depart.html", {"edit_obj": edit_obj})

    new_depart_name = request.POST.get('new_depart_name')
    models.staff_department.objects.filter(id=nid).update(title=new_depart_name)
    return redirect("/depart/")


def user(request):
    user_data = models.staff_info.objects.all()
    return render(request, "user.html", {"user_data": user_data})


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.staff_info
        fields = ['name', 'password', 'age', "salary", "create_time", "depart", "gender"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.TextInput(attrs={"class": "form-control"}),
            "salary": forms.TextInput(attrs={"class": "form-control"}),
            "create_time": forms.TextInput(attrs={"class": "form-control"}),
            "depart": forms.Select(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
        }


def user_add(request):
    """添加用户 ModelForm"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})

    # 当用户POST提交时,数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/user/')
    else:
        return render(request, 'user_add.html', {'form': form})


def user_edit(request, nid):
    edit_obj = models.staff_info.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据获取的id读取数据库
        form = UserModelForm(instance=edit_obj)
        return render(request, 'user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=edit_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/')
    return render(request, 'user_edit.html', {'form': form})


def user_del(request, nid):
    models.staff_info.objects.filter(id=nid).delete()
    return redirect('/user/')


class MobileModelForm(forms.ModelForm):
    # 手机号码校验（正则）
    mobile = forms.CharField(
        label="手机号码",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误')]
    )

    class Meta:
        model = models.Mobile_info
        fields = ['mobile', 'price', 'level', "status", "create_time"]
        # fields = "__all__"
        widgets = {
            "mobile": forms.TextInput(attrs={'class': 'form-control'}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "create_time": forms.TextInput(attrs={"class": "form-control"}),
        }

    # 钩子方法,钩子方法也是验证的一种方法,他的特点是可以操作数据,而正则不可以.
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        # 以电话号码为查询,使用exists来查看是否存在,存在则返回TURE,不存在返回FALSE
        moblie_exists = models.Mobile_info.objects.filter(mobile=txt_mobile).exists()

        if moblie_exists:
            raise ValidationError('电话号码已存在')
        return txt_mobile


def get_page_range(num, total_page, size=7):
    '''
    :param num: 当前页数
    :param total_page: 总页数
    :param size: 列表的数量，即 上一页 [1,2,3,4,5,6,7] 下一页
    :return:
    '''

    #
    min = num - int(size / 2)
    min = min if min >= 1 else 1
    max = min + size - 1
    max = max if max <= total_page else total_page
    return range(min, max + 1)

def mobile(request):
    # 快速加入300条数据用于测试
    # for i in range(300):
    #     models.Mobile_info.objects.create(mobile='18111100001', price=100, level=1,status=1,create_time="2022-11-29")

    # 创建空字典0
    data_dict = {}
    # q有值则拿q值，否则空值
    query_value = request.GET.get('q', "")

    if query_value:  # 如果取到了需要查询的数据，则添加字典上
        data_dict['mobile__contains'] = query_value
        '''
        以上语句就会组合成：
        data_dict = { 'mobile__contains' : query_value }
        再放到搜索条件上去查询数据库
        '''
    mobile_data = models.Mobile_info.objects.filter(**data_dict)

    # ********** 分页处理 - 开始 ********** #

    # 获取需要显示的页数
    page = request.GET.get('page')
    # 使用django自带的分页类 Paginator，在传参中，第一项是数据库对象，二项是每页显示的条数
    paginator = Paginator(mobile_data,20)
    # .get_page()是获得当前页数的数据，这个方法的好处是，如果输入大于页数的数，也只会显示最大页数。输入不是数字的，就会显示第一页。十分方便不需要做判断。
    mobile_paginator = paginator.get_page(page)

    # 分页页数
    page_range = get_page_range(mobile_paginator.number,paginator.num_pages,7)

    # ********** 分页处理 - 结束 ********** #

    # 搜索条件如果想要放入的是字典，可以用两个 **星号，如果filter为空值，就会搜索全部。

    return render(request, "mobile.html", {"mobile_paginator": mobile_paginator, "page_range":page_range})


def mobile_add(request):
    if request.method == 'GET':
        form = MobileModelForm()
        return render(request, "mobile_add.html", {"form": form})

    # 当用户POST提交时,数据校验
    form = MobileModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/mobile/')
    else:
        return render(request, 'mobile_add.html', {'form': form})


class MobileEditModelForm(forms.ModelForm):
    create_time = forms.CharField(disabled=True, label='上传时间')
    mobile = forms.CharField(
        label="手机号码",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误')]
    )

    class Meta:
        model = models.Mobile_info
        fields = ['mobile', 'price', 'level', "status", "create_time"]
        # fields = "__all__"
        widgets = {
            "mobile": forms.TextInput(attrs={'class': 'form-control'}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "create_time": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_mobile(self):
        # 当前编辑的id, pk是priemry key
        edit_id = self.instance.pk
        txt_mobile = self.cleaned_data['mobile']

        # 如果不是我的id,但是电话号码却存在的话,那就报错,不然的话,就可以更新
        moblie_exists = models.Mobile_info.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if moblie_exists:
            raise ValidationError('提交的电话号码已存在')

        return txt_mobile


def mobile_edit(request, nid):  # 通过链接，会带有一个nid，一起给接收了

    # 通过id在数据库上进行查询，并且赋值到edit_id上
    edit_id = models.Mobile_info.objects.filter(id=nid).first()

    if request.method == "GET":
        # 通过 instance 把数据放到 ModelForm上，以便与在网页上渲染出该编辑的原本数据
        form = MobileEditModelForm(instance=edit_id)
        return render(request, 'mobile_edit.html', {'form': form})

    # POST请求的时候，使用该方法去接受POST过来的信息，保存到 update_form,
    # 并且把原数据给带上，不然会【新增】而不是【更新】
    update_form = MobileEditModelForm(data=request.POST, instance=edit_id)
    if update_form.is_valid():
        update_form.save()
        return redirect('/mobile/')
    return render(request, 'mobile_edit.html', {'form': update_form})


def mobile_del(request, nid):
    # 拿到传入的id后，直接在数据库上删除
    models.Mobile_info.objects.filter(id=nid).delete()
    return redirect('/mobile/')


def admin(request):
    return render(request, "admin.html")