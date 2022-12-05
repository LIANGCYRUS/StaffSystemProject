import json
from django.shortcuts import render, HttpResponse
from django import forms
from staffsys import models
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, Page


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


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'detail', 'level']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        }


def task_list(request):
    # 获取是数据库所有信息，并且是以id倒叙排列
    queryset = models.Task.objects.all().order_by('-id')
    form = TaskModelForm()

    # 获取需要显示的页数
    page = request.GET.get('page')

    # 使用django自带的分页类 Paginator，在传参中，第一项是数据库对象，二项是每页显示的条数，
    # 表示从数据库导出来的信息，以15条（第二个参数）进行显示。
    paginator = Paginator(queryset, 15)

    # .get_page()是获得当前页数的数据，这个方法的好处是，如果输入大于页数的数，也只会显示最大页数。输入不是数字的，就会显示第一页。十分方便不需要做判断。
    mobile_paginator = paginator.get_page(page)

    # 分页页数
    page_range = get_page_range(mobile_paginator.number, paginator.num_pages, 7)

    # ********** 分页处理 - 结束 ********** #

    context = {
        'data': mobile_paginator,
        'page_range': page_range,
        "form": form
    }

    return render(request, "task.html", context)


# 因为使用ajax，所以要免除 csrf提交。不然会报错
@csrf_exempt
def task_ajax(request):
    print(request.POST)
    return HttpResponse("成功")


@csrf_exempt
def task_add(request):
    print(request.POST)

    # 1、用户发送过来的数据要进行校验（ModelForm校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
